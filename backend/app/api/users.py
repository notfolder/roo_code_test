"""ユーザー参照用エンドポイント。"""

from fastapi import APIRouter, Depends

from backend.app.api.deps import DBSession
from backend.app.core.deps import require_admin
from backend.app.repositories.user import UserRepository
from backend.app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[UserRead])
async def list_users(db: DBSession):
    repo = UserRepository(db)
    users = await repo.list()
    return users
