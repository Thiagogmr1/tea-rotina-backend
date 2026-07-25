import uuid
from datetime import time
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator
from app.models.tarefa import TipoTarefa

DIAS_VALIDOS = {"seg", "ter", "qua", "qui", "sex", "sab", "dom"}

class TarefaCreate(BaseModel):
    estudante_id: uuid.UUID
    titulo: str
    descricao: Optional[str] = None
    horario_previsto: time
    tipo: TipoTarefa = TipoTarefa.rotina_casa
    dias_semana: List[str]

    @field_validator("dias_semana")
    @classmethod
    def validar_dias(cls, valor: List[str]) -> List[str]:
        invalidos = set(valor) - DIAS_VALIDOS
        if invalidos:
            raise ValueError(f"Dias inválidos: {invalidos}. Use: {DIAS_VALIDOS}")
        if not valor:
            raise ValueError("Informe ao menos um dia da semana")
        return valor

class TarefaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    estudante_id: uuid.UUID
    titulo: str
    descricao: Optional[str]
    horario_previsto: time
    tipo: TipoTarefa
    dias_semana: List[str]
    ativo: bool