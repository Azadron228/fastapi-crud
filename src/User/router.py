from fastapi import Depends, HTTPException, status
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from src.User.UserSchema import UserSchema, AuthCredentials, UserCreate
from src.auth import jwt
from src.auth.jwt import AuthHandler, verify_password

from src.models.Base import get_db
from src.models.User import create_user, User, UserRole

router = APIRouter()

auth_handler = AuthHandler()
users = []

class Paylod(BaseModel):
    context: UserSchema
    iat: int
    exp: int


def encode_token(self, Payload):
    return jwt.encode(
        Payload,
        self.secret,
        algorithm='HS256'
    )


@router.post("/users", response_model=AuthCredentials)
def test(auth_details: AuthCredentials):
    token = auth_handler.encode_token("dwadaw")
    print(token)
    return

@router.post("/register", response_model=UserCreate)
async def create_user_endpoint(db: Session = Depends(get_db)):

    user = User(name="dwad", email="tgrrg", password="password", role="user")
    # db.add(user)
    # db.commit()
    # db.refresh(user)

    stmt = insert(User).values(user)
    result = await db.execute(stmt)
    # products = result.scalars().all()

    # user = create_user(db, user.name, user.email, user.password, user.role)
    return result

user_data = {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "hashedpassword",
    "role": "admin"
}


@router.post("/login")
def login(auth_credentials: AuthCredentials, db: Session = Depends(get_db)):


    user = db.query(User).filter(User.email == auth_credentials.email).first()
    return user['password']

    # if not user or not verify_password(auth_credentials.password, user.password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid email or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    #
    # payload = Paylod(UserSchema, 12314, 52345)
    # token = auth_handler.encode_token(payload)
    #
    # # Create access token
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"email": user.email, "role": user.role},
    #     expires_delta=access_token_expires,
    # )
    #
    # return {"access_token": access_token, "token_type": "bearer"}

@router.post('/login')
def login(auth_details: AuthCredentials):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

    token = auth_handler.encode_token(user['username'])
    print(user)
    return {'token': token}


@router.get('/unprotected')
def unprotected():
    return {'hello': 'world'}


@router.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}
