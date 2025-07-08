from fastapi import APIRouter

order_routes=APIRouter(prefix="/order",tags=["Home"])

@order_routes.post("/create")
async def create_post():
    return {"message": "Postagem criada com sucesso!"}