from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

db = create_engine("sqlite:///banco.db")

Base = declarative_base()

# Usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    # Relacionamento para acessar as matrículas de um usuário
    matriculas = relationship("Matricula", back_populates="usuario")
    # Relacionamento para acessar os registros de frequência de um usuário
    frequencias = relationship("Frequencia", back_populates="usuario")

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

# Cursos
class Curso(Base):
    __tablename__ = "cursos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    professor = Column("professor", String)

    # Relacionamentos para acessar as matrículas e aulas de um curso
    matriculas = relationship("Matricula", back_populates="curso")
    aulas = relationship("Aula", back_populates="curso", order_by="Aula.data_aula") # Ordene as aulas por data

    def __init__(self, nome, professor):
        self.nome = nome
        self.professor = professor


# Tabela de Matrícula
class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    curso_id = Column("curso_id", Integer, ForeignKey("cursos.id"), nullable=False)
    data_matricula = Column("data_matricula", DateTime, default=datetime.now)
    status = Column("status", String, default="Ativa")

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="matriculas")
    curso = relationship("Curso", back_populates="matriculas")

    def __init__(self, usuario_id, curso_id, status="Ativa"):
        self.usuario_id = usuario_id
        self.curso_id = curso_id
        self.status = status

class Aula(Base):
    __tablename__ = "aulas"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    curso_id = Column("curso_id", Integer, ForeignKey("cursos.id"), nullable=False)
    titulo = Column("titulo", String, nullable=False)
    data_aula = Column("data_aula", DateTime, nullable=False)
    descricao = Column("descricao", String)
    link_forms_frequencia = Column("link_forms_frequencia", String) # Link para o Forms daquela aula

    # Relacionamentos
    curso = relationship("Curso", back_populates="aulas")
    frequencias = relationship("Frequencia", back_populates="aula")

    def __init__(self, curso_id, titulo, data_aula, descricao=None, link_forms_frequencia=None):
        self.curso_id = curso_id
        self.titulo = titulo
        self.data_aula = data_aula
        self.descricao = descricao
        self.link_forms_frequencia = link_forms_frequencia

# Tabela de Frequência
class Frequencia(Base):
    __tablename__ = "frequencias"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    aula_id = Column("aula_id", Integer, ForeignKey("aulas.id"), nullable=False)
    data_registro = Column("data_registro", DateTime, default=datetime.now)
    presente = Column("presente", Boolean, default=True)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="frequencias")
    aula = relationship("Aula", back_populates="frequencias")

    def __init__(self, usuario_id, aula_id, presente=True):
        self.usuario_id = usuario_id
        self.aula_id = aula_id
        self.presente = presente
