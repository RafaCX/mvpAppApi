from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from Model import Base

class Avaliacao(Base):
    __tablename__ = 'avaliacao'

    id = Column(Integer, primary_key=True, index=True)
    nota = Column(Float, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    filme_id = Column(Integer, ForeignKey('filme.id'))

    # Relacionamento com Usuario
    usuario = relationship("Usuario", back_populates="avaliacoes")

    # Relacionamento com Filme
    filme = relationship("Filme", back_populates="avaliacoes")

    def __init__(self, nota: float, usuario_id: int, filme_id: int):
        self.nota = nota
        self.usuario_id = usuario_id
        self.filme_id = filme_id
