from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
import sqlite3

from database import get_conn, init_db
from models import (Funcionario, FuncionarioEntrada, Gerente, GerenteEntrada, categoria, categoriaEntrada, produto, produtoEntrada, pedido, pedidoEntrada) 

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Sistema de Gerenciamento do Espetinho da Esquina", version="1.3", lifespan=lifespan)

#Métodos com Funcionário---------------------------------------------------------------------------------------------------

@app.get("/")
def raiz():
    return {"mensagem": "A API está funcionando!"}

@app.post("/Funcionario", response_model=Funcionario, status_code=201)
def criar_funcionario(dados: FuncionarioEntrada):
    with get_conn() as conn:
        cur = conn.execute (
            "INSERT INTO funcionários (email, nome, cpf, data_nascimento, cargo, senha) VALUES (?, ?, ?, ?, ?, ?)",
            (dados.email, dados.nome, dados.cpf, dados.data_nascimento, dados.cargo, dados.senha)
        )
        conn.commit()
    return Funcionario(id=cur.lastrowid, **dados.model_dump())

@app.get("/Funcionario", response_model=List[Funcionario])
def listar_funcionarios():
    with get_conn() as conn:
        rows = conn.execute("SELECT email, nome, cpf, data_nascimento, cargo FROM funcionários").fetchall()
    return [Funcionario(**dict(r)) for r in rows]

@app.get("/Funcionario/{id}", response_model=Funcionario)
def buscar_funcionario(id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, email, nome, cpf, data_nascimento, cargo FROM funcionários WHERE id = ?", (id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return Funcionario(**dict(row))

@app.delete("/Funcionario/{id}", status_code=204)
def remover_funcionario(id: int):
    with get_conn() as conn:
        res = conn.execute("DELETE FROM funcionários WHERE id = ?", (id,))
        conn.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Funcionario não encontrado")

#Métodos com Gerente------------------------------------------------------------------------------------------------------

@app.post("/Gerente", response_model=Gerente, status_code=201)
def criar_gerente(dados: GerenteEntrada):
    with get_conn() as conn:
        cur = conn.execute (
            "INSERT INTO gerente (email, nome, cpf, data_nascimento, senha) VALUES (?, ?, ?, ?, ?)",
            (dados.email, dados.nome, dados.cpf, dados.data_nascimento, dados.senha)
        )
        conn.commit()
    return Gerente(id=cur.lastrowid, **dados.model_dump())

@app.get("/Gerente/{id}", response_model=Gerente)
def buscar_gerente(id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, email, nome, cpf, data_nascimento FROM gerente WHERE id = ?", (id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Gerente não encontrado")
    return Gerente(**dict(row))

@app.delete("/Gerente/{id}", status_code=204)
def remover_gerente(id: int):
    with get_conn() as conn:
        res = conn.execute("DELETE FROM gerente WHERE id = ?", (id,))
        conn.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Gerente não encontrado")

#Métodos com categoria------------------------------------------------------------------------------------------------------

@app.post("/Categoria", response_model=categoria, status_code=201)
def criar_categoria(dados: categoriaEntrada):
    with get_conn() as conn:
        cur = conn.execute (
            "INSERT INTO categoria (categoria) VALUES (?)"
            (dados.categoria,)
        )
        conn.commit()
    return categoria(id=cur.lastrowid, **dados.model_dump())

#Métodos com produtos------------------------------------------------------------------------------------------------------
@app.post("/Produto", response_model=produto, status_code=201)
def criar_produto(dados: produtoEntrada):
    with get_conn() as conn:
        cur = conn.execute (
            "INSERT INTO produto (nome, descrição, categoria_id) VALUES (?, ?, ?)",
            (dados.nome, dados.descricao, dados.categoria_id)
        )
        conn.commit()
    return produto(id=cur.lastrowid, **dados.model_dump())

@app.get("/Produto", response_model=List[produto])
def listar_produtos():
    with get_conn() as conn:
        rows = conn.execute("SELECT nome, descrição, categoria_id FROM produto").fetchall()
    return [produto(**dict(r)) for r in rows]

@app.get("/Produto/{id}", response_model=produto)
def buscar_produto(id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, nome, descrição, categoria_id FROM produto WHERE id = ?", (id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto(**dict(row))

@app.delete("/Produto/{id}", status_code=204)
def remover_produto(id: int):
    with get_conn() as conn:
        res = conn.execute("DELETE FROM produto WHERE id = ?", (id,))
        conn.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

#Métodos com pedidos------------------------------------------------------------------------------------------------------
@app.post("/Pedido", response_model=pedido, status_code=201)
def criar_pedido(dados: pedidoEntrada):
    with get_conn() as conn:
        cur = conn.execute (
            "INSERT INTO pedido (numero_da_mesa, estado_pedido, funcionarios_id, pedido_produto_id, data_criacao) VALUES (?, ?, ?, ?, ?)",
            (dados.numero_da_mesa, dados.estado_pedido, dados.funcionarios_id, dados.pedido_produto_id)
        
    )
        conn.commit()
    return pedido(id=cur.lastrowid, **dados.model_dump())

@app.get("/Pedido", response_model=List[pedido])
def listar_pedidos():
    with get_conn() as conn:
        rows = conn.execute("SELECT numero_da_mesa, estado_pedido, funcionarios_id, pedido_produto_id, data_criacao FROM pedido").fetchall()
    return [pedido(**dict(r)) for r in rows]


@app.get("/Pedido/{id}", response_model=pedido)
def buscar_pedido(id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, numero_da_mesa, estado_pedido, funcionarios_id, pedido_produto_id, data_criacao FROM pedido WHERE id = ?", (id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return pedido(**dict(row))

@app.patch("/pedidos/{id}", response_model=pedido)
def atualizar_estado_pedido(id: int, novo_estado: str):
    with get_conn() as conn:
        res = conn.execute(
            "UPDATE pedido SET estado_pedido = ? WHERE id = ?", 
            (novo_estado, id)
        )
        conn.commit()
        if res.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        row = conn.execute("SELECT id, numero_da_mesa, estado_pedido, funcionarios_id, pedido_produto_id, data_criacao FROM pedido WHERE id = ?", (id,)).fetchone()
    return pedido(**dict(row))