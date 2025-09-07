from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


# @app.post("/items/")
# async def create_item(item: Item) -> Item:
#     return item


# @app.get("/items/")
# async def read_items() -> list[Item]:
#     return [
#         Item(name="Portal Gun", price=42.0),
#         Item(name="Plumbus", price=32.0),
#     ]


# -------------------------------------------------------
# response_model Parameter
# @app.post("/items/", response_model=Item)
# async def create_item(item: Item) -> Any:
#     return item


# @app.get("/items/", response_model=list[Item])
# async def read_items() -> Any:
#     return [
#         {"name": "Portal Gun", "price": 42.0, "age": 200},
#         {"name": "Plumbus", "price": 32.0},
#     ]


# -------------------------------------------------------
# response_model Priority
"""
If you declare both a return type and a response_model, the response_model will take priority and be used by FastAPI.

This way you can add correct type annotations to your functions even when you are returning a type different than the response model, to be used by the editor and tools like mypy. And still you can have FastAPI do the data validation, documentation, etc. using the response_model.

You can also use response_model=None to disable creating a response model for that path operation, you might need to do it if you are adding type annotations for things that are not valid Pydantic fields, you will see an example of that in one of the sections below.
"""
# Return the same input data


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


# Don't do this in production!
# @app.post("/user/")
# async def create_user(user: UserIn) -> UserIn:
#     return user


# Add an output model
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn) -> Any:
#     return user


# -------------------------------------------------------
# Return Type and Data Filtering
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


# @app.post("/user/")
# async def create_user(user: UserIn) -> BaseUser:
#     return user


# -------------------------------------------------------
# Other Return Type Annotations


# Return a Response Directly
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse


# @app.get("/portal")
# async def get_portal(teleport: bool = False) -> Response:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return JSONResponse(content={"message": "Here's your interdimensional portal."})


# -------------------------------------------------------
# Disable Response Model
# @app.get("/portal", response_model=None)
# async def get_portal(teleport: bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return {"message": "Here's your interdimensional portal."}


# -------------------------------------------------------
# Response Model encoding parameters
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
