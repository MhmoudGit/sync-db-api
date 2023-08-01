from fastapi import APIRouter, HTTPException, status, Depends, Form
from sqlalchemy.orm import Session
from api.models import categories as categories_model
from api.models import items as items_model
from api.database import get_db
from api.routers.auth_router import get_token


# create an instance of apirouter and call it
router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


# get all categories
@router.get(
    "",
    response_model=list[categories_model.CategoryGet],
)
async def get_categories(
    db: Session = Depends(get_db),
):
    pass


# get single category by id
@router.get(
    "/{id}",
    response_model=list[categories_model.CategoryGet],
)
async def get_category(
    id: int,
    db: Session = Depends(get_db),
):
    pass


# get single category items
@router.get(
    "/{id}/items",
    response_model=list[items_model.ItemGet],
)
async def get_category_items(
    id: int,
    db: Session = Depends(get_db),
):
    pass


# post category for sellers only
@router.post(
    "",
)
async def post_category(
    category: categories_model.CategoryPost,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    pass


# put category for sellers only
@router.put(
    "/{id}",
)
async def put_category(
    id: int,
    new_category: categories_model.CategoryPost,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    pass


# delete category for sellers only
@router.delete(
    "/{id}",
)
async def delete_category(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    pass


# # get board categorys
# @router.get(
#     "",
#     response_model=list[categories_model.CategoryGet],
# )
# async def get_categories(db: Session = Depends(get_db)):
#     categories = db.query(categories_model.Categories).all()
#     if not categories:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     return categories


# @router.post("")
# async def post_categories(
#     category: categories_model.CategoryPost,
#     db: Session = Depends(get_db),
# ):
#     new_category = categories_model.Categories(**category.model_dump())
#     db.add(new_category)
#     db.commit()
#     db.refresh(new_category)
#     return {"message": "new category was created successfully"}
