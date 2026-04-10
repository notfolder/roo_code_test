from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from .config import get_settings
from .db import SessionLocal, init_db
from .dependencies import get_current_user, get_db, require_admin
from .models import (
    Item,
    ItemState,
    LoanRecord,
    OperationLog,
    Role,
    Status,
    User,
)
from .schemas import (
    ItemCreate,
    ItemOut,
    ItemUpdate,
    LoanOut,
    LoanRequest,
    Token,
    UserCreate,
    UserOut,
    UserUpdate,
    LoginRequest,
)
from .security import create_access_token, hash_password, verify_password

settings = get_settings()

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    with SessionLocal() as session:
        stmt = select(User).where(User.email == settings.admin_email)
        admin = session.execute(stmt).scalar_one_or_none()
        if not admin:
            admin = User(
                email=settings.admin_email,
                name="総務",
                role=Role.admin,
                status=Status.active,
                hashed_password=hash_password(settings.admin_password),
            )
            session.add(admin)
            session.commit()


@app.post(f"{settings.api_prefix}/auth/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    stmt = select(User).where(User.email == payload.email)
    user = db.execute(stmt).scalar_one_or_none()
    if not user or user.status != Status.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(
        {"sub": str(user.id), "user_id": str(user.id), "role": user.role.value}
    )
    return Token(access_token=access_token, role=user.role.value, user_id=str(user.id))


def build_item_response(item: Item) -> ItemOut:
    current_user_name = item.current_user.name if item.current_user else None
    return ItemOut(
        id=str(item.id),
        asset_number=item.asset_number,
        name=item.name,
        state=item.state.value,
        current_user_id=str(item.current_user_id) if item.current_user_id else None,
        current_user_name=current_user_name,
        updated_at=item.updated_at or datetime.utcnow(),
    )


@app.get(f"{settings.api_prefix}/items", response_model=List[ItemOut])
def list_items(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> List[ItemOut]:
    stmt = (
        select(Item)
        .options(selectinload(Item.current_user))
        .order_by(Item.asset_number)
    )
    items = db.execute(stmt).scalars().all()
    return [build_item_response(item) for item in items]


@app.post(f"{settings.api_prefix}/items", response_model=ItemOut)
def create_item(
    item_in: ItemCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> ItemOut:
    item = Item(asset_number=item_in.asset_number, name=item_in.name)
    if item_in.state:
        item.state = ItemState(item_in.state)
    db.add(item)
    try:
        db.commit()
        db.refresh(item)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="asset_number already exists",
        ) from exc
    db.add(
        OperationLog(
            operation="item_create", details=f"asset_number={item.asset_number}"
        )
    )
    db.commit()
    return build_item_response(item)


@app.put(f"{settings.api_prefix}/items/{{item_id}}", response_model=ItemOut)
def update_item(
    item_id: str,
    item_in: ItemUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> ItemOut:
    stmt = select(Item).where(Item.id == item_id)
    item = db.execute(stmt).scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    if item_in.name:
        item.name = item_in.name
    if item_in.state:
        item.state = ItemState(item_in.state)
    db.commit()
    db.add(OperationLog(operation="item_update", details=f"item_id={item_id}"))
    db.commit()
    db.refresh(item)
    return build_item_response(item)


@app.post(f"{settings.api_prefix}/items/{{item_id}}/loan", response_model=LoanOut)
def loan_item(
    item_id: str,
    payload: LoanRequest,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> LoanOut:
    with db.begin():
        stmt = select(Item).where(Item.id == item_id).with_for_update()
        item = db.execute(stmt).scalar_one_or_none()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        if item.state != ItemState.available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already lent"
            )

        user = db.get(User, payload.user_id)
        if not user or user.status != Status.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Target user invalid"
            )

        item.state = ItemState.lent
        item.current_user_id = user.id
        loan_record_stmt = select(LoanRecord).where(LoanRecord.item_id == item.id)
        loan_record = db.execute(loan_record_stmt).scalar_one_or_none()
        if loan_record:
            loan_record.user = user
            loan_record.lent_at = datetime.utcnow()
            loan_record.returned_at = None
        else:
            loan_record = LoanRecord(
                item=item, user=user, lent_at=datetime.utcnow(), returned_at=None
            )
            db.add(loan_record)
        db.add(
            OperationLog(
                operation="item_loan",
                details=f"item={item.asset_number} user={user.email}",
            )
        )
        db.refresh(loan_record)
        return LoanOut(
            id=str(loan_record.id),
            item_id=str(item.id),
            user_id=str(user.id),
            lent_at=loan_record.lent_at,
            returned_at=None,
        )


@app.post(f"{settings.api_prefix}/items/{{item_id}}/return", response_model=LoanOut)
def return_item(
    item_id: str, admin: User = Depends(require_admin), db: Session = Depends(get_db)
) -> LoanOut:
    with db.begin():
        stmt = select(LoanRecord).where(LoanRecord.item_id == item_id).with_for_update()
        loan_record = db.execute(stmt).scalar_one_or_none()
        if not loan_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Loan record not found"
            )
        if loan_record.returned_at:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already returned"
            )

        loan_record.returned_at = datetime.utcnow()
        item = db.get(Item, item_id)
        if item:
            item.state = ItemState.available
            item.current_user_id = None
        db.add(
            OperationLog(
                operation="item_return",
                details=f"item={item.asset_number if item else item_id}",
            )
        )
        db.refresh(loan_record)
        return LoanOut(
            id=str(loan_record.id),
            item_id=str(loan_record.item_id),
            user_id=str(loan_record.user_id),
            lent_at=loan_record.lent_at,
            returned_at=loan_record.returned_at,
        )


@app.get(f"{settings.api_prefix}/users", response_model=List[UserOut])
def list_users(
    admin: User = Depends(require_admin), db: Session = Depends(get_db)
) -> List[UserOut]:
    stmt = select(User).order_by(User.email)
    users = db.execute(stmt).scalars().all()
    return [
        UserOut(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role=user.role.value,
            status=user.status.value,
        )
        for user in users
    ]


@app.post(f"{settings.api_prefix}/users", response_model=UserOut)
def create_user(
    payload: UserCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserOut:
    user = User(
        email=payload.email,
        name=payload.name,
        hashed_password=hash_password(payload.password),
        role=Role.employee,
        status=Status.active,
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        ) from exc
    db.add(OperationLog(operation="user_create", details=f"email={user.email}"))
    db.commit()
    return UserOut(
        id=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role.value,
        status=user.status.value,
    )


@app.put(f"{settings.api_prefix}/users/{{user_id}}", response_model=UserOut)
def update_user(
    user_id: str,
    payload: UserUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserOut:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if payload.name:
        user.name = payload.name
    if payload.email:
        user.email = payload.email
    db.commit()
    db.add(OperationLog(operation="user_update", details=f"user_id={user_id}"))
    db.commit()
    return UserOut(
        id=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role.value,
        status=user.status.value,
    )


@app.delete(f"{settings.api_prefix}/users/{{user_id}}", response_model=UserOut)
def delete_user(
    user_id: str, admin: User = Depends(require_admin), db: Session = Depends(get_db)
) -> UserOut:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user.status = Status.deleted
    db.commit()
    db.add(OperationLog(operation="user_delete", details=f"user_id={user_id}"))
    db.commit()
    return UserOut(
        id=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role.value,
        status=user.status.value,
    )


@app.get(f"{settings.api_prefix}/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})
