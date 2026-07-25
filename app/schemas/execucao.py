import uuid
from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.tarefa import TipoTarefa
from app.models.execucao import StatusExecucao

class TarefaDoDiaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tarefa_id: uuid.UUID
    titulo: str
    descricao: Optional[str]
    horario_previsto: time
    tipo: TipoTarefa
    status: StatusExecucao
    execucao_id: Optional[uuid.UUID] = None
    concluido_em: Optional[datetime] = None

class ConcluirTarefaRequest(BaseModel):
    tarefa_id: uuid.UUID
    concluido_por_usuario_id: uuid.UUID
    data: Optional[date] = None  # se não informado, assume hoje

class ExecucaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    tarefa_id: uuid.UUID
    data: date
    status: StatusExecucao
    concluido_em: Optional[datetime]
    concluido_por_usuario_id: Optional[uuid.UUID]