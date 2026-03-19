import { Request, Response, NextFunction } from "express";
import { AppError } from "../utils/errors";

// 共通エラーハンドラ: AppError をステータス付きで返却し、その他は 500
export function errorHandler(err: unknown, req: Request, res: Response, _next: NextFunction) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ code: err.code, message: err.message });
  }
  console.error("Unexpected error", err);
  return res.status(500).json({ code: "SERVER_ERROR", message: "サーバ内部エラー" });
}
