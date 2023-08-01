from api.database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from passlib import hash


# postgres model for product of the postgres database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, index=True)
    phone_number = Column(String, nullable=False)
    location = Column(String, nullable=False)

    ## method used in verifying password after hashing
    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.password)


## pydantic models aka schema
class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    role: str
    phone_number: str
    location: str

    class Config:
        from_attributes = True


class UserGet(BaseModel):
    id: int
    username: str
    name: str
    role: str
    phone_number: str
    location: str

    class Config:
        from_attributes = True


class GetLogin(BaseModel):
    user: UserGet
    token: str
