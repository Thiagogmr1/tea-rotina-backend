from datetime import date as date_type, datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import exigir_papel
from app.models.estudante import Estudante
from app.models.usuario import Usuario, PapelUsuario
from app.models.vinculo import Vinculo
from app.models.tarefa import Tarefa
from app.models.execucao import Execucao, StatusExecucao
from app.schemas.execucao import TarefaDoDiaResponse, ConcluirTarefaRequest, ExecucaoResponse
from app.jobs import marcar_tarefas_nao_realizadas

router = APIRouter(tags=["Execuções"])

DIA_SEMANA_ABREV = {0: "seg", 1: "ter", 2: "qua", 3: "qui", 4: "sex", 5: "sab", 6: "dom"}


@router.get("/estudantes/{estudante_id}/tarefas-do-dia", response_model=List[TarefaDoDiaResponse])
def listar_tarefas_do_dia(
    estudante_id: str,
    data: Optional[date_type] = Query(default=None),
    db: Session = Depends(get_db),
):
    estudante = db.query(Estudante).filter(Estudante.id == estudante_id).first()
    if not estudante:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")

    data_consulta = data or datetime.now(timezone.utc).date()
    dia_abrev = DIA_SEMANA_ABREV[data_consulta.weekday()]

    tarefas = db.query(Tarefa).filter(Tarefa.estudante_id == estudante_id, Tarefa.ativo == True).all()
    tarefas_do_dia = [t for t in tarefas if dia_abrev in t.dias_semana]

    resultado = []
    for tarefa in tarefas_do_dia:
        execucao = db.query(Execucao).filter(
            Execucao.tarefa_id == tarefa.id, Execucao.data == data_consulta
        ).first()
        resultado.append(TarefaDoDiaResponse(
            tarefa_id=tarefa.id,
            titulo=tarefa.titulo,
            descricao=tarefa.descricao,
            horario_previsto=tarefa.horario_previsto,
            tipo=tarefa.tipo,
            status=execucao.status if execucao else StatusExecucao.pendente,
            execucao_id=execucao.id if execucao else None,
            concluido_em=execucao.concluido_em if execucao else None,
        ))

    resultado.sort(key=lambda t: t.horario_previsto)
    return resultado


@router.post("/execucoes/rodar-job-nao-realizadas")
def rodar_job_manualmente(
    data: Optional[date_type] = Query(default=None),
    usuario: Usuario = Depends(exigir_papel(PapelUsuario.gestor)),
):
    criadas = marcar_tarefas_nao_realizadas(data)
    return {"mensagem": f"{criadas} execuções marcadas como não realizada", "data_processada": str(data or "ontem")}


@router.post("/execucoes/concluir", response_model=ExecucaoResponse, status_code=201)
def concluir_tarefa(
    dados: ConcluirTarefaRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_papel(PapelUsuario.responsavel, PapelUsuario.aluno)),
):
    tarefa = db.query(Tarefa).filter(Tarefa.id == dados.tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    vinculo = db.query(Vinculo).filter(
        Vinculo.usuario_id == usuario.id,
        Vinculo.estudante_id == tarefa.estudante_id,
        Vinculo.ativo == True,
    ).first()
    if not vinculo:
        raise HTTPException(status_code=403, detail="Usuário não está vinculado a este estudante")

    data_execucao = dados.data or datetime.now(timezone.utc).date()

    execucao = db.query(Execucao).filter(
        Execucao.tarefa_id == dados.tarefa_id, Execucao.data == data_execucao
    ).first()
    if not execucao:
        execucao = Execucao(tarefa_id=dados.tarefa_id, data=data_execucao)
        db.add(execucao)

    execucao.status = StatusExecucao.concluida
    execucao.concluido_em = datetime.now(timezone.utc)
    execucao.concluido_por_usuario_id = usuario.id

    db.commit()
    db.refresh(execucao)
    return execucao