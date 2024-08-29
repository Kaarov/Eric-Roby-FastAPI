import os
from typing import Annotated
from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

# Database configurations - SQLite
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Define a simple User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


# Initialize database
Base.metadata.create_all(bind=engine)


@app.get("/user")
async def read_user(db: db_dependency):
    return db.query(User).all()


@app.post("/user")
async def create_user(name: str, background_tasks: BackgroundTasks, db: db_dependency):
    user = User(name=name)
    db.add(user)
    db.commit()
    background_tasks.add_task(print_message, name)
    return {"name": name, "message": "User created successfully"}


async def print_message(name: str):
    print(f"User {name} created successfully")
