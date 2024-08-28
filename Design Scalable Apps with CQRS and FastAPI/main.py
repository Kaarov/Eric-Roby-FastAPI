from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlmodel import Field, SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select as async_select
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # Use conn.run_sync() if you need to run synchronous functions
        # e.g., for creating table with SQLModel or SQLAlchemy
        await conn.run_sync(SQLModel.metadata.create_all)

    yield  # Yield control back to the application

    # If there were any shutdown tasks, they could be added here
    # For example, you might want to close async engine connections


app = FastAPI(lifespan=lifespan)

# Async database setup
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Models
class ItemBase(SQLModel):
    name: str
    description: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ItemRead(ItemBase):
    id: int


# Service Layer
class ItemService:
    async def create_item(self, item: ItemCreate, db: Session) -> Item:
        db_item = Item(name=item.name, description=item.description)
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    async def get_item(self, item_id: int, db: Session) -> Item:
        async with db as session:
            statement = async_select(Item).where(Item.id == item_id)
            result = await session.execute(statement)
            item = result.scalar()
            return item

    async def get_items(self, db: Session) -> List[Item]:
        async with db as session:
            statement = async_select(Item)
            result = await session.execute(statement)
            items = result.scalars().all()
            return items


# Dependency
def get_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_item_service():
    return ItemService()


db_dependency = Annotated[Session, Depends(get_db)]
item_service_dependency = Annotated[Session, Depends(get_item_service)]


# API layer
@app.post("/items/", response_model=ItemRead)
async def create_item(item: ItemCreate, background_tasks: BackgroundTasks,
                      item_service: item_service_dependency, db: db_dependency):
    created_item = await item_service.create_item(item, db)
    background_tasks.add_task(log_operation, item_id=created_item.id)
    return created_item


@app.get("/items/", response_model=List[ItemRead])
async def read_items(db: db_dependency, item_service: item_service_dependency):
    items = await item_service.get_items(db)
    return items


@app.get("/items/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, db: db_dependency, item_service: item_service_dependency):
    item = await item_service.get_item(item_id, db)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")


async def log_operation(item_id: int):
    # Placeholder function to simulate an async background task
    print(f"Logging operation for item_id: {item_id}")
