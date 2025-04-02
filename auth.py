from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


# Secret key used to sign the JWT
JWT_SECRET = "your-secret-key"  # Replace with a secure secret key
JWT_ALGORITHM = "HS256"  # Algorithm to use for signing

# FastAPI's built-in HTTP Bearer security schema for authentication
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generate a new JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_access_token(token: str):
    """
    Decode and verify a JWT token.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or malformed")


def auth_required(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
       Verifies the JWT token and extracts the payload.

       Args:
           credentials (HTTPAuthorizationCredentials): Authorization header with the `Bearer` token.

       Returns:
           dict: Decoded payload from the token.
       """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


