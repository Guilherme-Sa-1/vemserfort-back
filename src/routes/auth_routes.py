from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..models.models import Usuario
from ..dependencies import pegar_sessao,verificar_token
from src.utils.security import bcrypt_context
from main import ALGORITHM,ACCESS_TOKEN_EXPIRE_TOKEN,SECRET_KEY
from ..models.schemas import UsuarioSchema,LoginSchema
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime,timedelta,timezone

auth_routes=APIRouter(prefix="/auth",tags=["Autenticação"])

def criar_token(id_usuario,duracao_token= timedelta(minutes=ACCESS_TOKEN_EXPIRE_TOKEN)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        "sub": str(id_usuario), 
        "exp": int(data_expiracao.timestamp()) 
    }
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado



def autenticar_usuario(email,senha,session):
    usuario=session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha,usuario.senha):
        return False
    return usuario



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
    
   

@auth_routes.post("/login")
async def login(login_schema:LoginSchema,session:Session=Depends(pegar_sessao)):
    usuario=autenticar_usuario(login_schema.email,login_schema.senha,session)
    if not usuario:
        raise HTTPException(status_code=400,detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token=criar_token(usuario.id)
        refresh_token=criar_token(usuario.id,duracao_token=timedelta(days=10))
        return{
            "access_token":access_token,
            "refresh_token":refresh_token,
            "token_type":"Bearer"
            }
    
@auth_routes.post("/login-form")
async def login_form(dados_formulario:OAuth2PasswordRequestForm= Depends(),session:Session=Depends(pegar_sessao)):
    usuario=autenticar_usuario(dados_formulario.username,dados_formulario.password,session)
    if not usuario:
        raise HTTPException(status_code=400,detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token=criar_token(usuario.id)
        return{
            "access_token":access_token,
            "token_type":"Bearer"
            }

@auth_routes.get("/refresh")
async def use_refresh_token(usuario:Usuario=Depends(verificar_token)):
    access_token=criar_token(usuario.id)
    return{
            "access_token":access_token,
            "token_type":"Bearer"
            }