from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from sql_app import models, schemas
from sql_app.database import localSession, engine
from sqlalchemy.sql.expression import func
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

SECRET_KEY = "fc364310651db317ac759b29594b6af12ec1a1534d41177a00b640f6dbb8139d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

'''
As backend and frontend are running on the same machine and browser
google chrome and firefox are blocking the fetch() request stating that
CORS (Cross-Origin Resource Sharing)
so we need to allow CORS

Refer: https://fastapi.tiangolo.com/tutorial/cors/

Open the client side HTML after starting the python -m http.server 500
in that required folder
'''

app = FastAPI()

origins = [
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Dependency
def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_create(userName: str):
    db_user = localSession().query(models.loginDetails).filter(models.loginDetails.username == userName).first()

    #print(type(db))
    #Check - 1
    if (db_user):
        data = schemas.loginDetailsCreate(username=db_user.username, fullname=db_user.fullname, password=db_user.password)
        return data

def get_user_read(userName: str):
    db_user = localSession().query(models.loginDetails).filter(models.loginDetails.username == userName).first()

    #print(type(db))
    #Check - 1
    if (db_user):
        b =  False if (str(db_user.disabled) == "false") else True
        data = schemas.loginDetailsRead(uid = int(db_user.uid),username=db_user.username, fullname=db_user.fullname, disabled=b)
        return data

def authenticate_user(username: str, password: str):
    user = get_user_create(username)

    if(not user):
        return False
    
    if(not verify_password(password, user.password)):
        return False

    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if (expires_delta):
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception  = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not Validate credentials",
        headers = {"WWW-Authenticate" : "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("id")

        if (username is None):
            raise credentials_exception

        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_read(userName=token_data.username)

    if(user is None):
        raise credentials_exception

    return user

async def get_current_active_user(current_user: schemas.loginDetailsRead = Depends(get_current_user)):
    if(not current_user.disabled):
        raise HTTPException(status_code = 400, detail="Inactive User")

    return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(formData: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(formData.username, formData.password)

    if(not user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or Password",
            headers={"WWW-Authenticate" : "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data = {"id" : user.username}, expires_delta=access_token_expires
    )

    return {"access_token" : access_token, "token_type" : "bearer"}

@app.post("/signup", response_model=schemas.loginDetailsRead)
def create_user(user: schemas.loginDetailsCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.loginDetails).filter(models.loginDetails.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashedPassword = get_password_hash(user.password)

    t = db.query(func.max(models.loginDetails.uid)).scalar()

    if t == None:
        t = 0

    t = int(t) + 1

    db_user = models.loginDetails(uid = t, username = user.username, fullname = user.fullname, password = hashedPassword, disabled = False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.get("/users/me", response_model=schemas.loginDetailsRead)
async def read_users_me(current_user: schemas.loginDetailsRead = Depends(get_current_active_user)):
    return current_user
    

