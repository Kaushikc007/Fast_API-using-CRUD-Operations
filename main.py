from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    phone_no: str
    address: str


users_db = {}


@app.post("/users/", status_code=201)
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User ID already exists")
    users_db[user.id] = user
    return {"message": "User created successfully"}


@app.get("/users/{id}", response_model=User)
def get_user(id: int):
    if id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[id]


@app.get("/users/search", response_model=List[User])
def search_users(name: str):
    result = [user for user in users_db.values() if user.name.lower() == name.lower()]
    return result


@app.put("/users/{id}")
def update_user(id: int, user: User):
    if id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[id].name = user.name
    users_db[id].phone_no = user.phone_no
    users_db[id].address = user.address
    return {"message": "User updated successfully"}


@app.delete("/users/{id}")
def delete_user(id: int):
    if id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[id]
    return {"message": "User deleted successfully"}


