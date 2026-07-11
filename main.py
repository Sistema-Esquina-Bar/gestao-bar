from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from database import engine, Base, get_session
from models import Funcionario, Gerente, Categoria, Produto, Pedido, PedidoProduto
from schemas import (
    FuncionarioEntrada, FuncionarioResposta,
    GerenteEntrada, GerenteResposta,
    CategoriaEntrada, CategoriaResposta,
    ProdutoEntrada, ProdutoResposta,
    PedidoEntrada, PedidoResposta,
    PedidoProdutoEntrada, PedidoProdutoResposta
)
from security import verificar_api_key

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  
    yield

app = FastAPI(title="Sistema de Gestão do Espetinho da Esquina", version="1.4", lifespan=lifespan)


@app.get("/")
def raiz():
    return {"mensagem": "API do Espetinho da Esquina está funcionando!"}



@app.post("/Funcionario", response_model=FuncionarioResposta, status_code=201, dependencies=[Depends(verificar_api_key)])
def criar_funcionario(dados: FuncionarioEntrada, session: Session = Depends(get_session)):
    func = Funcionario(**dados.model_dump())
    session.add(func)
    session.commit()
    session.refresh(func)
    return func

@app.get("/Funcionario", response_model=List[FuncionarioResposta])
def listar_funcionarios(session: Session = Depends(get_session)):
    return session.query(Funcionario).order_by(Funcionario.nome).all()

@app.get("/Funcionario/{id}", response_model=FuncionarioResposta)
def buscar_funcionario(id: int, session: Session = Depends(get_session)):
    func = session.get(Funcionario, id)
    if func is None:
        raise HTTPException(404, "Funcionário não encontrado")
    return func

@app.delete("/Funcionario/{id}", status_code=204, dependencies=[Depends(verificar_api_key)])
def remover_funcionario(id: int, session: Session = Depends(get_session)):
    func = session.get(Funcionario, id)
    if func is None:
        raise HTTPException(404, "Funcionário não encontrado")
    session.delete(func)  
    session.commit()



@app.post("/Gerente", response_model=GerenteResposta, status_code=201, dependencies=[Depends(verificar_api_key)])
def criar_gerente(dados: GerenteEntrada, session: Session = Depends(get_session)):
    gerente = Gerente(**dados.model_dump())
    session.add(gerente)
    session.commit()
    session.refresh(gerente)
    return gerente

@app.get("/Gerente/{id}", response_model=GerenteResposta)
def buscar_gerente(id: int, session: Session = Depends(get_session)):
    gerente = session.get(Gerente, id)
    if gerente is None:
        raise HTTPException(404, "Gerente não encontrado")
    return gerente

@app.delete("/Gerente/{id}", status_code=204, dependencies=[Depends(verificar_api_key)])
def remover_gerente(id: int, session: Session = Depends(get_session)):
    gerente = session.get(Gerente, id)
    if gerente is None:
        raise HTTPException(404, "Gerente não encontrado")
    session.delete(gerente)
    session.commit()



@app.post("/Categoria", response_model=CategoriaResposta, status_code=201, dependencies=[Depends(verificar_api_key)])
def criar_categoria(dados: CategoriaEntrada, session: Session = Depends(get_session)):
    categoria_obj = Categoria(**dados.model_dump())
    session.add(categoria_obj)
    session.commit()
    session.refresh(categoria_obj)
    return categoria_obj



@app.post("/Produto", response_model=ProdutoResposta, status_code=201, dependencies=[Depends(verificar_api_key)])
def criar_produto(dados: ProdutoEntrada, session: Session = Depends(get_session)):
    prod = Produto(**dados.model_dump())
    session.add(prod)
    try:
        session.commit()
        session.refresh(prod)
    except IntegrityError:
        session.rollback()
        raise HTTPException(400, "Categoria informada inválida ou inexistente")
    return prod

@app.get("/Produto", response_model=List[ProdutoResposta])
def listar_produtos(session: Session = Depends(get_session)):
    return session.query(Produto).order_by(Produto.nome).all()

@app.get("/Produto/{id}", response_model=ProdutoResposta)
def buscar_produto(id: int, session: Session = Depends(get_session)):
    prod = session.get(Produto, id)
    if prod is None:
        raise HTTPException(404, "Produto não encontrado")
    return prod

@app.delete("/Produto/{id}", status_code=204, dependencies=[Depends(verificar_api_key)])
def remover_produto(id: int, session: Session = Depends(get_session)):
    prod = session.get(Produto, id)
    if prod is None:
        raise HTTPException(404, "Produto não encontrado")
    session.delete(prod)
    session.commit()



@app.post("/Pedido", response_model=PedidoResposta, status_code=201)
def criar_pedido(dados: PedidoEntrada, session: Session = Depends(get_session)):
    pedido_obj = Pedido(**dados.model_dump())
    session.add(pedido_obj)
    try:
        session.commit()
        session.refresh(pedido_obj)
    except IntegrityError:
        session.rollback()
        raise HTTPException(400, "Funcionário informado inválido ou inexistente")
    return pedido_obj

@app.get("/Pedido", response_model=List[PedidoResposta])
def listar_pedidos(session: Session = Depends(get_session)):
    return session.query(Pedido).all()

@app.get("/Pedido/{id}", response_model=PedidoResposta)
def buscar_pedido(id: int, session: Session = Depends(get_session)):
    pedido_obj = session.get(Pedido, id)
    if pedido_obj is None:
        raise HTTPException(404, "Pedido não encontrado")
    return pedido_obj

@app.patch("/pedidos/{id}", response_model=PedidoResposta)
def atualizar_estado_pedido(id: int, novo_estado: str, session: Session = Depends(get_session)):
    pedido_obj = session.get(Pedido, id)
    if pedido_obj is None:
        raise HTTPException(404, "Pedido não encontrado")
    pedido_obj.estado_pedido = novo_estado
    session.commit()
    session.refresh(pedido_obj)
    return pedido_obj

@app.delete("/Pedido/{id}", status_code=204)
def remover_pedido(id: int, session: Session = Depends(get_session)):
    pedido_obj = session.get(Pedido, id)
    if pedido_obj is None:
        raise HTTPException(404, "Pedido não encontrado")
    session.delete(pedido_obj)
    session.commit()



@app.post("/Pedido e Produto", response_model=PedidoProdutoResposta, status_code=201)
def criar_pedido_produto(dados: PedidoProdutoEntrada, session: Session = Depends(get_session)):
    vinc = PedidoProduto(**dados.model_dump())
    session.add(vinc)
    try:
        session.commit()
        session.refresh(vinc)
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Este produto já está associado a este pedido (Relação Duplicada)")
    return vinc

@app.delete("/Pedido e Produto/{id}", status_code=204)
def remover_pedido_produto(id: int, session: Session = Depends(get_session)):
    vinc = session.get(PedidoProduto, id)
    if vinc is None:
        raise HTTPException(404, "Vínculo de Pedido/Produto não encontrado")
    session.delete(vinc)
    session.commit()