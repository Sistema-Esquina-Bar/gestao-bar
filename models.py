from sqlalchemy import (Column, Integer, String, Float, Numeric, 
                        ForeignKey, DateTime, UniqueConstraint)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Funcionario(Base):
    __tablename__ = "funcionario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    cpf = Column(String(11), nullable=False)
    data_nascimento = Column(String, nullable=False)
    cargo = Column(String, nullable=False)
    senha = Column(String, nullable=False)

    pedidos = relationship("Pedido", back_populates="funcionario", cascade="all, delete-orphan")


class Gerente(Base):
    __tablename__ = "gerente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    cpf = Column(String(11), nullable=False)
    data_nascimento = Column(String, nullable=False)
    senha = Column(String, nullable=False)


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String, nullable=False)

    produtos = relationship("Produto", back_populates="categoria")


class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)  
    descrição = Column(String, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="produtos")
    pedido_produtos = relationship("PedidoProduto", back_populates="produto", cascade="all, delete-orphan")


class Pedido(Base):
    __tablename__ = "pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_da_mesa = Column(Integer, nullable=False)
    estado_pedido = Column(String, nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionario.id"), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    funcionario = relationship("Funcionario", back_populates="pedidos")
    pedido_produtos = relationship("PedidoProduto", back_populates="pedido", cascade="all, delete-orphan")


class PedidoProduto(Base):
    __tablename__ = "pedido_produto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedido.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produto.id"), nullable=False)

    pedido = relationship("Pedido", back_populates="pedido_produtos")
    produto = relationship("Produto", back_populates="pedido_produtos")

    __table_args__ = (
        UniqueConstraint("pedido_id", "produto_id", name="uq_pedido_produto"),
    )