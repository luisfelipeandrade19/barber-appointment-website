from datetime import datetime, date, time
from decimal import Decimal
from sqlalchemy import func, create_engine, Enum, Text, Date, Time, DECIMAL
from sqlalchemy.orm import relationship, registry, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base, sessionmaker
from sqlalchemy.sql import expression
from enum import Enum as PyEnum

Base = declarative_base()
engine = create_engine('postgresql://user:password@localhost/mydatabase')
_Session = sessionmaker(bind=engine)

table_registry = registry()

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
@table_registry.mapped_as_dataclass
class Usuario:
    __tablename__ = "usuario"
    
    id_usuario: Mapped[int] = mapped_column(init=False, primary_key=True)
    tipo: Mapped[TipoUsuario] = mapped_column(Enum(TipoUsuario), nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    telefone: Mapped[str] = mapped_column(nullable=True)
    senha_hash: Mapped[str] = mapped_column(nullable=False)
    data_cadastro: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    ativo: Mapped[bool] = mapped_column(default=True)
    
    # Relacionamentos
    cliente: Mapped["Cliente"] = relationship(back_populates="usuario", cascade="all, delete-orphan", uselist=False)
    barbeiro: Mapped["Barbeiro"] = relationship(back_populates="usuario", cascade="all, delete-orphan", uselist=False)

@table_registry.mapped_as_dataclass
class Cliente:
    __tablename__ = "cliente"
    
    id_cliente: Mapped[int] = mapped_column(primary_key=True, foreign_key="usuario.id_usuario")
    preferencias: Mapped[str] = mapped_column(Text, nullable=True)
    data_ultima_visita: Mapped[datetime] = mapped_column(nullable=True)
    
    # Relacionamentos
    usuario: Mapped[Usuario] = relationship(back_populates="cliente")
    agendamentos: Mapped[list["Agendamento"]] = relationship(back_populates="cliente")
    historicos: Mapped[list["HistoricoServico"]] = relationship(back_populates="cliente")

@table_registry.mapped_as_dataclass
class Barbeiro:
    __tablename__ = "barbeiro"
    
    id_barbeiro: Mapped[int] = mapped_column(primary_key=True, foreign_key="usuario.id_usuario")
    especialidade: Mapped[str] = mapped_column(nullable=True)
    ativo: Mapped[bool] = mapped_column(default=True)
    comissao: Mapped[Decimal] = mapped_column(DECIMAL(5, 2), default=Decimal('0.00'))
    
    # Relacionamentos
    usuario: Mapped[Usuario] = relationship(back_populates="barbeiro")
    servicos_criados: Mapped[list["Servico"]] = relationship(back_populates="barbeiro_criador")
    agendamentos: Mapped[list["Agendamento"]] = relationship(back_populates="barbeiro")
    disponibilidades: Mapped[list["DisponibilidadeBarbeiro"]] = relationship(back_populates="barbeiro")
    historicos: Mapped[list["HistoricoServico"]] = relationship(back_populates="barbeiro")
    registros_financeiros: Mapped[list["RegistroFinanceiro"]] = relationship(back_populates="barbeiro")

@table_registry.mapped_as_dataclass
class Servico:
    __tablename__ = "servico"
    
    id_servico: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=True)
    duracao_estimada: Mapped[int] = mapped_column(nullable=False)  # em minutos
    preco: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    ativo: Mapped[bool] = mapped_column(default=True)
    id_barbeiro_criador: Mapped[int] = mapped_column(foreign_key="barbeiro.id_barbeiro", nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    
    # Relacionamentos
    barbeiro_criador: Mapped[Barbeiro] = relationship(back_populates="servicos_criados")
    agendamento_servicos: Mapped[list["AgendamentoServico"]] = relationship(back_populates="servico")

@table_registry.mapped_as_dataclass
class Agendamento:
    __tablename__ = "agendamento"
    
    id_agendamento: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(foreign_key="cliente.id_cliente", nullable=False)
    id_barbeiro: Mapped[int] = mapped_column(foreign_key="barbeiro.id_barbeiro", nullable=False)
    data_hora_inicio: Mapped[datetime] = mapped_column(nullable=False)
    data_hora_fim: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[StatusAgendamento] = mapped_column(Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE)
    tempo_total_estimado: Mapped[int] = mapped_column(nullable=False)  # em minutos
    valor_total: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    observacoes: Mapped[str] = mapped_column(Text, nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    data_ultima_atualizacao: Mapped[datetime] = mapped_column(
        init=False, 
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relacionamentos
    cliente: Mapped[Cliente] = relationship(back_populates="agendamentos")
    barbeiro: Mapped[Barbeiro] = relationship(back_populates="agendamentos")
    agendamento_servicos: Mapped[list["AgendamentoServico"]] = relationship(
        back_populates="agendamento", 
        cascade="all, delete-orphan"
    )
    notificacoes: Mapped[list["Notificacao"]] = relationship(back_populates="agendamento")
    historicos: Mapped[list["HistoricoServico"]] = relationship(back_populates="agendamento")
    registros_financeiros: Mapped[list["RegistroFinanceiro"]] = relationship(back_populates="agendamento")

@table_registry.mapped_as_dataclass
class AgendamentoServico:
    __tablename__ = "agendamento_servico"
    
    id_agendamento_servico: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_agendamento: Mapped[int] = mapped_column(foreign_key="agendamento.id_agendamento", nullable=False)
    id_servico: Mapped[int] = mapped_column(foreign_key="servico.id_servico", nullable=False)
    preco_na_epoca: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    observacoes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relacionamentos
    agendamento: Mapped[Agendamento] = relationship(back_populates="agendamento_servicos")
    servico: Mapped[Servico] = relationship(back_populates="agendamento_servicos")

@table_registry.mapped_as_dataclass
class DisponibilidadeBarbeiro:
    __tablename__ = "disponibilidade_barbeiro"
    
    id_disponibilidade: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_barbeiro: Mapped[int] = mapped_column(foreign_key="barbeiro.id_barbeiro", nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fim: Mapped[time] = mapped_column(Time, nullable=False)
    tipo: Mapped[TipoDisponibilidade] = mapped_column(Enum(TipoDisponibilidade), default=TipoDisponibilidade.DISPONIVEL)
    recorrente: Mapped[bool] = mapped_column(default=False)
    
    # Relacionamentos
    barbeiro: Mapped[Barbeiro] = relationship(back_populates="disponibilidades")

@table_registry.mapped_as_dataclass
class Notificacao:
    __tablename__ = "notificacao"
    
    id_notificacao: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_agendamento: Mapped[int] = mapped_column(foreign_key="agendamento.id_agendamento", nullable=False)
    tipo: Mapped[TipoNotificacao] = mapped_column(Enum(TipoNotificacao), nullable=False)
    canal: Mapped[CanalNotificacao] = mapped_column(Enum(CanalNotificacao), nullable=False)
    destinatario: Mapped[str] = mapped_column(nullable=False)
    mensagem: Mapped[str] = mapped_column(Text, nullable=False)
    data_envio: Mapped[datetime] = mapped_column(nullable=False)
    status_envio: Mapped[StatusEnvio] = mapped_column(Enum(StatusEnvio), default=StatusEnvio.PENDENTE)
    tentativas: Mapped[int] = mapped_column(default=0)
    
    # Relacionamentos
    agendamento: Mapped[Agendamento] = relationship(back_populates="notificacoes")

@table_registry.mapped_as_dataclass
class HistoricoServico:
    __tablename__ = "historico_servico"
    
    id_historico: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_agendamento: Mapped[int] = mapped_column(foreign_key="agendamento.id_agendamento", nullable=False)
    id_cliente: Mapped[int] = mapped_column(foreign_key="cliente.id_cliente", nullable=False)
    id_barbeiro: Mapped[int] = mapped_column(foreign_key="barbeiro.id_barbeiro", nullable=False)
    data_servico: Mapped[datetime] = mapped_column(nullable=False)
    servicos_realizados: Mapped[str] = mapped_column(Text, nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    observacoes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relacionamentos
    agendamento: Mapped[Agendamento] = relationship(back_populates="historicos")
    cliente: Mapped[Cliente] = relationship(back_populates="historicos")
    barbeiro: Mapped[Barbeiro] = relationship(back_populates="historicos")

@table_registry.mapped_as_dataclass
class RegistroFinanceiro:
    __tablename__ = "registro_financeiro"
    
    id_registro: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_barbeiro: Mapped[int] = mapped_column(foreign_key="barbeiro.id_barbeiro", nullable=False)
    id_agendamento: Mapped[int] = mapped_column(foreign_key="agendamento.id_agendamento", nullable=True)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    valor: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    tipo: Mapped[TipoRegistroFinanceiro] = mapped_column(Enum(TipoRegistroFinanceiro), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relacionamentos
    barbeiro: Mapped[Barbeiro] = relationship(back_populates="registros_financeiros")
    agendamento: Mapped[Agendamento] = relationship(back_populates="registros_financeiros")

# Criar todas as tabelas
def criar_tabelas():
    Base.metadata.create_all(engine)

# Exemplo de uso
if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso!")