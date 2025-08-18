from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import pegar_sessao, verificar_token, verificar_admin
from ..models.models import Curso, Matricula, Aula, Frequencia, Usuario


cursos_router = APIRouter(
       prefix="/cursos",
       tags=["Cursos e Matrículas"],
       dependencies=[Depends(verificar_token)]
   )


# Rota de criação de curso
@cursos_router.post("/criar",status_code=status.HTTP_201_CREATED,response_model=CursoResponse)
async def criar_curso(
    curso: CursoCreate,
    session: Session = Depends(pegar_sessao),
    admin: Usuario = Depends(verificar_admin)
):
    novo_curso = Curso(
        nome=curso.nome,
        professor=curso.professor,
        descricao=curso.descricao,
        carga_horaria=curso.carga_horaria,
        data_inicio=curso.data_inicio,
        data_termino=curso.data_termino,
        total_aulas=curso.total_aulas
    )

    session.add(novo_curso)
    session.commit()
    session.refresh(novo_curso)
    return novo_curso

# Rota de listagem de cursos
@cursos_router.get("/listar", response_model=List[CursoListagemResponse])

# Rota de detalhes do curso
@cursos_router.get("/{curso_id}/detalhes", response_model=CursoDetalhesResponse)

# Rota de matrícula
@cursos_router.post("/matricular", response_model=MatriculaResponse)

# Rota de listagem de matrículas
@cursos_router.get("/{curso_id}/matriculas", response_model=List[MatriculaSchema])