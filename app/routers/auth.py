from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from ..schemas import UserCreate, UserLogin
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
import os

router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Now write two functions below that skeleton — don't write endpoints yet, just utility functions:
# 1. hash_password(password: str) — takes a plain password, returns hashed version
# 2. verify_password(plain_password, hashed_password) — returns True or False
# Hint — pwd_context has two methods: .hash() and .verify(). Figure out how to use them.


def hash_password(password : str):
    return pwd_context.hash(password)
# takes pass as str and hashes it and returns

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
# verify the plain_password given by user to hashed_password it generated earlier

def create_access_token(data : dict):
    to_encode = data.copy()

    # set expiration time
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update( {'exp' : expire})

    # Encode the JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# POST /register
# Takes: username, email, password
# Does:
# - Check if email already exists in DB, if yes return error
# - Hash the password
# - Create new User object and save to DB
# - Return success message

@router.post('/register/')
def register(user: UserCreate, db : Session = Depends(get_db)):
    
    # check if email exist
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user :
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # hash the password
    hashed = hash_password(user.password)

    #create new user object and save to db
    new_user = models.User(username = user.username, email = user.email, password = hashed)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


# Same signature pattern as register
# Find user by email
# Verify password using verify_password()
# If wrong, raise HTTPException
# If correct, call create_access_token() and return the token
@router.post('/login/')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    find_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if find_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    if not verify_password(user_credentials.password, find_user.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    
    return {"access_token": create_access_token({"user_id": find_user.id}), "token_type": "bearer"}


