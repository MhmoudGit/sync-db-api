from api.models import users as users_model
from sqlalchemy.orm import Session
from passlib import hash
from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.config import settings
from datetime import timedelta, datetime
import uuid

## fastapi schema for authentication
oauth2schema = OAuth2PasswordBearer(tokenUrl="auth/login")
JWT_SECRET = settings.jwt_secret


# create an instance of apirouter and call it
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# users register
@router.post("/register", response_model=users_model.GetLogin)
async def login(
    user: users_model.UserCreate,
    db: Session = Depends(get_db),
):
    if user.role in ["seller", "buyer"]:
        new_user = await user_create(user, db)
        access_token = await create_token(new_user)
        return {
            "user": new_user,
            "token": access_token,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user role"
        )


# users login
@router.post("/login", response_model=users_model.GetLogin)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    access_token = await create_token(user)
    return {
        "user": user,
        "token": access_token,
    }


# # users logout
# @router.get("/logout")
# async def logout(
#     db: Session = Depends(get_db),
#     token: str = Depends(get_token),
# ):
#     revoke: RevokedTokens.RevokedCreate = {
#         "uuid": token["jti"],
#     }
#     revoke_token = RevokedTokens.Revoked(**revoke)
#     db.add(revoke_token)
#     db.commit()
#     db.refresh(revoke_token)
#     return {"logged out": "success"}


## Helpers
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return (
        db.query(users_model.User).filter(users_model.User.username == username).first()
    )


async def user_create(user: users_model.UserCreate, db: Session):
    hashed_password = hash.bcrypt.hash(user.password)
    user.password = hashed_password
    new_user = users_model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
):
    user = await get_user_by_username(username, db)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def create_token(
    user: users_model.User,
    expire_delta: timedelta = timedelta(minutes=600),
):
    to_encode = dict(id=user.id, role=user.role).copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    if datetime.utcnow() > expire:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated"
        )
    return token


async def get_token(token: str = Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.exceptions.DecodeError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")
    return payload
