from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from Model import Base

class Filme(Base):
    __tablename__ = 'filme'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), unique=True, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categoria.id'), nullable=False)
    nota = Column(Float, nullable=False, default=0.0)
    
    # Relacionamento com Categoria
    categoria = relationship("Categoria", back_populates="filmes")

    # Relacionamento com Avaliação
    avaliacoes = relationship("Avaliacao", back_populates="filme")

    def __init__(self, titulo: str, categoria_id: int, nota: float = 0.0):
        self.titulo = titulo
        self.categoria_id = categoria_id
        self.nota = nota
