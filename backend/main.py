from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from common.errors import AppError
from database import DatabaseManager
from routers import auth, equipment, lending


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリ起動時にDBの初期化を実行する"""
    DatabaseManager().init_db()
    yield


app = FastAPI(lifespan=lifespan)

# CORS設定（nginxリバースプロキシ経由のアクセスのみ許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://frontend"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router)
app.include_router(equipment.router)
app.include_router(lending.router)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """AppError系の例外をHTTPレスポンスに変換する共通ハンドラ"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
