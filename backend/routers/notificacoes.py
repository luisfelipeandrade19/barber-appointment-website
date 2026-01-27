from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Notificacao, Usuario, TipoUsuario
from schemas import NotificacaoRequest
from dependencies import get_db, get_current_user
from datetime import datetime

router = APIRouter(tags=["Notificações"])

@router.post('/api/notificacoes')
def criar_notificacao(data: NotificacaoRequest, db: Session = Depends(get_db)):
    db.add(Notificacao(id_cliente=data.id_cliente, mensagem=data.mensagem, lida=False, data_envio=datetime.now()))
    db.commit()
    return {"mensagem": "Notificação enviada"}

@router.get('/api/notificacoes')
def listar_notificacoes(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.CLIENTE: raise HTTPException(status_code=403, detail="Acesso negado")
    notificacoes = db.query(Notificacao).filter_by(id_cliente=current_user.id_usuario).all()
    return [{"id": n.id_notificacao, "mensagem": n.mensagem, "lida": n.lida, "data": n.data_envio} for n in notificacoes]