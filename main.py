from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Cria a aplicação FastAPI
app = FastAPI()

# Importação das rotas
from src.routes.auth_routes import auth_routes
from src.routes.posts_routes import posts_routes

# Registro das rotas
app.include_router(auth_routes)
app.include_router(posts_routes)
