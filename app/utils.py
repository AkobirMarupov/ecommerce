from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

# Konfiguratsiya sozlamalari
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1800

# Parolni xashlash uchun kontekst
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Parolni xashlash
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Parolni tekshirish
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT access token yaratish
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
