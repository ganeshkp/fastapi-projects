from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Owner
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateOwnerRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_owner(username: str, password: str, db):
    owner = db.query(Owner).filter(Owner.username == username).first()
    if not owner:
        return False
    if not bcrypt_context.verify(password, owner.hashed_password):
        return False
    return owner


def create_access_token(
    username: str, owner_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": owner_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_owner(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        owner_id: int = payload.get("id")
        owner_role: str = payload.get("role")
        if username is None or owner_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate owner.",
            )
        return {"username": username, "id": owner_id, "owner_role": owner_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate owner."
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_owner(db: db_dependency, create_owner_request: CreateOwnerRequest):
    create_owner_model = Owner(
        email=create_owner_request.email,
        username=create_owner_request.username,
        first_name=create_owner_request.first_name,
        last_name=create_owner_request.last_name,
        role=create_owner_request.role,
        hashed_password=bcrypt_context.hash(create_owner_request.password),
        is_active=True,
        phone_number=create_owner_request.phone_number,
    )

    db.add(create_owner_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    owner = authenticate_owner(form_data.username, form_data.password, db)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate owner."
        )
    token = create_access_token(
        owner.username, owner.id, owner.role, timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}
