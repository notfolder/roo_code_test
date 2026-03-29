from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.init_db import create_tables, create_initial_data
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.equipment import router as equipment_router
from app.routers.loans import router as loans_router
from app.routers.reservation import router as reservation_router

app = FastAPI(title="備品管理システム", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    create_tables()
    create_initial_data()


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(equipment_router, prefix="/api/equipment", tags=["equipment"])
app.include_router(loans_router, prefix="/api/loans", tags=["loans"])
app.include_router(reservation_router, prefix="/api/reservations", tags=["reservations"])


@app.get("/api/health")
def health():
    return {"status": "ok"}
