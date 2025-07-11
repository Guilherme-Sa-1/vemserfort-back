from fastapi import APIRouter, Depends, HTTPException
from ..models.models import Usuario
from ..dependencies import pegar_sessão
from src.utils.security import bcrypt_context

auth_routes=APIRouter(prefix="/auth",tags=["Autenticação"])

@auth_routes.get("/create")
async def home():
    return {"message": "Usuario criado com sucesso!"}


@auth_routes.post("/criar_conta")
async def criar_conta(nome:str,email:str,senha:str,session=Depends(pegar_sessão)):
    
    usuario= session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:

        raise HTTPException(status_code=400,detail="E-mail de usuário já cadastrado.")
    else:
        senha_criptografada=bcrypt_context.hash(senha)
        novo_usuario=Usuario(nome,email,senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return{"Mensagem":f"Usuario cadastrado com sucesso: {email}"}
    
   