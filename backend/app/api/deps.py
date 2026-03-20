"""API 層共通の依存性。"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]
