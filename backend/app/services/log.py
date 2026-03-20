"""操作ログサービス。主要操作で呼び出し、操作監査を残す。"""

from backend.app.repositories.operation_log import OperationLogRepository
from backend.app.models import OperationLog


class LogService:
    """ログを一元的に記録するサービス。"""

    def __init__(self, session):
        self.repo = OperationLogRepository(session)
        self.session = session

    async def record(self, actor_id, action_type: str, target_type: str, target_id=None, message: str = ""):
        log = OperationLog(
            actor_id=actor_id,
            action_type=action_type,
            target_type=target_type,
            target_id=target_id,
            message=message or action_type,
        )
        await self.repo.add(log)
        # ログは他のトランザクションと同一セッションで commit する想定（呼び出し元で commit）

