import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import mysql.connector
from datetime import datetime, timedelta

app = FastAPI()

with mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="learning"
) as db:
    cursor = db.cursor()

SECRET_KEY = "yoursecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: User):
    cursor = db.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    values = (user.username, user.password)
    cursor.execute(query, values)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(user: User):
    cursor = db.cursor()
    query = "SELECT password FROM users WHERE username = %s"
    values = (user.username,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result:
        stored_password = result[0]
        if user.password == stored_password:
            token_data = {
                "sub": user.username,
                "exp": datetime.utcnow() + timedelta(minutes=60)
            }
            encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": encoded_jwt, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    return {"message": "You are authorized!"}
