from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from backend.services.auth import (
    register_user_service,
    login_user_service,
)
from database.config import get_db

router = APIRouter()

# Pydantic models for request and response validation
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    register_data: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Endpoint to register a new user.
    """
    try:
        await register_user_service(register_data.email, register_data.password, db)
        return {"message": "User registered successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration.",
        )

@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def login_user(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Endpoint to log in a user.
    """
    try:
        token = await login_user_service(login_data.email, login_data.password, db)
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login.",
        )