from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.estudante import Estudante
from app.models.usuario import Usuario, PapelUsuario
from app.models.tarefa import Tarefa
from app.schemas.tarefa import TarefaCreate, TarefaResponse

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])

PAPEIS_QUE_PODEM_CRIAR_TAREFA = {PapelUsuario.professor_sala, PapelUsuario.professor_aee}


@router.post("", response_model=TarefaResponse, status_code=201)
def criar_tarefa(dados: TarefaCreate, db: Session = Depends(get_db)):
    estudante = db.query(Estudante).filter(Estudante.id == dados.estudante_id).first()
    if not estudante:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")

    professor = db.query(Usuario).filter(Usuario.id == dados.criado_por_usuario_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if professor.papel not in PAPEIS_QUE_PODEM_CRIAR_TAREFA:
        raise HTTPException(
            status_code=403,
            detail="Apenas professores podem criar tarefas. Responsáveis não têm permissão para isso no MVP."
        )

    tarefa = Tarefa(
        estudante_id=dados.estudante_id,
        criado_por_usuario_id=dados.criado_por_usuario_id,
        titulo=dados.titulo,
        descricao=dados.descricao,
        horario_previsto=dados.horario_previsto,
        tipo=dados.tipo,
        dias_semana=dados.dias_semana,
    )
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa