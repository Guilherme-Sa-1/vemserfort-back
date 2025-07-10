from fastapi import APIRouter, Depends
from ..models.models import Usuario
from ..dependencies import pegar_sessão

auth_routes=APIRouter(prefix="/auth",tags=["Autenticação"])

@auth_routes.get("/create")
async def home():
    return {"message": "Usuario criado com sucesso!"}


@auth_routes.post("/criar_conta")
async def criar_conta(nome:str,email:str,senha:str,session=Depends(pegar_sessão)):
    
    usuario= session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:

        return{"Mensagem":"Ja existe um usuário com este e-mail"  }
    else:
        novo_usuario=Usuario(nome,email,senha)
        session.add(novo_usuario)
        session.commit()
        return{"Mensagem":"Usuario cadastrado com sucesso"}
    
   