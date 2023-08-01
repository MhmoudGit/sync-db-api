from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.database import engine, Base
from api.routers.auth_router import router as auth_router
from api.routers.categories_router import router as categories_router
from api.routers.items_router import router as items_router

Base.metadata.create_all(bind=engine)

# openapi_url=None for closing docs
app = FastAPI()

## mounts for uploading image files
app.mount("/images", StaticFiles(directory="api/images"), name="images")


app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(items_router)
