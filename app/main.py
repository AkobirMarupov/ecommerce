from fastapi import FastAPI
from app.routes import users



app = FastAPI(title="E-commerce API")

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome API"}
