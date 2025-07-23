from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi import Form


class UsuarioSchema(BaseModel):
    nome:str
    email:str
    senha:str
    ativo:Optional[bool]
    admin:Optional[bool]

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    conteudo_texto: Optional[str]

    @classmethod
    def as_form(
        cls,
        conteudo_texto: Optional[str] = Form(None),
    ):
        return cls(conteudo_texto=conteudo_texto)


class PostResponse(BaseModel):
    id:int
    admin_id:int
    conteudo_texto:Optional[str]
    url_midia:Optional[str]
    data_criacao: datetime

    class Config:
        from_attributes = True
    
class LoginSchema(BaseModel):
    email:str
    senha:str

    class Config:
        from_attributes = True