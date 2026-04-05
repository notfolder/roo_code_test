from common.auth import create_access_token, verify_password
from common.errors import UnauthorizedError
from repositories.admin_user_repository import AdminUserRepository


class AuthService:
    """認証に関する業務ロジックを担うサービス"""

    def __init__(self):
        self._admin_user_repo = AdminUserRepository()

    def login(self, login_id: str, password: str) -> str:
        """ログインIDとパスワードを照合し、JWTトークンを返す。失敗時は例外を送出する"""
        user = self._admin_user_repo.find_by_login_id(login_id)
        if user is None or not verify_password(password, user["password_hash"]):
            raise UnauthorizedError("IDまたはパスワードが正しくありません")
        return create_access_token({"sub": login_id})
