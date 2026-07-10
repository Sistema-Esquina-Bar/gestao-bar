from pydantic import BaseModel
from datetime import datetime
from typing import List

class FuncionarioEntrada(BaseModel):
    email: str
    nome: str
    cpf: str
    data_nascimento: str
    cargo: str
    senha: str

class FuncionarioResposta(FuncionarioEntrada):
    id: int
    class Config:
        from_attributes = True

class GerenteEntrada(BaseModel):
    email: str
    nome: str
    cpf: str
    data_nascimento: str
    senha: str

class GerenteResposta(GerenteEntrada):
    id: int
    class Config:
        from_attributes = True

class CategoriaEntrada(BaseModel):
    categoria: str

class CategoriaResposta(CategoriaEntrada):
    id: int
    class Config:
        from_attributes = True

class ProdutoEntrada(BaseModel):
    nome: str
    preco: float    
    categoria_id: int
    descrição: str

class ProdutoResposta(ProdutoEntrada):
    id: int
    class Config:
        from_attributes = True

class PedidoProdutoEntrada(BaseModel):
    quantidade: int
    pedido_id: int
    produto_id: int

class PedidoProdutoResposta(PedidoProdutoEntrada):
    id: int
    class Config:
        from_attributes = True

class PedidoEntrada(BaseModel):
    numero_da_mesa: int
    estado_pedido: str
    funcionario_id: int

class PedidoResposta(PedidoEntrada):
    id: int
    data_criacao: datetime
    class Config:
        from_attributes = True