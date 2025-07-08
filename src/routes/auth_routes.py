from fastapi import APIRouter

auth_routes=APIRouter(prefix="/auth",tags=["Autenticação"])

@auth_routes.get("/create")
async def autenticar():
    return {"message": "Usuario criado com sucesso!"}