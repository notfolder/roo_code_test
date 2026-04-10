from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import auth, health, items, users
from app.db import init_db


app = FastAPI(title="Equipment Loan API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(users.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
