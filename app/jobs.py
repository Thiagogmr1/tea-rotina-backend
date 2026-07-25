from datetime import date, timedelta
from app.database import SessionLocal
from app.models.tarefa import Tarefa
from app.models.execucao import Execucao, StatusExecucao

DIA_SEMANA_ABREV = {0: "seg", 1: "ter", 2: "qua", 3: "qui", 4: "sex", 5: "sab", 6: "dom"}


def marcar_tarefas_nao_realizadas(data_alvo: date | None = None) -> int:
    """
    Marca como 'não realizada' qualquer tarefa programada para 'data_alvo'
    (por padrão, ontem) que não teve execução registrada.
    Retorna quantas execuções foram criadas.
    """
    db = SessionLocal()
    try:
        alvo = data_alvo or (date.today() - timedelta(days=1))
        dia_abrev = DIA_SEMANA_ABREV[alvo.weekday()]

        tarefas = db.query(Tarefa).filter(Tarefa.ativo == True).all()
        tarefas_do_dia = [t for t in tarefas if dia_abrev in t.dias_semana]

        criadas = 0
        for tarefa in tarefas_do_dia:
            existe = db.query(Execucao).filter(
                Execucao.tarefa_id == tarefa.id,
                Execucao.data == alvo,
            ).first()
            if not existe:
                db.add(Execucao(tarefa_id=tarefa.id, data=alvo, status=StatusExecucao.nao_realizada))
                criadas += 1

        db.commit()
        return criadas
    finally:
        db.close()