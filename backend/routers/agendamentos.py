from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Agendamento, Servico, AgendamentoServico, Usuario, TipoUsuario, StatusAgendamento, Barbeiro
from schemas import AgendamentoRequest, UpdateStatusRequest, UpdateBarbeiroRequest
from dependencies import get_db, get_current_user
from datetime import datetime, timedelta

router = APIRouter(tags=["Agendamentos"])

@router.post('/api/agendamentos', status_code=status.HTTP_201_CREATED)
def criar_agendamento(data: AgendamentoRequest, db: Session = Depends(get_db)):
    try:
        # Validações de Integridade
        cliente = db.query(Usuario).filter(Usuario.id_usuario == data.id_cliente, Usuario.tipo == TipoUsuario.CLIENTE).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

        barbeiro = db.query(Barbeiro).filter(Barbeiro.id_barbeiro == data.id_barbeiro).first()
        if not barbeiro:
            raise HTTPException(status_code=404, detail="Barbeiro não encontrado.")

        data_inicio = datetime.fromisoformat(data.data_hora)
        servicos_db = db.query(Servico).filter(Servico.id_servico.in_(data.servicos)).all()
        if len(servicos_db) != len(data.servicos):
            raise HTTPException(status_code=400, detail="Um ou mais serviços solicitados não foram encontrados.")
        
        duracao_total = sum([s.duracao_estimada for s in servicos_db])
        valor_total = sum([s.preco for s in servicos_db])
        data_fim = data_inicio + timedelta(minutes=duracao_total)

        # Verifica se já existe agendamento no horário (exceto cancelados/recusados)
        conflito = db.query(Agendamento).filter(
            Agendamento.id_barbeiro == data.id_barbeiro,
            Agendamento.status.notin_([StatusAgendamento.CANCELADO, StatusAgendamento.RECUSADO]),
            Agendamento.data_hora_inicio < data_fim,
            Agendamento.data_hora_fim > data_inicio
        ).first()

        if conflito:
            raise HTTPException(status_code=409, detail="Horário indisponível. O barbeiro já possui um agendamento neste intervalo.")

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

    try:
        agendamento.status = StatusAgendamento(data.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Status inválido. Status permitidos: {[e.value for e in StatusAgendamento]}")
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
    
    novo_barbeiro = db.query(Barbeiro).get(data.id_barbeiro)
    if not novo_barbeiro:
        raise HTTPException(status_code=404, detail="Novo barbeiro não encontrado.")

    agendamento.id_barbeiro = data.id_barbeiro
    db.commit()
    return {"mensagem": "Barbeiro atualizado"}

@router.get('/api/agendamentos')
def listar_meus_agendamentos(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Agendamento)
    
    if current_user.tipo == TipoUsuario.CLIENTE:
        query = query.filter(Agendamento.id_cliente == current_user.id_usuario)
    elif current_user.tipo == TipoUsuario.BARBEIRO:
        query = query.filter(Agendamento.id_barbeiro == current_user.id_usuario)
    # Se for ADMIN, vê todos (ou poderíamos filtrar se quisesse)
    
    agendamentos = query.order_by(Agendamento.data_hora_inicio.desc()).all()
    
    resultados = []
    for a in agendamentos:
        # Formatar a resposta para facilitar o frontend
        # Precisamos do nome do barbeiro, contato, data, hora, servicos
        
        # Recuperar servicos
        servicos_nomes = [s.servico.nome for s in a.agendamento_servicos]
        servicos_str = ", ".join(servicos_nomes)
        
        resultados.append({
            "id": a.id_agendamento,
            "barberName": a.barbeiro.usuario.nome if a.barbeiro and a.barbeiro.usuario else "Desconhecido",
            "contact": a.barbeiro.usuario.telefone if a.barbeiro and a.barbeiro.usuario else "", # Assumindo telefone no usuario
            "date": a.data_hora_inicio.strftime("%d/%m/%Y"),
            "time": a.data_hora_inicio.strftime("%H:%Mh"),
            "services": servicos_str,
            "status": a.status.value, # Importante para saber se está cancelado
            # "image": ... (imagem do perfil não temos fácil agora, frontend pode usar default)
        })
        
    return resultados