from api.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel
from sqlalchemy.orm import relationship


# postgres model for product of the postgres database
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    image = Column(String)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    ## relation ship between items and category.
    category = relationship("Category", back_populates="items")


## pydantic models aka schema
class ItemPost(BaseModel):
    image: str
    title: str
    description: str
    owner_name: str
    phone_number: str
    location: str
    is_active: bool = True

    class Config:
        from_attributes = True


class ItemGet(ItemPost):
    id: int
    category_id: int

    class Config:
        from_attributes = True
