from pydantic import BaseModel
from typing import List, Optional
from Model import Avaliacao
class AvaliacaoSchema(BaseModel):
    """Define como uma nova avaliação deve ser representada."""
    filme_id: int = 1
    usuario_id: int = 1
    nota: float = 4.5

class AvaliacaoBuscaSchema(BaseModel):
    """Define como buscar uma avaliação pelo ID do filme ou usuário."""
    filme_id: Optional[int]
    usuario_id: Optional[int]

class AvaliacaoViewSchema(BaseModel):
    """Define como uma avaliação será retornada."""
    id: int
    filme_id: int
    usuario_id: int
    nota: float

class ListagemAvaliacoesSchema(BaseModel):
    """Define como uma lista de avaliações será retornada."""
    avaliacoes: List[AvaliacaoViewSchema]

class AvaliacaoDelSchema(BaseModel):
    """Define a resposta ao deletar uma avaliação."""
    message: str = "Avaliação removida com sucesso!"
    id: int
def apresenta_avaliacoes(avaliacoes: List[Avaliacao]):
    """Retorna a representação de uma lista de avaliações."""
    return {
        "avaliacoes": [
            {
                "id": a.id,
                "filme_id": a.filme_id,
                "usuario_id": a.usuario_id,
                "nota": a.nota,
            }
            for a in avaliacoes
        ]
    }

def apresenta_avaliacao(avaliacao: Avaliacao):
    """Retorna a representação de uma única avaliação."""
    return {
        "id": avaliacao.id,
        "filme_id": avaliacao.filme_id,
        "usuario_id": avaliacao.usuario_id,
        "nota": avaliacao.nota,
    }
def apresenta_avaliacoes(avaliacoes: List[Avaliacao]):
    """Retorna a representação de uma lista de avaliações."""
    return {
        "avaliacoes": [
            {
                "id": a.id,
                "filme_id": a.filme_id,
                "usuario_id": a.usuario_id,
                "nota": a.nota,
                
            }
            for a in avaliacoes
        ]
    }

def apresenta_avaliacao(avaliacao: Avaliacao):
    """Retorna a representação de uma única avaliação."""
    return {
        "id": avaliacao.id,
        "filme_id": avaliacao.filme_id,
        "usuario_id": avaliacao.usuario_id,
        "nota": avaliacao.nota,
        
    }
