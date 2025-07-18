from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import pegar_sessao,verificar_token
from ..models.models import Post
from ..models.schemas import PostResponse  # Certifique-se de ter isso no schemas.py
from datetime import datetime
import os
from typing import Optional

posts_routes = APIRouter(prefix="/posts", tags=["Posts"],dependencies=[Depends(verificar_token)])

UPLOAD_DIR = "src/uploads" 

@posts_routes.post("/criar_post")
async def criar_post(
    conteudo_texto: str = Form(...),
    arquivo: Optional[UploadFile] = File(None),
    session: Session = Depends(pegar_sessao)
):
    # Simulação de admin_id (idealmente isso virá do token futuramente)
    admin_id = 6

    url_arquivo = None

    # Se foi enviado um arquivo
    if arquivo:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Cria um nome único pro arquivo
        nome_arquivo = f"{datetime.now().timestamp()}_{arquivo.filename}"
        caminho_completo = os.path.join(UPLOAD_DIR, nome_arquivo)

        # Salva o arquivo
        with open(caminho_completo, "wb") as buffer:
            buffer.write(await arquivo.read())

        # Caminho relativo para salvar no banco
        url_arquivo = caminho_completo

    # Cria o post no banco
    novo_post = Post(
        admin_id=admin_id,
        conteudo_texto=conteudo_texto,
        url_midia=url_arquivo
    )
    session.add(novo_post)
    session.commit()
    session.refresh(novo_post)

    return {
        "mensagem": "Post criado com sucesso!",
        "id": novo_post.id,
        "conteudo": novo_post.conteudo_texto,
        "url_midia": novo_post.url_midia
    }

@posts_routes.get("/listar_posts", response_model=list[PostResponse])
async def listar_posts(session: Session = Depends(pegar_sessao)):
    posts = session.query(Post).order_by(Post.data_criacao.desc()).all()
    return posts

@posts_routes.post("/deletar/{post_id}")
async def deletar_post(post_id:int,session:Session=Depends(pegar_sessao)):
    post=session.query(Post).filter(Post.id==post_id).first()

    if not post:
        raise HTTPException(status_code=404,detail="Post não encontrado")
    
    if post.url_midia and os.path.exists(post.url_midia):
        os.remove(post.url_midia)

    session.delete(post)
    session.commit()

    return{"Mensagem":"Post deletado com suscesso!"}
