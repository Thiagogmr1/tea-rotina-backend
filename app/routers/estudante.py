import random
import string
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import exigir_papel
from app.models.estudante import Estudante
from app.models.usuario import Usuario, PapelUsuario
from app.models.vinculo import Vinculo, TipoVinculo
from app.models.codigo_vinculo import CodigoVinculo
from app.schemas.estudante import EstudanteCreate, EstudanteCreateResponse, EstudanteResponse

router = APIRouter(prefix="/estudantes", tags=["Estudantes"])


def gerar_codigo(tamanho: int = 6) -> str:
    caracteres = string.ascii_uppercase + string.digits
    return "".join(random.choices(caracteres, k=tamanho))


@router.post("", response_model=EstudanteCreateResponse, status_code=201)
def criar_estudante(
    dados: EstudanteCreate,
    db: Session = Depends(get_db),
    professor: Usuario = Depends(exigir_papel(
        PapelUsuario.professor_sala, PapelUsuario.professor_aee, PapelUsuario.gestor
    )),
):
    estudante = Estudante(
        nome=dados.nome,
        data_nascimento=dados.data_nascimento,
        ano_escolar=dados.ano_escolar,
        observacoes=dados.observacoes,
    )
    db.add(estudante)
    db.flush()

    vinculo_professor = Vinculo(
        usuario_id=professor.id,
        estudante_id=estudante.id,
        tipo_vinculo=TipoVinculo(professor.papel.value),
    )
    db.add(vinculo_professor)

    codigo = gerar_codigo()
    tentativas = 0
    while db.query(CodigoVinculo).filter(CodigoVinculo.codigo == codigo).first():
        codigo = gerar_codigo()
        tentativas += 1
        if tentativas > 5:
            raise Exception("Erro ao gerar código único")

    expira_em = datetime.now(timezone.utc) + timedelta(days=7)
    codigo_vinculo = CodigoVinculo(estudante_id=estudante.id, codigo=codigo, expira_em=expira_em)
    db.add(codigo_vinculo)

    db.commit()
    db.refresh(estudante)

    return EstudanteCreateResponse(
        estudante=EstudanteResponse.model_validate(estudante),
        codigo_vinculo=codigo,
        expira_em=expira_em.isoformat(),
    )