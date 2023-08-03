from fastapi import APIRouter, HTTPException, status, Depends
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
    response_model=list[categories_model.AllCategories],
)
async def get_categories(
    db: Session = Depends(get_db),
):
    categories = db.query(categories_model.Category).all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return categories


# get single category by id
@router.get(
    "/{id}",
    response_model=categories_model.CategoryGet,
)
async def get_category(
    id: int,
    db: Session = Depends(get_db),
):
    category = db.query(categories_model.Category).filter_by(id=id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return category


# get single category items
@router.get(
    "/{id}/items",
    response_model=list[items_model.ItemGet],
)
async def get_category_items(
    id: int,
    db: Session = Depends(get_db),
):
    category = db.query(categories_model.Category).filter_by(id=id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return category.items


# post category for sellers only
@router.post(
    "",
)
async def post_category(
    category: categories_model.CategoryPost,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    if token["role"] == "seller":
        new_category = categories_model.Category(**category.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return {"message": "new category was created successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )


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
    if token["role"] == "seller":
        old_category = db.query(categories_model.Category).filter_by(id=id)
        if old_category.first():
            old_category.update(new_category.model_dump(), synchronize_session=False)
            db.commit()
            return {"message": "category updated successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )


# delete category for sellers only
@router.delete(
    "/{id}",
)
async def delete_category(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    if token["role"] == "seller":
        old_category = db.query(categories_model.Category).filter_by(id=id)
        if old_category.first():
            old_category.delete()
            db.commit()
            return {"message": "category deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )
