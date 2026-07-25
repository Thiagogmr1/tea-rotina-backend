import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.usuario import PapelUsuario

class UsuarioCreate(BaseModel):
    nome: str
    papel: PapelUsuario
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    senha: str  # senha pura, será hasheada antes de salvar

class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    nome: str
    papel: PapelUsuario
    telefone: Optional[str]

class LoginRequest(BaseModel):
    telefone: str
    senha: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse