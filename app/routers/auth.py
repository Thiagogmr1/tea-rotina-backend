from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import LoginRequest, LoginResponse
from app.security import verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=LoginResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.telefone == dados.telefone).first()

    if not usuario or not usuario.senha_hash or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Telefone ou senha incorretos")

    token = criar_token(usuario.id, usuario.papel.value)
    return LoginResponse(access_token=token, usuario=usuario)