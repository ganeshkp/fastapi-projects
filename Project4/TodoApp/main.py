from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos, admin, owner
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(owner.router)


if __name__ == "__main__":
    uvicorn.run("TodoApp.main:app", reload=True)
