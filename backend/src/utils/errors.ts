// アプリ共通のエラークラス
export class AppError extends Error {
  statusCode: number;
  code: string;

  constructor(statusCode: number, code: string, message: string) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }
}

// エラー生成ヘルパー
export const Errors = {
  authInvalid: () => new AppError(401, "AUTH_INVALID", "認証に失敗しました"),
  authExpired: () => new AppError(403, "AUTH_EXPIRED", "パスワードの有効期限が切れています"),
  validation: (msg: string) => new AppError(400, "VALIDATION_ERROR", msg),
  doubleBooking: () => new AppError(409, "DOUBLE_BOOKING", "予約が重複しています"),
  userLimit: () => new AppError(409, "USER_LIMIT_EXCEEDED", "同時予約上限を超えています"),
  cancelWindow: () => new AppError(409, "CANCEL_WINDOW_CLOSED", "キャンセル可能時間を過ぎています"),
  notFound: (msg = "対象が見つかりません") => new AppError(404, "NOT_FOUND", msg),
  server: (msg = "サーバ内部エラー") => new AppError(500, "SERVER_ERROR", msg),
};
