from datetime import datetime, timedelta, timezone

import jwt

from src.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS
from src.config import SECRET_KEY


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.now(timezone.utc)

    expire = now + (expires_delta or expire_time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
