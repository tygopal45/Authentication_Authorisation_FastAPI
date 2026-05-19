from pydantic import BaseModel, EmailStr

# schema for new user registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    role: str

# schema for user login
class UserLogin(BaseModel):
    username: str
    password: str




