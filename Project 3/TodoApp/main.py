from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, owner
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(owner.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
