import os
from typing import List
from datetime import datetime

from fastapi import FastAPI, Depends, File, UploadFile, Query, Response
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.gzip import GZipMiddleware

from sqlalchemy.orm import Session

from config.config import SessionLocal, engine
from model import models, schemas
from services import userService, occurrenceService, birdService
from model.queryClasses import Color, Size, Shape, Breeding

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Ornithologists REST API",
        version="1.0.6",
        description="This API provides access to the user and IOC bird data for the Ornithologists app.",
        routes=app.routes

    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    # openapi_schema["servers"] = [{
    #     "url": "http://localhost:8000"
    # }]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(GZipMiddleware, minimum_size=200)

#app.mount(picture_dir, StaticFiles(directory=picture_dir), name="pictures")


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


##################
# User
##################

@app.post("/user", operation_id='create_user', tags=["User"], response_model=schemas.User, status_code=201)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user = userService.create_user(db, user)
    return user

@app.post("/user/{id}", operation_id='add_picture_to_user', tags=["User"], response_model=schemas.User)
async def add_picture_to_user(id: int, picture: UploadFile = File(...), db: Session = Depends(get_db)):
    return await userService.add_picture_to_user(db, id, picture)

@app.get("/pictures/user/{user_id}", tags=["User"], operation_id="get_user_picture", responses=schemas.pictureResponse)
async def get_user_picture(user_id: int, db: Session = Depends(get_db)):
    return await userService.get_user_picture(db, user_id)

@app.get("/user/{id}", operation_id='get_user', tags=["User"], response_model=schemas.User)
def read_user(id: int, db: Session = Depends(get_db)):
    return userService.get_user(db, id)

@app.get("/user", operation_id='get_users', tags=["User"], response_model=List[schemas.User])
def get_users(name: str = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return userService.get_users(db, name, skip, limit)

@app.put("/user/{id}", operation_id='update_user', tags=["User"], response_model=schemas.User)
def update_user(id: int, new_prop: schemas.User, db: Session = Depends(get_db)):
    return userService.update_user(db, id, new_prop)

@app.delete("/user/{id}", operation_id='delete_user', tags=["User"], status_code=204)
def delete_user(id: int, db: Session = Depends(get_db)):
    userService.delete_user(db, id)


##################
# Occurrence
##################

@app.post("/occurrence", tags=["Occurrence"], operation_id='add_occurrence', response_model=schemas.Occurrence, status_code=201)
def create_occurrence(occurrence: schemas.Occurrence, db: Session = Depends(get_db)):
    return occurrenceService.create_occurrence(db, occurrence)

@app.post("/occurrence/{id}", tags=["Occurrence"], operation_id='add_picture_to_occurrence', response_model=schemas.Occurrence)
async def add_picture_to_occurrence(id: int, picture: UploadFile = File(...), db: Session = Depends(get_db)):
    return await occurrenceService.add_picture_to_occurrence(db, id, picture)

@app.get("/pictures/occurrence/{occurrence_id}", tags=["Occurrence"], operation_id="get_occurrence_picture", responses=schemas.pictureResponse)
async def get_occurrence_picture(occurrence_id: int, db: Session = Depends(get_db)):
    return await occurrenceService.get_occurrence_picture(db, occurrence_id)

@app.head("/pictures/occurrence/{occurrence_id}", tags=["Occurrence"], operation_id="has_occurrence_picture", status_code=204)
async def has_occurrence_picture(occurrence_id: int, db: Session = Depends(get_db)):
    if(await occurrenceService.has_occurrence_picture(db, occurrence_id)):
        return Response(status_code=204, content=None)
    else:
        return Response(status_code=404, content=None)

@app.get("/occurrence/{id}", tags=["Occurrence"], operation_id='get_occurrence', response_model=schemas.Occurrence)
def read_occurrence(id: int, db: Session = Depends(get_db)):
    return occurrenceService.get_occurrence(db, id)


@app.get("/occurrence", tags=["Occurrence"], operation_id='get_occurrences', response_model=List[schemas.Occurrence])
def query_occurrence(
        user_id: int = None,
        bird_id: int = None,
        from_ts: datetime = None,
        to_ts: datetime = None,
        longitude: float = Query(None, format="double"),
        latitude: float = Query(None, format="double"),
        radius: float = Query(None, format="double"),
        limit: int = 20,
        db: Session = Depends(get_db)
):
    return occurrenceService.get_occurrences(db, user_id, bird_id, from_ts, to_ts,
                                             latitude, longitude, radius, limit)

@app.put("/occurrence/{id}", tags=["Occurrence"], operation_id='update_occurrence', response_model=schemas.Occurrence)
def update_occurrence(id: int, new_prop: schemas.Occurrence, db: Session = Depends(get_db)):
    return occurrenceService.update_occurrence(db, id, new_prop)

@app.delete("/occurrence/{id}", tags=["Occurrence"], operation_id='delete_occurrence', status_code=204)
def delete_occurrence(id: int, db: Session = Depends(get_db)):
    occurrenceService.delete_occurrence(db, id)


##################
# Bird
##################

@app.get("/bird/{id}", tags=["Bird"], operation_id='get_bird', response_model=schemas.Bird)
def read_bird(id: int, db: Session = Depends(get_db)):
    return birdService.get_bird(db, id)

@app.get("/bird", tags=["Bird"], operation_id='get_birds', response_model=List[schemas.Bird])
def query_bird(
        part_name: str = None,
        color: Color = None,
        size: Size = None,
        shape: Shape = None,
        breeding: Breeding = None,
        skip: int = 0,
        limit: int = 20,
        db: Session = Depends(get_db)
):
    return birdService.get_birds(db, part_name, color, size, shape, breeding, skip, limit)

@app.get("/pictures/bird/{bird_id}", tags=["Bird"], operation_id="get_bird_picture", responses=schemas.pictureResponse)
async def get_bird_picture(bird_id: int, db: Session = Depends(get_db)):
    return await birdService.get_bird_picture(db, bird_id)
