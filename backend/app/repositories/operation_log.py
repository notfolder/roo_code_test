"""OperationLogリポジトリ。"""

from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import OperationLog
from .base import BaseRepository


class OperationLogRepository(BaseRepository[OperationLog]):
    """操作ログの永続化。"""

    def __init__(self, session: AsyncSession):
        super().__init__(OperationLog, session)
