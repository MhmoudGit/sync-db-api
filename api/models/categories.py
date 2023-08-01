from api.database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from .items import ItemGet


# postgres model for categories of the postgres database
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    items = relationship("Item", back_populates="category")


## pydantic models aka schema
class CategoryPost(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CategoryGet(CategoryPost):
    id: int
    items: list[ItemGet]

    class Config:
        from_attributes = True
