import gzip
from typing import List, Dict, Callable
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Request, Response
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import schemas, models
from .services import userService, occurrenceService, birdService, familyService, speciesService
from .queryClasses import Color, Size, Shape, Breeding
from .utils import uploadPicture

picture_dir = './pictures'
bird_picture_dir = './pictures/birds'

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Ornithologists REST API",
        version="1.0.0",
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

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

app.router.route_class = GzipRoute

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

@app.post("/user", operation_id='create_user', tags=["User"], response_model=schemas.User, status_code=201)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user = userService.create_user(db, user)
    return user

@app.post("/user/{id}", operation_id='add_picture_to_user', tags=["User"], response_model=schemas.User)
async def add_picture_to_user(id: int, picture: UploadFile = File(...), db: Session = Depends(get_db)):
    return await userService.add_picture_to_user(db, id, picture)

@app.get("/user/{id}", operation_id='get_user', tags=["User"], response_model=schemas.User)
def read_user(id: int, db: Session = Depends(get_db)):
    return userService.get_user(db, id)

@app.get("/user", operation_id='get_users', tags=["User"], response_model=List[schemas.User])
def get_users(name: str = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return userService.get_users(db, name, skip, limit)

@app.put("/user/{id}", operation_id='update_user', tags=["User"], response_model=schemas.User)
def update_user(id: int, new_prop: schemas.User, db: Session = Depends(get_db)):
    return userService.update_user(db, id, new_prop)

@app.delete("/user/{id}", operation_id='delete_user', tags=["User"], response_model=schemas.User)
def delete_user(id: int, db: Session = Depends(get_db)):
    return userService.delete_user(db, id)


##################
# Occurrence
##################

@app.post("/occurrence", tags=["Occurrence"], response_model=schemas.Occurrence, status_code=201)
def create_occurrence(occurrence: schemas.OccurrenceCreate, db: Session = Depends(get_db)):
    return occurrenceService.create_occurrence(db, occurrence)

@app.post("/occurrence/{id}", tags=["Occurrence"], response_model=schemas.Occurrence)
def add_picture_to_occurrence(id: int, picture: UploadFile = File(...), db: Session = Depends(get_db)):
    return occurrenceService.add_picture_to_occurrence(db, id, picture)


@app.get("/occurrence/{id}", tags=["Occurrence"], response_model=schemas.Occurrence)
def read_occurrence(id: int, db: Session = Depends(get_db)):
    return occurrenceService.get_occurrence(db, id)


@app.get("/occurrence", tags=["Occurrence"], response_model=List[schemas.Occurrence])
def query_occurrence(
        user_id: int = None,
        bird_id: int = None,
        from_ts: datetime = None,
        to_ts: datetime = None,
        longitude: float = None,
        latitude: float = None,
        radius: float = None,
        limit: int = 20,
        db: Session = Depends(get_db)
):
    return occurrenceService.get_occurrences(db, user_id, bird_id, from_ts, to_ts,
                                             latitude, longitude, radius, limit)

@app.put("/occurrence/{id}", tags=["Occurrence"], response_model=schemas.Occurrence)
def update_occurrence(id: int, new_prop: schemas.OccurrenceUpdate, db: Session = Depends(get_db)):
    return occurrenceService.update_occurrence(db, id, new_prop)

@app.delete("/occurrence/{id}", tags=["Occurrence"], response_model=schemas.Occurrence)
def delete_occurrence(id: int, db: Session = Depends(get_db)):
    return occurrenceService.delete_occurrence(db, id)


##################
# Bird
##################

@app.get("/bird/{id}", tags=["Bird"], response_model=schemas.Bird)
def read_bird(id: int, db: Session = Depends(get_db)):
    return birdService.get_bird(db, id)

@app.get("/bird", tags=["Bird"], response_model=List[schemas.Bird])
def query_bird(
        color: Color = None,
        size: Size = None,
        shape: Shape = None,
        breeding: Breeding = None,
        skip: int = 0,
        limit: int = 20,
        db: Session = Depends(get_db)
):
    return birdService.get_birds(db, color, size, shape, breeding, skip, limit)

##################
# Family
##################

@app.get("/family/{name_scientific}", tags=["Family"], response_model=schemas.Family)
def read_family(name_scientific: str, db: Session = Depends(get_db)):
    return familyService.get_families(db, name_scientific)

##################
# Species
##################

@app.get("/species/{name_scientific}", tags=["Species"], response_model=schemas.Species)
def read_species(name_scientific: str, db: Session = Depends(get_db)):
    return speciesService.get_species(db, name_scientific)

##################
# Files
##################

@app.post("/files/", tags=["Files"], response_model=schemas.FileResponse)
async def upload_file(file: UploadFile = File(...)):
    path = Path(picture_dir, file.filename)
    await uploadPicture(file, path)
    response : schemas.FileResponse = schemas.FileResponse.construct()
    response.file_url = file.filename
    return response
