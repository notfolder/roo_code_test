"""パスワードのbcryptハッシュ化・検証（共通処理）"""
import bcrypt


class PasswordUtil:
    @staticmethod
    def hash(password: str) -> str:
        """平文パスワードをbcryptでハッシュ化して返す"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        """平文パスワードとハッシュを照合する"""
        return bcrypt.checkpw(password.encode(), hashed.encode())
