from typing import List, Dict
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import schemas, models
from .services import userService
from .queryClasses import Color, Size, Shape, Breeding
from .utils import uploadPicture

picture_dir = './pictures'
bird_picture_dir = './pictures/birds'
occurrence_picture_dir = './pictures/occurrences'

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")


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

# TODO: create user
@app.post("/user", operation_id='create_user', tags=["User"], response_model=schemas.User, status_code=201)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = userService.create_user(db, user)
    return user


# TODO: add picture to user
@app.post("/user/{id}", operation_id='add_picture_to_user', tags=["User"], response_model=schemas.User)
async def add_picture_to_user(id: int, picture: UploadFile = File(...), db: Session = Depends(get_db)):
    return await userService.add_picture_to_user(db, id, picture)


# TODO: read user
@app.get("/user/{id}", operation_id='read_user', tags=["User"], response_model=schemas.User)
def read_user(id: int, db: Session = Depends(get_db)):
    return userService.read_user(db, id)


# TODO: query user (name)
@app.get("/user", operation_id='query_user', tags=["User"], response_model=List[schemas.User])
def query_user(name: str = None, db: Session = Depends(get_db)):
    print('noch ein test')
    return userService.query_user(db, name)


# TODO: update user
@app.put("/user/{id}", operation_id='update_user', tags=["User"], response_model=schemas.User)
def update_user(id: int, new_prop: schemas.UserCreate, db: Session = Depends(get_db)):
    return userService.update_user(db, id, new_prop)


# TODO: delete user
@app.delete("/user/{id}", operation_id='delete_user', tags=["User"], response_model=List[schemas.User])
def delete_user(id: int, db: Session = Depends(get_db)):
    return userService.delete_user(db, id)


##################
# Occurrence
##################

# TODO: create occurrence
@app.post("/occurrence", tags=["Occurrence"], response_model=schemas.Occurrence, status_code=201)
def create_occurrence(occurrence: schemas.OccurrenceCreate, db: Session = Depends(get_db)):
    return schemas.Occurrence()


# TODO: add picture to occurrence
@app.post("/occurrence/{id}", tags=["Occurrence"], response_model=schemas.Occurrence)
def add_picture_to_occurrence(id: int, picture: UploadFile = File(...), db: Session = Depends(get_db)):
    # TODO: get id
    id = None
    # TODO: delete old picture if it exits
    path = Path(occurrence_picture_dir, id + '.png')
    uploadPicture(picture, path)
    # TODO: add new picture_url to occurrence
    return schemas.Occurrence()


# TODO: read occurrence
@app.get("/occurrence/{id}", tags=["Occurrence"], response_model=schemas.Occurrence)
def read_occurrence(id: int, db: Session = Depends(get_db)):
    return schemas.Occurrence()


# TODO: query occurrence (user, bird, (lon, lat, radius))
@app.get("/occurrence", tags=["Occurrence"], response_model=List[schemas.Occurrence])
def query_occurrence(
        user_id: int = None,
        bird_id: int = None,
        longitude: float = None,
        latitude: float = None,
        radius: float = None,
        db: Session = Depends(get_db)
):
    return [schemas.Occurrence()]


# TODO: update occurrence
@app.put("/occurrence/{id}", tags=["Occurrence"], response_model=schemas.Occurrence)
def update_occurrence(id: int, new_prop: schemas.OccurrenceCreate, db: Session = Depends(get_db)):
    return schemas.Occurrence()


# TODO: delete occurrence
@app.delete("/occurrence/{id}", tags=["Occurrence"], response_model=schemas.Occurrence)
def delete_occurrence(id: int, db: Session = Depends(get_db)):
    return schemas.Occurrence()


##################
# Bird
##################

# TODO: read bird
@app.get("/bird/{id}", tags=["Bird"], response_model=schemas.Bird)
def read_bird(id: int, db: Session = Depends(get_db)):
    return schemas.Bird()


# TODO: query bird (color, size, shape, breeding)
@app.get("/bird", tags=["Bird"], response_model=List[schemas.Bird])
def query_bird(
        color: Color = None,
        size: Size = None,
        shape: Shape = None,
        breeding: Breeding = None,
        db: Session = Depends(get_db)
):
    return [schemas.Bird()]


##################
# Family
##################

# TODO: read family
@app.get("/family/{id}", tags=["Family"], response_model=schemas.Family)
def read_family(id: int, db: Session = Depends(get_db)):
    return schemas.Family()


# TODO: query family

##################
# Species
##################

# TODO: read species
@app.get("/species/{id}", tags=["Species"], response_model=schemas.Species)
def read_species(id: int, db: Session = Depends(get_db)):
    return schemas.Species()


# TODO: query species

##################
# Files
##################

@app.get("/files/{path:path}", tags=["Files"])
async def get_file(path: str):
    path = Path(picture_dir, path)
    return FileResponse(path)


@app.post("/files/", tags=["Files"])
async def upload_file(file: UploadFile = File(...), response_model=Dict[str, float]):
    path = Path(picture_dir, file.filename)
    await uploadPicture(file, path)
    return {"filename": file.filename}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Ornithologists REST API",
        version="1.0.0",
        description="This API provides access to the user and IOC bird data for the Ornithologists app.",
        routes=app.routes,
        openapi_prefix="/api"

    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
