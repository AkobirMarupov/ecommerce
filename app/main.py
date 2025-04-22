from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.routers import users
from app.routers import products
from app.routers import category
from app.routers import order
from app.routers import review
from app.routers import order_item
from app.routers import carts
from app.routers import cart_item
from app.routers import Inventory


app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "Welcome API"}


app.include_router(users.router)
app.include_router( products.router)
app.include_router(category.router)
app.include_router(order.router)
app.include_router(order_item.router)
app.include_router(review.router)
app.include_router(carts.router)
app.include_router(cart_item.router)
app.include_router(Inventory.router)



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="E-COMMERSE",
        version="0.0.1",
        description="API with JWT-based Authentication",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi