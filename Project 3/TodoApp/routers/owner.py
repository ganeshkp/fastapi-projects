import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Owner
from database import SessionLocal
from .auth import get_current_owner
from passlib.context import CryptContext
from jose import jwt

router = APIRouter(prefix="/owner", tags=["owner"])

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
owner_dependency = Annotated[dict, Depends(get_current_owner)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OwnerVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_owner(owner: owner_dependency, db: db_dependency):
    if owner is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Owner).filter(Owner.id == owner.get("id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    owner: owner_dependency, db: db_dependency, owner_verification: OwnerVerification
):
    if owner is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    owner_model = db.query(Owner).filter(Owner.id == owner.get("id")).first()

    if not bcrypt_context.verify(
        owner_verification.password, owner_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Error on password change")
    owner_model.hashed_password = bcrypt_context.hash(owner_verification.new_password)
    db.add(owner_model)
    db.commit()


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: db_dependency):
    owner = db.query(Owner).filter(Owner.email == request.email).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    reset_token = jwt.encode(
        {"sub": owner.email, "exp": expires, "purpose": "password_reset"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    reset_link = f"https://yourfrontend.com/reset-password?token={reset_token}"

    # TODO: Send via email
    print(f"Send this link to owner: {reset_link}")

    return {"message": "Password reset link sent to your email"}


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: db_dependency):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("purpose") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid token type")
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    owner = db.query(Owner).filter(Owner.email == email).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    owner.hashed_password = bcrypt_context.hash(request.new_password)
    db.add(owner)
    db.commit()

    return {"message": "Password reset successful"}
