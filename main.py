from fastapi import FastAPI

app = FastAPI()

from src.routes.auth_routes import auth_routes
from src.routes.order_routes import order_routes


app.include_router(auth_routes)
app.include_router(order_routes)