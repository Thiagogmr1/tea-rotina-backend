from fastapi import FastAPI
from app.database import engine, Base
from app.models import usuario, estudante, vinculo, codigo_vinculo, tarefa, execucao
from app.routers import estudante as estudante_router
from app.routers import usuario as usuario_router
from app.routers import vinculo as vinculo_router
from app.routers import tarefa as tarefa_router
from app.routers import execucao as execucao_router
from app.routers import auth as auth_router

app = FastAPI(title="TEA Rotina API")

app.include_router(estudante_router.router)
app.include_router(usuario_router.router)
app.include_router(vinculo_router.router)
app.include_router(tarefa_router.router)
app.include_router(execucao_router.router)
app.include_router(auth_router.router)

@app.get("/")
def health_check():
    return {"status": "ok", "mensagem": "API da rotina TEA está rodando"}