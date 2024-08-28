from fastapi import APIRouter

from models.todos import Todo
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()


# GET Request Method
@router.get("/")
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos


# POST Request Method
@router.post("/")
async def create_todo(todo: Todo):
    collection_name.insert_one(dict(todo))


# PUT Request Method
@router.put("/{id}")
async def update_todo(id: str, todo: Todo):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(todo)})


# DELETE Request Method
@router.delete("/{id}")
async def delete_todo(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
