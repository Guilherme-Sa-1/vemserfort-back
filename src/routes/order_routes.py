from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import pegar_sessao
from ..models.schemas import PedidoSChema

order_routes=APIRouter(prefix="/order",tags=["Home"])

@order_routes.post("/post")
async def create_post(post_schema:PostSchema,session:Session=Depends(pegar_sessao)):
    return {"message": "Postagem criada com sucesso!"}

