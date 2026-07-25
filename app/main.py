from fastapi import FastAPI
from app.database import engine, Base
from app.models import usuario, estudante, vinculo, codigo_vinculo, tarefa, execucao
from app.routers import estudante as estudante_router
from app.routers import usuario as usuario_router
from app.routers import vinculo as vinculo_router

app = FastAPI(title="TEA Rotina API")

app.include_router(estudante_router.router)
app.include_router(usuario_router.router)
app.include_router(vinculo_router.router)

@app.get("/")
def health_check():
    return {"status": "ok", "mensagem": "API da rotina TEA está rodando"}