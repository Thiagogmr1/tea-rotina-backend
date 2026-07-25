import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.usuario import PapelUsuario

class UsuarioCreate(BaseModel):
    nome: str
    papel: PapelUsuario
    telefone: Optional[str] = None
    cpf: Optional[str] = None

class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    nome: str
    papel: PapelUsuario
    telefone: Optional[str]