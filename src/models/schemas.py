from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from fastapi import Form

# --------------------- USUÁRIO ---------------------
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

# --------------------- LOGIN ---------------------
class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

# --------------------- POSTS ---------------------
class PostCreate(BaseModel):
    conteudo_texto: Optional[str]

    @classmethod
    def as_form(cls, conteudo_texto: Optional[str] = Form(None)):
        return cls(conteudo_texto=conteudo_texto)

class PostResponse(BaseModel):
    id: int
    admin_id: int
    conteudo_texto: Optional[str]
    url_midia: Optional[str]
    data_criacao: datetime

    class Config:   
        from_attributes = True

# --------------------- MATRÍCULAS ---------------------
class MatriculaSchema(BaseModel):
    id_matricula: int
    id_usuario: int
    id_curso: int
    data_matricula: datetime
    status: str

    class Config:
        from_attributes = True

class MatriculaResponse(BaseModel):
    mensagem: str
    id_matricula: int

    class Config:
        from_attributes = True

# --------------------- CURSOS ---------------------
class CursoCreate(BaseModel):
    nome: str
    professor: str
    descricao: str
    carga_horaria: int
    data_inicio: datetime
    data_termino: datetime
    total_aulas: int

class CursoResponse(BaseModel):
    id_curso: int
    nome: str
    professor: str
    descricao: str
    carga_horaria: int
    data_inicio: datetime
    data_termino: datetime
    total_aulas: int

    class Config:
        from_attributes = True

class CursoListagemResponse(BaseModel):
    id_curso: int
    nome: str
    professor: str
    total_matriculas: int

    class Config:
        from_attributes = True

class CursoDetalhesResponse(CursoResponse):
    matriculas: List[MatriculaSchema] = []
    total_matriculas: int = 0

    class Config:
        from_attributes = True

# --------------------- AULAS ---------------------
class AulaCreate(BaseModel):
    titulo: str
    data: datetime
    curso_id: int

# --------------------- FREQUÊNCIA ---------------------
class CursoFrequencia(BaseModel):
    curso: str
    presencas: int
    total_aulas: int

    class Config:
        from_attributes = True

class AlunoFrequencia(BaseModel):
    usuario_id: int
    nome: str
    frequencias: List[CursoFrequencia]

    class Config:
        from_attributes = True