from pymongo import MongoClient

client = MongoClient(
    "<url>"
)

db = client.todo_db

collection_name = db["todo_collection"]
