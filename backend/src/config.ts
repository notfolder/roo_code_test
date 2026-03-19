import dotenv from "dotenv";

// 環境変数を読み込む
dotenv.config();

// 設定値を集約
export const config = {
  port: parseInt(process.env.PORT || "3000", 10),
  databaseUrl: process.env.DATABASE_URL || "",
  jwtSecret: process.env.JWT_SECRET || "",
  passwordExpireDays: parseInt(process.env.PASSWORD_EXPIRE_DAYS || "90", 10),
  passwordMinLength: parseInt(process.env.PASSWORD_MIN_LENGTH || "8", 10),
};

// 必須設定の簡易チェック
if (!config.databaseUrl) {
  throw new Error("DATABASE_URL が未設定です");
}
if (!config.jwtSecret) {
  throw new Error("JWT_SECRET が未設定です");
}
