from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    password: str

class NonEmptyUser(BaseModel):
    username: str = Field(..., description="Username cannot be empty")
    password: str = Field(..., description="Password cannot be empty")


user_data = {
    "username": "myusername",
    "password": "mypassword"
}

user = NonEmptyUser(**user_data)


user = NonEmptyUser(username="myusername", password="mypassword")

user_data_empty = {
    "username": "",
    "password": ""
}

user_empty = NonEmptyUser(**user_data_empty)
