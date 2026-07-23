import uuid
import enum
from sqlalchemy import Column, String, Text, Time, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from app.database import Base

class TipoTarefa(str, enum.Enum):
    rotina_casa = "rotina_casa"
    dever = "dever"

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estudante_id = Column(UUID(as_uuid=True), ForeignKey("estudantes.id", ondelete="CASCADE"), nullable=False)
    criado_por_usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    titulo = Column(String(150), nullable=False)
    descricao = Column(Text)
    horario_previsto = Column(Time, nullable=False)
    tipo = Column(Enum(TipoTarefa, name="tipo_tarefa_enum", create_type=False), nullable=False, default=TipoTarefa.rotina_casa)
    dias_semana = Column(ARRAY(String), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())