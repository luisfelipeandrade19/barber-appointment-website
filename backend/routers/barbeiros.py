from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
from models import Barbeiro, Especialidade, Disponibilidade, Servico, Agendamento, Usuario, TipoUsuario, DisponibilidadeBarbeiro, TipoDisponibilidade, StatusAgendamento
from schemas import EspecialidadeRequest, DisponibilidadeRequest, ServicoRequest
from dependencies import get_db, get_current_user
from datetime import datetime

router = APIRouter(tags=["Barbeiros"])

@router.get('/api/barbeiros')
def listar_barbeiros(db: Session = Depends(get_db)):
    barbeiros = db.query(Barbeiro).filter_by(ativo=True).all()
    return [{
        "id": b.id_barbeiro,
        "nome": b.usuario.nome if b.usuario else "Desconhecido",
        "especialidade": b.especialidade,
        "especialidades": [{"id": e.id_especialidade, "nome": e.nome, "descricao": e.descricao} for e in b.especialidades] if hasattr(b, 'especialidades') else []
    } for b in barbeiros]

@router.get('/api/barbeiros/{id_barbeiro}/especialidades')
def listar_especialidades(id_barbeiro: int, db: Session = Depends(get_db)):
    barbeiro = db.query(Barbeiro).get(id_barbeiro)
    if not barbeiro: raise HTTPException(status_code=404, detail="Barbeiro não encontrado")
    return [{"id": e.id_especialidade, "nome": e.nome, "descricao": e.descricao} for e in barbeiro.especialidades] if hasattr(barbeiro, 'especialidades') else [{"nome": barbeiro.especialidade}]

@router.post('/api/barbeiros/especialidades')
def criar_especialidade(data: EspecialidadeRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.BARBEIRO: raise HTTPException(status_code=403, detail="Apenas barbeiros")
    db.add(Especialidade(id_barbeiro=current_user.id_usuario, nome=data.nome, descricao=data.descricao))
    db.commit()
    return {"mensagem": "Especialidade adicionada"}

@router.get('/api/barbeiros/{id_barbeiro}/disponibilidade')
def listar_disponibilidade(id_barbeiro: int, db: Session = Depends(get_db)):
    disponibilidades = db.query(DisponibilidadeBarbeiro).filter(
        DisponibilidadeBarbeiro.id_barbeiro == id_barbeiro
    ).all()

    # Buscar agendamentos ativos
    agendamentos = db.query(Agendamento).filter(
        Agendamento.id_barbeiro == id_barbeiro,
        Agendamento.status.notin_([StatusAgendamento.CANCELADO, StatusAgendamento.RECUSADO, StatusAgendamento.NAO_COMPARECEU])
    ).all()

    resultados = []
    for d in disponibilidades:
        # Combina data (Date) e hora_inicio (Time) para datetime
        slot_inicio = datetime.combine(d.data, d.hora_inicio)
        slot_fim = datetime.combine(d.data, d.hora_fim)
        
        ocupado = False
        for agendamento in agendamentos:
            # Verifica sobreposicao de horario
            # (SlotInicio < AgendamentoFim) E (SlotFim > AgendamentoInicio)
            if slot_inicio < agendamento.data_hora_fim and slot_fim > agendamento.data_hora_inicio:
                ocupado = True
                break
        
        if not ocupado:
            resultados.append({
                "id": d.id_disponibilidade,
                "inicio": slot_inicio.isoformat(), 
                "disponivel": True
            })
    return resultados

@router.post('/api/barbeiros/disponibilidade')
def criar_disponibilidade(data: DisponibilidadeRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.BARBEIRO: raise HTTPException(status_code=403, detail="Acesso negado")
    db.add(Disponibilidade(
        id_barbeiro=current_user.id_usuario,
        data_hora_inicio=datetime.fromisoformat(data.data_hora_inicio),
        data_hora_fim=datetime.fromisoformat(data.data_hora_fim),
        disponivel=data.disponivel
    ))
    db.commit()
    return {"mensagem": "Disponibilidade atualizada"}

@router.get('/api/barbeiros/financeiro')
def registro_financeiro(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.BARBEIRO: raise HTTPException(status_code=403, detail="Acesso negado")
    mes, ano = datetime.now().month, datetime.now().year
    agendamentos = db.query(Agendamento).filter(
        Agendamento.id_barbeiro == current_user.id_usuario,
        extract('month', Agendamento.data_hora_inicio) == mes,
        extract('year', Agendamento.data_hora_inicio) == ano
    ).all()
    
    # Calcula comissão (assumindo que o campo comissao no banco é porcentagem, ex: 50.00 para 50%)
    taxa_comissao = float(current_user.barbeiro.comissao) if current_user.barbeiro.comissao else 0.0
    total_bruto = sum([float(a.valor_total) for a in agendamentos])
    # Se tiver comissão definida usa ela, senão assume o total
    total_liquido = total_bruto * (taxa_comissao / 100) if taxa_comissao > 0 else total_bruto

    return {"mes": mes, "ano": ano, "total_ganhos": total_liquido, "quantidade_agendamentos": len(agendamentos)}

@router.get('/api/barbeiros/{id_barbeiro}/servicos')
def listar_servicos_barbeiro(id_barbeiro: int, db: Session = Depends(get_db)):
    return db.query(Servico).filter_by(id_barbeiro_criador=id_barbeiro).all()

@router.post('/api/barbeiros/servicos')
def criar_servico(data: ServicoRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.BARBEIRO: raise HTTPException(status_code=403, detail="Acesso negado")
    db.add(Servico(
        nome=data.nome,
        descricao=data.descricao,
        preco=data.preco,
        duracao_estimada=data.duracao_estimada,
        id_barbeiro_criador=current_user.id_usuario,
        ativo=True
    ))
    db.commit()
    return {"mensagem": "Serviço criado"}

@router.get('/api/barbeiros/agendamentos')
def listar_agendamentos_barbeiro(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.BARBEIRO: raise HTTPException(status_code=403, detail="Acesso negado")
    return db.query(Agendamento).filter_by(id_barbeiro=current_user.id_usuario).all()