from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Agendamento, Servico, AgendamentoServico, Usuario, TipoUsuario
from schemas import AgendamentoRequest, UpdateStatusRequest, UpdateBarbeiroRequest
from dependencies import get_db, get_current_user
from datetime import datetime, timedelta

router = APIRouter(tags=["Agendamentos"])

@router.post('/api/agendamentos', status_code=status.HTTP_201_CREATED)
def criar_agendamento(data: AgendamentoRequest, db: Session = Depends(get_db)):
    try:
        data_inicio = datetime.fromisoformat(data.data_hora)
        servicos_db = db.query(Servico).filter(Servico.id_servico.in_(data.servicos)).all()
        
        duracao_total = sum([s.duracao_estimada for s in servicos_db])
        valor_total = sum([s.preco for s in servicos_db])
        data_fim = data_inicio + timedelta(minutes=duracao_total)

        novo_agendamento = Agendamento(
            id_cliente=data.id_cliente,
            id_barbeiro=data.id_barbeiro,
            data_hora_inicio=data_inicio,
            data_hora_fim=data_fim,
            tempo_total_estimado=duracao_total,
            valor_total=valor_total
        )
        db.add(novo_agendamento)
        db.flush()

        for servico in servicos_db:
            db.add(AgendamentoServico(
                id_agendamento=novo_agendamento.id_agendamento,
                id_servico=servico.id_servico,
                preco_na_epoca=servico.preco
            ))
        db.commit()
        return {"mensagem": "Agendamento realizado com sucesso!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/api/agendamentos/{id_agendamento}/status')
def atualizar_status_agendamento(id_agendamento: int, data: UpdateStatusRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).get(id_agendamento)
    if not agendamento: raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    if current_user.id_usuario not in [agendamento.id_cliente, agendamento.id_barbeiro] and current_user.tipo != TipoUsuario.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso negado")

    agendamento.status = data.status
    if data.data_hora:
        novo_inicio = datetime.fromisoformat(data.data_hora)
        agendamento.data_hora_inicio = novo_inicio
        # Recalcula data fim mantendo a duração original
        agendamento.data_hora_fim = novo_inicio + timedelta(minutes=agendamento.tempo_total_estimado)
        
    db.commit()
    return {"mensagem": "Status atualizado"}

@router.put('/api/agendamentos/{id_agendamento}/barbeiro')
def atualizar_barbeiro_agendamento(id_agendamento: int, data: UpdateBarbeiroRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).get(id_agendamento)
    if not agendamento: raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    agendamento.id_barbeiro = data.id_barbeiro
    db.commit()
    return {"mensagem": "Barbeiro atualizado"}