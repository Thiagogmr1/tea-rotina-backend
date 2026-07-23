import uuid
from sqlalchemy import Column, String, Date, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Estudante(Base):
    __tablename__ = "estudantes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(150), nullable=False)
    data_nascimento = Column(Date)
    ano_escolar = Column(String(20))
    observacoes = Column(Text)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())