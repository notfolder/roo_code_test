import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import { config } from "./config";
import { router } from "./api/routes";
import { errorHandler } from "./middleware/errorHandler";
import { ensureSchema } from "./db";

async function bootstrap() {
  // スキーマを初期化
  await ensureSchema();

  const app = express();

  // 基本ミドルウェア
  app.use(helmet());
  app.use(cors());
  app.use(express.json());
  app.use(morgan("combined"));

  // API ルート
  app.use("/api", router);

  // エラーハンドラ
  app.use(errorHandler);

  app.listen(config.port, () => {
    console.log(`API server listening on port ${config.port}`);
  });
}

bootstrap().catch((err) => {
  console.error("Failed to start server", err);
  process.exit(1);
});
