
import jwt
import bcrypt
from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import config.database as db
from datetime import datetime, timedelta

from user.model.user_model import User

router = APIRouter()

tag = "Setting : User login&Register"

SECRET_KEY = "yoursecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", tags=[tag])
def register(user: User):
    raw_password = user.password
    hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())

    connection = db.db  
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            values = (user.username, hashed_password)
            cursor.execute(query, values)
            connection.commit()
        return {"message": "User created"}
    finally:
        connection.close()

@router.post("/login", tags=[tag])
def login(user: User):
    raw_password = user.password
    
    try:
        with db.db.cursor() as cursor:
            query = "SELECT password, role FROM users WHERE username = %s"
            values = (user.username,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                stored_password, user_role = result[0], result[1]
                if bcrypt.checkpw(raw_password.encode('utf-8'), stored_password.encode('utf-8')):
                    token_data = {
                        "sub": user.username,
                        "exp": datetime.utcnow() + timedelta(minutes=60)
                    }
                    encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
                    if user_role == "admin":
                        return {"access_token": encoded_jwt, "token_type": "bearer", "message": "Admin login"}
                    else:
                        return {"access_token": encoded_jwt, "token_type": "bearer"}
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    finally:
        db.db.close()

@router.get("/protected" , tags=[tag])
def protected(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    return {"message": "You are authorized!"}
