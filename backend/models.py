from datetime import datetime, date, time
from decimal import Decimal
import os
from sqlalchemy import func, create_engine, Enum, Text, Date, Time, DECIMAL, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis do arquivo .env

Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://postgres:1605@localhost:5432/barbersystem'))
_Session = sessionmaker(bind=engine)

# Enums
class TipoUsuario(PyEnum):
    CLIENTE = 'cliente'
    BARBEIRO = 'barbeiro'
    ADMIN = 'admin'

class StatusAgendamento(PyEnum):
    PENDENTE = 'pendente'
    CONFIRMADO = 'confirmado'
    RECUSADO = 'recusado'
    CANCELADO = 'cancelado'
    CONCLUIDO = 'concluido'
    NAO_COMPARECEU = 'nao_compareceu'

class TipoDisponibilidade(PyEnum):
    DISPONIVEL = 'disponivel'
    FOLGA = 'folga'
    FERIAS = 'ferias'
    MANUTENCAO = 'manutencao'

class TipoNotificacao(PyEnum):
    CONFIRMACAO = 'confirmacao'
    CANCELAMENTO = 'cancelamento'
    REAGENDAMENTO = 'reagendamento'
    LEMBRETE = 'lembrete'

class CanalNotificacao(PyEnum):
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push'

class StatusEnvio(PyEnum):
    PENDENTE = 'pendente'
    ENVIADO = 'enviado'
    FALHA = 'falha'

class TipoRegistroFinanceiro(PyEnum):
    SERVICO = 'servico'
    COMISSAO = 'comissao'

# Entidades
class Usuario(Base):
    __tablename__ = "usuario"
    
    id_usuario = Column(Integer, primary_key=True)
    tipo = Column(Enum(TipoUsuario), nullable=False)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    senha_hash = Column(String(255), nullable=False)
    data_cadastro = Column(DateTime, server_default=func.now())
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="usuario", cascade="all, delete-orphan", uselist=False)
    barbeiro = relationship("Barbeiro", back_populates="usuario", cascade="all, delete-orphan", uselist=False)

class Cliente(Base):
    __tablename__ = "cliente"
    
    id_cliente = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
    preferencias = Column(Text, nullable=True)
    data_ultima_visita = Column(DateTime, nullable=True)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="cliente")
    agendamentos = relationship("Agendamento", back_populates="cliente")
    historicos = relationship("HistoricoServico", back_populates="cliente")

class Barbeiro(Base):
    __tablename__ = "barbeiro"
    
    id_barbeiro = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
    especialidade = Column(String(100), nullable=True)
    ativo = Column(Boolean, default=True)
    comissao = Column(DECIMAL(5, 2), default=Decimal('0.00'))
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="barbeiro")
    servicos_criados = relationship("Servico", back_populates="barbeiro_criador")
    agendamentos = relationship("Agendamento", back_populates="barbeiro")
    disponibilidades = relationship("DisponibilidadeBarbeiro", back_populates="barbeiro")
    historicos = relationship("HistoricoServico", back_populates="barbeiro")
    registros_financeiros = relationship("RegistroFinanceiro", back_populates="barbeiro")
    especialidades = relationship("Especialidade", back_populates="barbeiro")

class Servico(Base):
    __tablename__ = "servico"
    
    id_servico = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    duracao_estimada = Column(Integer, nullable=False)  # em minutos
    preco = Column(DECIMAL(10, 2), nullable=False)
    ativo = Column(Boolean, default=True)
    id_barbeiro_criador = Column(Integer, ForeignKey('barbeiro.id_barbeiro'), nullable=True)
    data_criacao = Column(DateTime, server_default=func.now())
    
    # Relacionamentos
    barbeiro_criador = relationship("Barbeiro", back_populates="servicos_criados")
    agendamento_servicos = relationship("AgendamentoServico", back_populates="servico")

class Agendamento(Base):
    __tablename__ = "agendamento"
    
    id_agendamento = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    id_barbeiro = Column(Integer, ForeignKey('barbeiro.id_barbeiro'), nullable=False)
    data_hora_inicio = Column(DateTime, nullable=False)
    data_hora_fim = Column(DateTime, nullable=False)
    status = Column(Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE)
    tempo_total_estimado = Column(Integer, nullable=False)  # em minutos
    valor_total = Column(DECIMAL(10, 2), nullable=False)
    observacoes = Column(Text, nullable=True)
    data_criacao = Column(DateTime, server_default=func.now())
    data_ultima_atualizacao = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="agendamentos")
    barbeiro = relationship("Barbeiro", back_populates="agendamentos")
    agendamento_servicos = relationship("AgendamentoServico", back_populates="agendamento", cascade="all, delete-orphan")
    notificacoes = relationship("Notificacao", back_populates="agendamento")
    historicos = relationship("HistoricoServico", back_populates="agendamento")
    registros_financeiros = relationship("RegistroFinanceiro", back_populates="agendamento")

