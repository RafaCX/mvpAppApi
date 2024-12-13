from pydantic import BaseModel
from typing import List, Optional
from Model import Categoria

class CategoriaSchema(BaseModel):
    """Define como uma nova categoria deve ser representada."""
    nome: str = "Ação"

class CategoriaBuscaSchema(BaseModel):
    """Define como buscar uma categoria pelo ID ou nome."""
    id: Optional[int]
    nome: Optional[str] = "Ação"

class CategoriaViewSchema(BaseModel):
    """Define como uma categoria será retornada."""
    id: int
    nome: str

class ListagemCategoriasSchema(BaseModel):
    """Define como uma lista de categorias será retornada."""
    categorias: List[CategoriaViewSchema]

class CategoriaDelSchema(BaseModel):
    """Define a resposta ao deletar uma categoria."""
    message: str = "Categoria removida com sucesso!"
    id: int
def apresenta_categorias(categorias: List[Categoria]):
    """Retorna a representação de uma lista de categorias."""
    return {"categorias": [{"id": c.id, "nome": c.nome} for c in categorias]}

def apresenta_categoria(categoria: Categoria):
    """Retorna a representação de uma única categoria."""
    return {"id": categoria.id, "nome": categoria.nome}

