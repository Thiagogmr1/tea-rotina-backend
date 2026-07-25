import uuid
from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class EstudanteCreate(BaseModel):
    nome: str
    data_nascimento: Optional[date] = None
    ano_escolar: Optional[str] = None
    observacoes: Optional[str] = None

class EstudanteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    nome: str
    data_nascimento: Optional[date]
    ano_escolar: Optional[str]
    observacoes: Optional[str]

class EstudanteCreateResponse(BaseModel):
    estudante: EstudanteResponse
    codigo_vinculo: str
    expira_em: str