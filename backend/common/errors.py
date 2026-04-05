# 共通例外クラス定義


class AppError(Exception):
    """アプリケーション共通基底例外"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    """対象リソースが見つからない場合の例外"""

    def __init__(self, message: str = "指定されたリソースが見つかりません"):
        super().__init__(message, status_code=404)


class ConflictError(AppError):
    """業務制約違反・重複エラーの例外"""

    def __init__(self, message: str = "操作が競合しています"):
        super().__init__(message, status_code=409)


class UnauthorizedError(AppError):
    """認証エラーの例外"""

    def __init__(self, message: str = "認証が必要です"):
        super().__init__(message, status_code=401)
