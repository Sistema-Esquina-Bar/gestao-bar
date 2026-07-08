from pydantic import BaseModel

class FuncionarioEntrada(BaseModel):
    email: str
    nome: str
    cpf: str
    data_nascimento: str
    cargo: str
    senha: str

class Funcionario(FuncionarioEntrada):
    id: int

#Cadastro de Gerente
class GerenteEntrada (BaseModel):
    email: str
    nome: str
    cpf: str
    data_nascimento: str
    senha: str

class Gerente(GerenteEntrada):
    id: int

#Cadastro de Categoria
class categoriaEntrada(BaseModel):
    categoria: str

class categoria(categoriaEntrada):
    id: int

#Cadastro dos produtos
class produtoEntrada(BaseModel):
    nome: str
    preco: float    
    categoria_id: int
    descrição: str

class produto(produtoEntrada):
    id: int

class pedido_produtoEntrada(BaseModel):
    quantidade: str
    pedido_id: int
    produto_id: int

class pedido_produto(pedido_produtoEntrada):
    id: int

#Cadastro dos pedidos
class pedidoEntrada(BaseModel):
    numero_da_mesa: int
    estado_pedido: str
    funcionario_id: int
    data_criacao: str

class pedido(pedidoEntrada):
    id: int
