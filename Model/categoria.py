from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from Model import Base

class Categoria(Base):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)

    # Relacionamento com filmes
    filmes = relationship("Filme", back_populates="categoria")

    def __init__(self, nome: str):
        self.nome = nome
