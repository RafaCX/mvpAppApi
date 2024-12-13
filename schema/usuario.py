from pydantic import BaseModel
from typing import List, Optional
from Model import Usuario

class UsuarioSchema(BaseModel):
    """Define como um novo usuário deve ser representado."""
    nome: str = "João da Silva"

class UsuarioBuscaSchema(BaseModel):
    """Define como buscar um usuário pelo ID ou nome."""
    id: Optional[int]
    nome: Optional[str] = "João da Silva"

class UsuarioViewSchema(BaseModel):
    """Define como um usuário será retornado."""
    id: int
    nome: str

class ListagemUsuariosSchema(BaseModel):
    """Define como uma lista de usuários será retornada."""
    usuarios: List[UsuarioViewSchema]

class UsuarioDelSchema(BaseModel):
    """Define a resposta ao deletar um usuário."""
    message: str = "Usuário removido com sucesso!"
    id: int
def apresenta_usuarios(usuarios: List[Usuario]):
    """Retorna a representação de uma lista de usuários."""
    return {"usuarios": [{"id": u.id, "nome": u.nome} for u in usuarios]}

def apresenta_usuario(usuario: Usuario):
    """Retorna a representação de um único usuário."""
    return {"id": usuario.id, "nome": usuario.nome}
