from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Schemas Pydantic

class RegisterRequest(BaseModel):
    nome: str
    email: str
    senha: str
    confirmar_senha: str

class LoginRequest(BaseModel):
    email: str
    senha: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    usuario: Dict[str, Any]

class AgendamentoRequest(BaseModel):
    id_cliente: int
    id_barbeiro: int
    servicos: List[int]
    data_hora: str

class BarbeiroCreateRequest(BaseModel):
    nome: str
    email: str
    senha: str
    telefone: str
    especialidade: str = "Geral"

class EspecialidadeRequest(BaseModel):
    nome: str
    descricao: Optional[str] = None

class DisponibilidadeRequest(BaseModel):
    data_hora_inicio: str
    data_hora_fim: str
    disponivel: bool = True

class ServicoRequest(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    duracao_estimada: int

class PreferenciaRequest(BaseModel):
    descricao: str

class UpdateStatusRequest(BaseModel):
    status: str
    data_hora: Optional[str] = None

class UpdateBarbeiroRequest(BaseModel):
    id_barbeiro: int

class NotificacaoRequest(BaseModel):
    id_cliente: int
    mensagem: str

class UpdatePerfilRequest(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
