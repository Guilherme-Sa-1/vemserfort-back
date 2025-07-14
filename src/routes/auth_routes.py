from fastapi import APIRouter, Depends, HTTPException
from ..models.models import Usuario
from ..dependencies import pegar_sessao
from src.utils.security import bcrypt_context
from ..models.schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_routes=APIRouter(prefix="/auth",tags=["Autenticação"])

@auth_routes.get("/create")
async def home():
    return {"message": "Usuario criado com sucesso!"}


@auth_routes.post("/criar_conta")
async def criar_conta(usuario_schema:UsuarioSchema,session:Session=Depends(pegar_sessao)):
    
    usuario= session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:

        raise HTTPException(status_code=400,detail="E-mail de usuário já cadastrado.")
    else:
        senha_criptografada=bcrypt_context.hash(usuario_schema.senha)
        novo_usuario=Usuario(usuario_schema.nome,usuario_schema.email,senha_criptografada,usuario_schema.ativo,usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return{"Mensagem":f"Usuario cadastrado com sucesso: {usuario_schema.email}"}
    
   