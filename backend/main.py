"""FastAPIアプリ起動・ルーター登録・CORS設定"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, equipment, user

# ログ設定（監査ログ用）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="備品管理システム")

# CORS設定（nginxオリジンのみ許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    """全APIリクエストの監査ログを出力する"""
    response = await call_next(request)
    logger.info(
        "method=%s path=%s status=%d",
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


# ルーター登録（全エンドポイントは /api/ 以下）
app.include_router(auth.router, prefix="/api")
app.include_router(equipment.router, prefix="/api")
app.include_router(user.router, prefix="/api")
