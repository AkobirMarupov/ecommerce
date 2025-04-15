from fastapi import FastAPI
from app.routers import users
from app.routers import products
from app.routers import category



app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "Welcome API"}


app.include_router(users.router)
app.include_router( products.router)
app.include_router(category.router)