import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import { config } from "../config";
import { Errors } from "../utils/errors";

export interface AuthUser {
  userId: number;
  role: "admin" | "user";
}

declare module "express-serve-static-core" {
  interface Request {
    authUser?: AuthUser;
  }
}

// Bearer トークンを検証し、req.authUser に設定
export function requireAuth(req: Request, _res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  if (!header || !header.startsWith("Bearer ")) {
    return next(Errors.authInvalid());
  }
  const token = header.substring("Bearer ".length);
  try {
    const payload = jwt.verify(token, config.jwtSecret) as AuthUser;
    req.authUser = payload;
    return next();
  } catch (_e) {
    return next(Errors.authInvalid());
  }
}

// 管理者のみ許可
export function requireAdmin(req: Request, _res: Response, next: NextFunction) {
  if (req.authUser?.role !== "admin") {
    return next(Errors.authInvalid());
  }
  return next();
}
