from service.schema import user
from service.util import user as user_util
from service.util.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/auth", response_model=user.TokenBase, name="authorization")
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_util.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not user_util.validate_password(
        password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return await user_util.create_user_token(user_id=user["id"])


@router.post("/sign-up", response_model=user.User, name="registration")
async def create_user(user: user.UserCreate):
    db_user = await user_util.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_util.create_user(user=user)


@router.get("/me", response_model=user.UserBase, name="user data")
async def read_user_me(current_user: user.User = Depends(get_current_user)):
    return current_user


@router.get("/list", name="users data")
async def read_users(current_user: user.User = Depends(get_current_user)):

    return await user_util.get_users()