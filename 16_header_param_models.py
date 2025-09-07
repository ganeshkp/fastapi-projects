from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


# @app.get("/items/")
# async def read_items(headers: Annotated[CommonHeaders, Header()]):
#     return headers


# -----------------------------------------------------------------------
# Disable Convert Underscores
"""
The same way as with regular header parameters, when you have underscore characters in the parameter names, they are automatically converted to hyphens.

For example, if you have a header parameter save_data in the code, the expected HTTP header will be save-data, and it will show up like that in the docs.

If for some reason you need to disable this automatic conversion, you can do it as well for Pydantic models for header parameters.
"""


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(
    headers: Annotated[CommonHeaders, Header(convert_underscores=False)],
):
    return headers
