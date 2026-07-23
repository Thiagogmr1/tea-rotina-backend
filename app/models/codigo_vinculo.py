import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class CodigoVinculo(Base):
    __tablename__ = "codigos_vinculo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estudante_id = Column(UUID(as_uuid=True), ForeignKey("estudantes.id", ondelete="CASCADE"), nullable=False)
    codigo = Column(String(10), nullable=False, unique=True)
    expira_em = Column(DateTime(timezone=True), nullable=False)
    usado = Column(Boolean, nullable=False, default=False)
    usado_por_usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    criado_em = Column(DateTime(timezone=True), server_default=func.now())