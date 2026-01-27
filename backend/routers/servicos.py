from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Servico
from dependencies import get_db

router = APIRouter(tags=["Serviços"])

@router.get('/api/servicos')
def listar_servicos(db: Session = Depends(get_db)):
    servicos = db.query(Servico).filter_by(ativo=True).all()
    return [{
        "id": s.id_servico,
        "nome": s.nome,
        "descricao": s.descricao,
        "preco": float(s.preco),
        "duracao_estimada": s.duracao_estimada,
        "id_barbeiro": s.id_barbeiro_criador
    } for s in servicos]