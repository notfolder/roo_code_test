"""認証サービス。"""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import verify_password, get_password_hash, create_access_token
from backend.app.repositories.user import UserRepository
from backend.app.schemas.auth import LoginRequest, TokenResponse
from backend.app.schemas.user import UserCreate
from backend.app.models import User
from backend.app.services.log import LogService


class AuthService:
    """認証/ユーザー作成を司るサービス。"""

    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)
        self.log = LogService(session)
        self.session = session

    async def login(self, data: LoginRequest) -> TokenResponse:
        """メールとパスワードでログインし、JWT を返す。"""

        user = await self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="認証に失敗しました")

        token = create_access_token(str(user.id))
        await self.log.record(user.id, "login", "user", user.id, "ログイン")
        await self.session.commit()
        return TokenResponse(access_token=token)

    async def create_user(self, data: UserCreate) -> User:
        """管理者用: 新規ユーザーを作成。"""

        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="メールが重複しています")

        password_hash = get_password_hash(data.password)
        user = User(
            email=data.email,
            name=data.name,
            role=data.role,
            password_hash=password_hash,
        )
        await self.repo.add(user)
        await self.log.record(None, "create_user", "user", user.id, f"{user.email} 作成")
        await self.session.commit()
        await self.session.refresh(user)
        return user
