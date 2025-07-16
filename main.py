from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer



# Carrega variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_TOKEN=int(os.getenv("ACCESS_TOKEN_EXPIRE_TOKEN"))

# Cria a aplicação FastAPI
app = FastAPI()

oauth2_schema=OAuth2PasswordBearer(tokenUrl="auth/login-form")

# Importação das rotas
from src.routes.auth_routes import auth_routes
from src.routes.posts_routes import posts_routes

# Registro das rotas
app.include_router(auth_routes)
app.include_router(posts_routes)
