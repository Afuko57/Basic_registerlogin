from fastapi import HTTPException
from user.model.user_model import User
import config.database as db
import bcrypt
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "yoursecretkey"
ALGORITHM = "HS256"

#User registration
def register_user(user: User):
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

# User login
def user_login(user: User):
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
        cursor.close()