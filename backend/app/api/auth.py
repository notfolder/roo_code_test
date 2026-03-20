"""認証関連エンドポイント。"""

from fastapi import APIRouter, Depends

from backend.app.schemas.auth import LoginRequest, TokenResponse
from backend.app.schemas.user import UserCreate, UserRead
from backend.app.services.auth import AuthService
from backend.app.api.deps import DBSession
from backend.app.core.deps import require_admin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: DBSession):
    """ログインしてJWTを取得。"""

    service = AuthService(db)
    return await service.login(data)


@router.post("/users", response_model=UserRead, dependencies=[Depends(require_admin)])
async def create_user(data: UserCreate, db: DBSession):
    """管理者がユーザーを作成。"""

    service = AuthService(db)
    return await service.create_user(data)
