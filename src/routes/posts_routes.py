from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List,Optional
from ..dependencies import pegar_sessao,verificar_token
from ..models.models import Post
from ..models.schemas import PostResponse,PostCreate
from datetime import datetime
import os

posts_routes = APIRouter(prefix="/posts", tags=["Posts"],)

UPLOAD_DIR = "src/uploads" 

@posts_routes.get("/listar_posts", response_model=List[PostResponse])
async def listar_posts(session: Session = Depends(pegar_sessao)):
    posts = session.query(Post).order_by(desc(Post.data_criacao)).all()
    return posts


@posts_routes.post("/criar_post")
async def criar_post(
    dados: PostCreate = Depends(PostCreate.as_form),
    arquivo: Optional[UploadFile] = File(None),
    session: Session = Depends(pegar_sessao),
    usuario=Depends(verificar_token)
):
    
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem criar posts.")

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
        admin_id=usuario.id,
        conteudo_texto=dados.conteudo_texto,
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


@posts_routes.delete("/deletar/{post_id}")
async def deletar_post(
    post_id: int,
    session: Session = Depends(pegar_sessao),
    usuario = Depends(verificar_token)
):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem deletar posts.")

    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado.")
    
    if post.url_midia and os.path.exists(post.url_midia):
        os.remove(post.url_midia)

    session.delete(post)
    session.commit()
    return {"mensagem": "Post deletado com sucesso."}
