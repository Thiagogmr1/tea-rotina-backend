from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import exigir_papel
from app.models.usuario import Usuario, PapelUsuario
from app.models.codigo_vinculo import CodigoVinculo
from app.models.vinculo import Vinculo, TipoVinculo
from app.schemas.vinculo import UsarCodigoRequest, VinculoResponse

router = APIRouter(prefix="/vinculos", tags=["Vínculos"])


@router.post("/usar-codigo", response_model=VinculoResponse, status_code=201)
def usar_codigo(
    dados: UsarCodigoRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_papel(PapelUsuario.responsavel)),
):
    codigo_vinculo = db.query(CodigoVinculo).filter(CodigoVinculo.codigo == dados.codigo).first()
    if not codigo_vinculo:
        raise HTTPException(status_code=404, detail="Código não encontrado")
    if codigo_vinculo.usado:
        raise HTTPException(status_code=400, detail="Código já foi utilizado")
    if codigo_vinculo.expira_em < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Código expirado")

    vinculo_existente = db.query(Vinculo).filter(
        Vinculo.usuario_id == usuario.id,
        Vinculo.estudante_id == codigo_vinculo.estudante_id,
    ).first()
    if vinculo_existente:
        raise HTTPException(status_code=400, detail="Usuário já vinculado a este estudante")

    vinculo = Vinculo(usuario_id=usuario.id, estudante_id=codigo_vinculo.estudante_id, tipo_vinculo=TipoVinculo.responsavel)
    db.add(vinculo)

    codigo_vinculo.usado = True
    codigo_vinculo.usado_por_usuario_id = usuario.id

    db.commit()
    db.refresh(vinculo)
    return vinculo