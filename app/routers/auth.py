from fastapi import APIRouter, Depends, HTTPException, Request
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
from ..ratelimiter import check_ip_rate_limit

router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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



@router.post('/register/')
def register(request: Request, user: UserCreate, db : Session = Depends(get_db)):
    
    check_ip_rate_limit(request)

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


@router.post('/login/')
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    check_ip_rate_limit(request)

    # find user in db
    find_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if find_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    if not verify_password(user_credentials.password, find_user.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    
    return {"access_token": create_access_token({"user_id": find_user.id}), "token_type": "bearer"}


