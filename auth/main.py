from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta, timezone


load_dotenv()

# helper function to take user input
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, ("SECRET_KEY"), algorithm=("ALGORITHM"))
    return encode_jwt


app = FastAPI()
@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # hash the password
    hashed_password = utils.hash_password(user.password)

    # create a new user instance
    new_user = models.User(
        user=user.username,
        email=user.email, 
        password=hashed_password,
        role=user.role
    )

    # save user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # return the value of the new user(without the password)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "role": new_user.role}








    

