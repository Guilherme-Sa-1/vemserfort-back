from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UsuarioSchema(BaseModel):
    nome:str
    email:str
    senha:str
    ativo:Optional[bool]
    admin:Optional[bool]

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    conteudo_texto:Optional[str]


class PostResponse(BaseModel):
    id:int
    admin_id:int
    conteudo_texto:Optional[str]
    url_midia:Optional[str]
    data_criacao: datetime

    class Config:
        from_attributes=True
    