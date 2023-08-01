from fastapi import APIRouter, HTTPException, status, Depends, Form
from sqlalchemy.orm import Session
from api.models import items as items_model
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
    response_model=list[items_model.ItemGet],
)
async def get_item(
    id: int,
    db: Session = Depends(get_db),
):
    pass


# post item for sellers only
@router.post(
    "",
)
async def post_item(
    item: items_model.ItemPost,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    pass


# put item for sellers only
@router.put(
    "/{id}",
)
async def post_item(
    id: int,
    new_item: items_model.ItemPost,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    pass


# delete item for sellers only
@router.delete(
    "/{id}",
)
async def post_item(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    pass


# # get board Itemss
# @router.get(
#     "",
#     # response_model=list[items_model.ItemsGet],
# )
# async def get_items(db: Session = Depends(get_db)):
#     items = db.query(items_model.Items).all()
#     if not items:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     return items


# @router.post("")
# async def post_items(
#     item_id: int = Form(...),
#     name: str = Form(...),
#     price: int = Form(...),
#     db: Session = Depends(get_db),
# ):
#     item: items_model.ItemPost = {
#         "name": name,
#         "item_id": item_id,
#         "price": price,
#     }
#     ## for pydantic models we need to change the data to dict using item.dict() then unpack them using **
#     new_item = items_model.Items(**item)
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return {"message": "new Items was created successfully"}
