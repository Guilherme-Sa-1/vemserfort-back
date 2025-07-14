from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import pegar_sessao
from ..models.models import Post
from ..models.schemas import PostResponse  # Certifique-se de ter isso no schemas.py
from datetime import datetime
import os
from typing import Optional

posts_routes = APIRouter(prefix="/posts", tags=["Home"])

UPLOAD_DIR = "src/uploads"  # A pasta deve existir ou será criada

@posts_routes.post("/criar")
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

@posts_routes.get("/", response_model=list[PostResponse])
async def listar_posts(session: Session = Depends(pegar_sessao)):
    posts = session.query(Post).order_by(Post.data_criacao.desc()).all()
    return posts
