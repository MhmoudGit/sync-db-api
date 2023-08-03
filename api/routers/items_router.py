from fastapi import APIRouter, HTTPException, status, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from api.models import items as items_model
from api.models.categories import Category
from api.database import get_db
from api.routers.auth_router import get_token


# create an instance of apirouter and call it
router = APIRouter(
    prefix="/items",
    tags=["items"],
)


# get single item by id
@router.get(
    "/{id}",
    response_model=items_model.ItemGet,
)
async def get_item(
    id: int,
    db: Session = Depends(get_db),
):
    items = db.query(items_model.Item).filter_by(id=id).first()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return items


# post item for sellers only
@router.post(
    "",
)
async def post_item(
    image: UploadFile = File(None),
    category_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    owner_name: str = Form(...),
    phone_number: str = Form(...),
    location: str = Form(...),
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    if token["role"] == "seller":
        item: items_model.ItemPost = {
            "image": f"/images/{image.filename}" if image is not None else None,
            "category_id": category_id,
            "title": title,
            "description": description,
            "owner_name": owner_name,
            "phone_number": phone_number,
            "location": location,
        }
        await uploads(image)
        category = db.query(Category).filter_by(id=category_id).first()
        if category is not None:
            new_item = items_model.Item(**item)
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {"message": "new Items was created successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )


# put item for sellers only
@router.put(
    "/{id}",
)
async def put_item(
    id: int,
    image: UploadFile = File(None),
    category_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    owner_name: str = Form(...),
    phone_number: str = Form(...),
    location: str = Form(...),
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    if token["role"] == "seller":
        item: items_model.ItemPost = {
            "category_id": category_id,
            "title": title,
            "description": description,
            "owner_name": owner_name,
            "phone_number": phone_number,
            "location": location,
        }
        old_item = db.query(items_model.Item).filter_by(id=id)
        if old_item.first():
            if image:
                await uploads(image)
            item["image"] = (
                f"/images/{image.filename}"
                if image is not None
                else old_item.first().image,
            )
            old_item.update(item.model_dump(), synchronize_session=False)
            db.commit()
            return {"message": "item updated successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"item with id {id} doesnt exist",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Access",
        )


# delete item for sellers only
@router.delete(
    "/{id}",
)
async def delete_item(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    if token["role"] == "seller":
        old_item = db.query(items_model.Item).filter_by(id=id)
        if old_item.first():
            old_item.delete()
            db.commit()
            return {"message": "item deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )


### upload images
async def uploads(image=None):
    if image is not None:
        with open(f"./api/images/{image.filename}", "wb") as img_out:
            img_out.write(await image.read())
