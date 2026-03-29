import pytest
from app.dependencies import hash_password, verify_password, create_access_token, decode_token


def test_hash_and_verify_password():
    hashed = hash_password("testpassword")
    assert verify_password("testpassword", hashed)
    assert not verify_password("wrongpassword", hashed)


def test_hash_is_not_plaintext():
    hashed = hash_password("secret")
    assert hashed != "secret"


def test_create_and_decode_token():
    token = create_access_token({"sub": "42"})
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "42"


def test_decode_invalid_token_returns_none():
    result = decode_token("invalid.token.here")
    assert result is None


def test_decode_tampered_token_returns_none():
    token = create_access_token({"sub": "1"})
    tampered = token[:-5] + "XXXXX"
    assert decode_token(tampered) is None
