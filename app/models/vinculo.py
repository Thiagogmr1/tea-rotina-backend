import uuid
import enum
from sqlalchemy import Column, Boolean, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class TipoVinculo(str, enum.Enum):
    professor_sala = "professor_sala"
    professor_aee = "professor_aee"
    gestor = "gestor"
    responsavel = "responsavel"
    aluno_titular = "aluno_titular"

class Vinculo(Base):
    __tablename__ = "vinculos"
    __table_args__ = (UniqueConstraint("usuario_id", "estudante_id"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    estudante_id = Column(UUID(as_uuid=True), ForeignKey("estudantes.id", ondelete="CASCADE"), nullable=False)
    tipo_vinculo = Column(Enum(TipoVinculo, name="tipo_vinculo_enum", create_type=False), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())