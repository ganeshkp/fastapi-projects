from typing import Annotated

from fastapi import Cookie, FastAPI, Response

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


@app.get("/set-cookie/")
def set_cookie(response: Response):
    response.set_cookie(
        key="ads_id",
        value="fggg",
        httponly=True,  # not accessible from JavaScript
        secure=False,  # set True if using HTTPS
        samesite="Lax",  # controls cross-site behavior
    )
    return {"message": "Cookie set successfully"}
