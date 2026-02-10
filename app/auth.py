from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from bson import ObjectId
from .schemas import UserCreate, UserOut, PyObjectId
from .database import users
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "jkWE4ph6grwi@oij5@@g3p@F2tg"
ALGORITHM = "HS256"

router = APIRouter()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(username_or_email: str, password: str):
    user = users.find_one({
        "$or": [{"email": username_or_email}, {"username": username_or_email}]
    })
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users.find_one({"email": user_email})
    if user is None:
        raise credentials_exception
    return user

@router.post("/register")
def register(user: UserCreate):
    if users.find_one({"$or": [{"email": user.email}, {"username": user.username}]}):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = get_password_hash(user.password)
    user_doc = {
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password
    }
    result = users.insert_one(user_doc)
    user_doc["_id"] = str(result.inserted_id)
    return {"msg": "User registered successfully"}

@router.post("/login", summary="Login user and get access token", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "email": current_user["email"]}