class AgendamentoServico(Base):
    __tablename__ = "agendamento_servico"
    
    id_agendamento_servico = Column(Integer, primary_key=True)
    id_agendamento = Column(Integer, ForeignKey('agendamento.id_agendamento'), nullable=False)
    id_servico = Column(Integer, ForeignKey('servico.id_servico'), nullable=False)
    preco_na_epoca = Column(DECIMAL(10, 2), nullable=False)
    observacoes = Column(Text, nullable=True)
    
    # Relacionamentos
    agendamento = relationship("Agendamento", back_populates="agendamento_servicos")
    servico = relationship("Servico", back_populates="agendamento_servicos")

class DisponibilidadeBarbeiro(Base):
    __tablename__ = "disponibilidade_barbeiro"
    
    id_disponibilidade = Column(Integer, primary_key=True)
    id_barbeiro = Column(Integer, ForeignKey('barbeiro.id_barbeiro'), nullable=False)
    data = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    tipo = Column(Enum(TipoDisponibilidade), default=TipoDisponibilidade.DISPONIVEL)
    recorrente = Column(Boolean, default=False)
    
    # Relacionamentos
    barbeiro = relationship("Barbeiro", back_populates="disponibilidades")

class Notificacao(Base):
    __tablename__ = "notificacao"
    
    id_notificacao = Column(Integer, primary_key=True)
    id_agendamento = Column(Integer, ForeignKey('agendamento.id_agendamento'), nullable=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=True)
    tipo = Column(Enum(TipoNotificacao), nullable=True)
    canal = Column(Enum(CanalNotificacao), nullable=True)
    destinatario = Column(String(255), nullable=True)
    mensagem = Column(Text, nullable=True)
    data_envio = Column(DateTime, nullable=False)
    status_envio = Column(Enum(StatusEnvio), default=StatusEnvio.PENDENTE)
    tentativas = Column(Integer, default=0)
    lida = Column(Boolean, default=False)
    
    # Relacionamentos
    agendamento = relationship("Agendamento", back_populates="notificacoes")
    cliente = relationship("Cliente")

class Especialidade(Base):
    __tablename__ = "especialidade"
    
    id_especialidade = Column(Integer, primary_key=True)
    id_barbeiro = Column(Integer, ForeignKey('barbeiro.id_barbeiro'), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    
    barbeiro = relationship("Barbeiro", back_populates="especialidades")

class Preferencia(Base):
    __tablename__ = "preferencia"
    
    id_preferencia = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    descricao = Column(Text, nullable=False)
    
    cliente = relationship("Cliente")

class Disponibilidade(Base):
    __tablename__ = "disponibilidade"
    
    id_disponibilidade = Column(Integer, primary_key=True)
    id_barbeiro = Column(Integer, ForeignKey('barbeiro.id_barbeiro'), nullable=False)
    data_hora_inicio = Column(DateTime, nullable=False)
    data_hora_fim = Column(DateTime, nullable=False)
    disponivel = Column(Boolean, default=True)

class HistoricoServico(Base):
    __tablename__ = "historico_servico"
    
    id_historico = Column(Integer, primary_key=True)
    id_agendamento = Column(Integer, ForeignKey('agendamento.id_agendamento'), nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    id_barbeiro = Column(Integer, ForeignKey('barbeiro.id_barbeiro'), nullable=False)
    data_servico = Column(DateTime, nullable=False)
    servicos_realizados = Column(Text, nullable=False)
    valor_total = Column(DECIMAL(10, 2), nullable=False)
    observacoes = Column(Text, nullable=True)
    
    # Relacionamentos
    agendamento = relationship("Agendamento", back_populates="historicos")
    cliente = relationship("Cliente", back_populates="historicos")
    barbeiro = relationship("Barbeiro", back_populates="historicos")

class RegistroFinanceiro(Base):
    __tablename__ = "registro_financeiro"
    
    id_registro = Column(Integer, primary_key=True)
    id_barbeiro = Column(Integer, ForeignKey('barbeiro.id_barbeiro'), nullable=False)
    id_agendamento = Column(Integer, ForeignKey('agendamento.id_agendamento'), nullable=True)
    data = Column(Date, nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    tipo = Column(Enum(TipoRegistroFinanceiro), nullable=False)
    descricao = Column(Text, nullable=True)
    
    # Relacionamentos
    barbeiro = relationship("Barbeiro", back_populates="registros_financeiros")
    agendamento = relationship("Agendamento", back_populates="registros_financeiros")


#Base.metadata.create_all(engine)

def criar_tabelas():
    print("Conectando ao banco...")
    print(f"URL: {engine.url}")
    
    try:
        # Testa a conexão primeiro
        with engine.connect() as conn:
            print("Conexão bem-sucedida!")
        
        # Cria as tabelas
        Base.metadata.create_all(engine)
        print("Tabelas criadas com sucesso!")
        
        # Lista tabelas criadas
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            print(f"Tabelas: {', '.join(tables)}")
            
    except Exception as e:
        print(f"ERRO: {e}")
        raise
    
if __name__ == "__main__":
    criar_tabelas()