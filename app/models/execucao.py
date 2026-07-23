import uuid
import enum
from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class StatusExecucao(str, enum.Enum):
    pendente = "pendente"
    concluida = "concluida"
    nao_realizada = "nao_realizada"

class Execucao(Base):
    __tablename__ = "execucoes"
    __table_args__ = (UniqueConstraint("tarefa_id", "data"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tarefa_id = Column(UUID(as_uuid=True), ForeignKey("tarefas.id", ondelete="CASCADE"), nullable=False)
    data = Column(Date, nullable=False)
    status = Column(Enum(StatusExecucao, name="status_execucao_enum", create_type=False), nullable=False, default=StatusExecucao.pendente)
    concluido_em = Column(DateTime(timezone=True))
    concluido_por_usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    criado_em = Column(DateTime(timezone=True), server_default=func.now())