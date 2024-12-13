from pydantic import BaseModel
from typing import List, Optional
from Model import Filme
class FilmeSchema(BaseModel):
    """Define como um novo filme deve ser representado."""
    titulo: str = "Vingadores"
    categoria_id: int = 1
    nota: float = 8.5

class FilmeBuscaSchema(BaseModel):
    """Define como buscar um filme pelo ID ou título."""
    id: Optional[int]
    titulo: Optional[str] = "Vingadores"

class FilmeViewSchema(BaseModel):
    """Define como um filme será retornado."""
    id: int
    titulo: str
    categoria_id: int
    nota: float

class ListagemFilmesSchema(BaseModel):
    """Define como uma lista de filmes será retornada."""
    filmes: List[FilmeViewSchema]

class FilmeDelSchema(BaseModel):
    """Define a resposta ao deletar um filme."""
    message: str = "Filme removido com sucesso!"
    id: int
    
class FilmesPorCategoriaSchema(BaseModel):
    """Define como listar os filmes de uma categoria específica."""
    categoria_id: int
    filmes: List[FilmeViewSchema]

def apresenta_filmes_por_categoria(filmes: List[Filme], categoria_id: int):
    """Retorna a representação de uma lista de filmes pertencentes a uma categoria."""
    return {
        "categoria_id": categoria_id,
        "filmes": [
            {"id": f.id, "titulo": f.titulo, "categoria_id": f.categoria_id, "nota": f.nota}
            for f in filmes
        ]
    }

def apresenta_filmes(filmes: List[Filme]):
    """Retorna a representação de uma lista de filmes."""
    return {"filmes": [{"id": f.id, "titulo": f.titulo, "categoria_id": f.categoria_id, "nota": f.nota} for f in filmes]}

def apresenta_filme(filme: Filme):
    """Retorna a representação de um único filme."""
    return {
        "id": filme.id,
        "titulo": filme.titulo,
        "categoria_id": filme.categoria_id,
        "nota": filme.nota,
    }
