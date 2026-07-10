from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from typing import List

from database import DatabaseConfig
from dao import FuncionarioDAO, GerenteDAO, CategoriaDAO, ProdutoDAO, PedidoDAO, PedidoProdutoDAO
from security import verificar_api_key
from models import (
    Funcionario, FuncionarioEntrada, Gerente, GerenteEntrada, 
    categoria, categoriaEntrada, produto, produtoEntrada, 
    pedido, pedidoEntrada, pedido_produto, pedido_produtoEntrada
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o banco de dados via Singleton no início da aplicação
    DatabaseConfig().init_db()
    yield

app = FastAPI(title="Sistema de Gerenciamento do Espetinho da Esquina", version="1.4", lifespan=lifespan)

# --- DEPENDÊNCIAS PARA INSTANCIAR OS DAOs ---
def get_funcionario_dao(): return FuncionarioDAO()
def get_gerente_dao(): return GerenteDAO()
def get_categoria_dao(): return CategoriaDAO()
def get_produto_dao(): return ProdutoDAO()
def get_pedido_dao(): return PedidoDAO()
def get_pedido_produto_dao(): return PedidoProdutoDAO()


@app.get("/")
def raiz():
    return {"mensagem": "A API utilizando Padrões de Projeto está funcionando!"}

# --- FUNCIONÁRIO ---
@app.post("/Funcionario", response_model=Funcionario, status_code=201, dependencies=[Depends(verificar_api_key)])
def criar_funcionario(dados: FuncionarioEntrada, dao: FuncionarioDAO = Depends(get_funcionario_dao)):
    id_criado = dao.criar(dados)
    return Funcionario(id=id_criado, **dados.model_dump())

@app.get("/Funcionario", response_model=List[Funcionario])
def listar_funcionario(dao: FuncionarioDAO = Depends(get_funcionario_dao)):
    rows = dao.listar()
    return [Funcionario(**dict(r)) for r in rows]

@app.get("/Funcionario/{id}", response_model=Funcionario)
def buscar_funcionario(id: int, dao: FuncionarioDAO = Depends(get_funcionario_dao)):
    row = dao.buscar_por_id(id)
    if not row:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return Funcionario(**dict(row))

@app.delete("/Funcionario/{id}", status_code=204, dependencies=[Depends(verificar_api_key)])
def remover_funcionario(id: int, dao: FuncionarioDAO = Depends(get_funcionario_dao)):
    if not dao.remover(id):
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

# --- GERENTE ---
@app.post("/Gerente", response_model=Gerente, status_code=201, dependencies=[Depends(verificar_api_key)])
def criar_gerente(dados: GerenteEntrada, dao: GerenteDAO = Depends(get_gerente_dao)):
    id_criado = dao.criar(dados)
    return Gerente(id=id_criado, **dados.model_dump())

@app.get("/Gerente/{id}", response_model=Gerente)
def buscar_gerente(id: int, dao: GerenteDAO = Depends(get_gerente_dao)):
    row = dao.buscar_por_id(id)
    if not row:
        raise HTTPException(status_code=404, detail="Gerente não encontrado")
    return Gerente(**dict(row))

@app.delete("/Gerente/{id}", status_code=204, dependencies=[Depends(verificar_api_key)])
def remover_gerente(id: int, dao: GerenteDAO = Depends(get_gerente_dao)):
    if not dao.remover(id):
        raise HTTPException(status_code=404, detail="Gerente não encontrado")

# --- CATEGORIA ---
@app.post("/Categoria", response_model=categoria, status_code=201, dependencies=[Depends(verificar_api_key)])
def criar_categoria(dados: categoriaEntrada, dao: CategoriaDAO = Depends(get_categoria_dao)):
    id_criado = dao.criar(dados)
    return categoria(id=id_criado, **dados.model_dump())

# --- PRODUTO ---
@app.post("/Produto", response_model=produto, status_code=201, dependencies=[Depends(verificar_api_key)])
def criar_produto(dados: produtoEntrada, dao: ProdutoDAO = Depends(get_produto_dao)):
    id_criado = dao.criar(dados)
    return produto(id=id_criado, **dados.model_dump())

@app.get("/Produto", response_model=List[produto])
def listar_produtos(dao: ProdutoDAO = Depends(get_produto_dao)):
    rows = dao.listar()
    return [produto(**dict(r)) for r in rows]

@app.get("/Produto/{id}", response_model=produto)
def buscar_produto(id: int, dao: ProdutoDAO = Depends(get_produto_dao)):
    row = dao.buscar_por_id(id)
    if not row:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto(**dict(row))

@app.delete("/Produto/{id}", status_code=204, dependencies=[Depends(verificar_api_key)])
def remover_produto(id: int, dao: ProdutoDAO = Depends(get_produto_dao)):
    if not dao.remover(id):
        raise HTTPException(status_code=404, detail="Produto não encontrado")

# --- PEDIDO ---
@app.post("/Pedido", response_model=pedido, status_code=201)
def criar_pedido(dados: pedidoEntrada, dao: PedidoDAO = Depends(get_pedido_dao)):
    id_criado = dao.criar(dados)
    return pedido(id=id_criado, **dados.model_dump())

@app.get("/Pedido", response_model=List[pedido])
def listar_pedidos(dao: PedidoDAO = Depends(get_pedido_dao)):
    rows = dao.listar()
    return [pedido(**dict(r)) for r in rows]

@app.get("/Pedido/{id}", response_model=pedido)
def buscar_pedido(id: int, dao: PedidoDAO = Depends(get_pedido_dao)):
    row = dao.buscar_por_id(id)
    if not row:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido(**dict(row))

@app.patch("/pedidos/{id}", response_model=pedido)
def atualizar_estado_pedido(id: int, novo_estado: str, dao: PedidoDAO = Depends(get_pedido_dao)):
    if not dao.atualizar_estado(id, novo_estado):
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    row = dao.buscar_por_id(id)
    return pedido(**dict(row))

@app.delete("/Pedido/{id}", status_code=204)
def remover_pedido(id: int, dao: PedidoDAO = Depends(get_pedido_dao)):
    if not dao.remover(id):
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

# --- PEDIDO PRODUTO (N-N) ---
@app.post("/Pedido e Produto", response_model=pedido_produto, status_code=201)
def criar_pedido_produto(dados: pedido_produtoEntrada, dao: PedidoProdutoDAO = Depends(get_pedido_produto_dao)):
    id_criado = dao.criar(dados)
    return pedido_produto(id=id_criado, **dados.model_dump())

@app.delete("/Pedido e Produto/{id}", status_code=204)
def remover_pedido_produto(id: int, dao: PedidoProdutoDAO = Depends(get_pedido_produto_dao)):
    if not dao.remover(id):
        raise HTTPException(status_code=404, detail="Pedido/Produto não encontrado")