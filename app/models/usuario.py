import uuid
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import enum

class PapelUsuario(str, enum.Enum):
    professor_sala = "professor_sala"
    professor_aee = "professor_aee"
    gestor = "gestor"
    responsavel = "responsavel"
    aluno = "aluno"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(150), nullable=False)
    papel = Column(Enum(PapelUsuario, name="papel_usuario", create_type=False), nullable=False)
    telefone = Column(String(20))
    cpf = Column(String(14))
    senha_hash = Column(String(255))
    criado_em = Column(DateTime(timezone=True), server_default=func.now())