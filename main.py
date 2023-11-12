from datetime import datetime
from enum import Enum
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get("/", summary="Root", response_description="Successful Response")
def root():
    return {"message": "Hello, this is my first API"}

@app.post("/post", summary="Get Post", response_description="Successful Response")
def get_post(new_timestamp: Timestamp):
    new_timestamp = Timestamp(timestamp=datetime.now())
    return Timestamp(id=new_timestamp.id,
                     timestamp=int(round(new_timestamp.timestamp.timestamp())))

@app.get("/dog", summary="Get Dogs", response_description="Successful Response", response_model=Dog)
def get_dogs(kind: DogType = Query(None, description="Dogs filter bu kind")):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())

@app.post("/dog", summary="Create Dogs", response_description="Successful Response", response_model=Dog)
def create_dogs(dog: Dog):
    dog.pk = max(dogs_db.keys()) + 1
    dogs_db[dog.pk] = dog
    return dog

@app.get("/dog/{pk}", summary="Get Dog By Pk", response_description="Successful Response", response_model=Dog)
def get_dog_by_pk(pk: int = Path(..., title="Pk", description="Pk of the dog")):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dogs_db[pk]

@app.patch("/dog/{pk}", summary="Update Dog", response_description="Successful Response", response_model=Dog)
def update_dog(pk: int = Path(..., title="Pk", description="Pk of the dog"), updated_dog: Dog):
    dog = dogs_db.get(pk)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    dog.name = updated_dog.name
    dog.kind = updated_dog.kind
    return dog