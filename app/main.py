from fastapi import FastAPI
from app.database import engine, Base
from app.models import usuario, estudante, vinculo, codigo_vinculo, tarefa, execucao

app = FastAPI(title="TEA Rotina API")

@app.get("/")
def health_check():
    return {"status": "ok", "mensagem": "API da rotina TEA está rodando"}