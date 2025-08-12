from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import pegar_sessao, verificar_token, verificar_admin
from ..models.models import Curso, Matricula, Aula, Frequencia, Usuario


cursos_router = APIRouter(
       prefix="/cursos",
       tags=["Cursos e Matrículas"],
       dependencies=[Depends(verificar_token)]
   )


@cursos_router.post("/criar")
async def criar_curso():
    

@cursos_router.get("/listar")
async def listar_curso():


@cursos_router.get("/{curso_id}/detalhes")
async def detalhar_curso():

@cursos_router.post("/matricular")
async def matricular_aluno(usuario_id:int,curso_id:int,session: Session= Depends(pegar_sessao)):
     # Verificar se já está matriculado
       # Criar nova matrícula

@cursos_router.get("{curso_id}/matricula")
async def listar_matriculas
    