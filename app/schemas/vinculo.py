import uuid
from pydantic import BaseModel, ConfigDict
from app.models.vinculo import TipoVinculo

class UsarCodigoRequest(BaseModel):
    codigo: str
    usuario_id: uuid.UUID

class VinculoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    usuario_id: uuid.UUID
    estudante_id: uuid.UUID
    tipo_vinculo: TipoVinculo
    ativo: bool