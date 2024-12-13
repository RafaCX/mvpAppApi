from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from Model import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False)

    # Relacionamento com avaliações
    avaliacoes = relationship("Avaliacao", back_populates="usuario")

    def __init__(self, nome: str):
        self.nome = nome
