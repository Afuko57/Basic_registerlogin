from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from user.bll.user_bll import register_user,user_login

from user.model.user_model import User

router = APIRouter(tags=["User"])

SECRET_KEY = "yoursecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register")
def register(user: User):
    return register_user(user)

@router.post("/login")
def login(user: User):
    return user_login(user)

@router.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    return {"message": "You are authorized!"}