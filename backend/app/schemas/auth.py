from pydantic import BaseModel


class LoginRequest(BaseModel):
    login_id: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
