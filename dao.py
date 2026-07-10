from typing import List, Optional
import sqlite3
from database import DatabaseConfig
from models import (
    FuncionarioEntrada, GerenteEntrada, categoriaEntrada, 
    produtoEntrada, pedidoEntrada, pedido_produtoEntrada
)

class FuncionarioDAO:
    def __init__(self):
        self.db_config = DatabaseConfig()

    def criar(self, dados: FuncionarioEntrada) -> int:
        with self.db_config.get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO funcionario (email, nome, cpf, data_nascimento, cargo, senha) VALUES (?, ?, ?, ?, ?, ?)",
                (dados.email, dados.nome, dados.cpf, dados.data_nascimento, dados.cargo, dados.senha)
            )
            conn.commit()
            return cur.lastrowid

    def listar(self) -> List[sqlite3.Row]:
        with self.db_config.get_conn() as conn:
            return conn.execute("SELECT id, email, nome, cpf, data_nascimento, cargo, senha FROM funcionario").fetchall()

    def buscar_por_id(self, id: int) -> Optional[sqlite3.Row]:
        with self.db_config.get_conn() as conn:
            return conn.execute("SELECT id, email, nome, cpf, data_nascimento, cargo, senha FROM funcionario WHERE id = ?", (id,)).fetchone()

    def remover(self, id: int) -> bool:
        with self.db_config.get_conn() as conn:
            res = conn.execute("DELETE FROM funcionario WHERE id = ?", (id,))
            conn.commit()
            return res.rowcount > 0


class GerenteDAO:
    def __init__(self):
        self.db_config = DatabaseConfig()

    def criar(self, dados: GerenteEntrada) -> int:
        with self.db_config.get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO gerente (email, nome, cpf, data_nascimento, senha) VALUES (?, ?, ?, ?, ?)",
                (dados.email, dados.nome, dados.cpf, dados.data_nascimento, dados.senha)
            )
            conn.commit()
            return cur.lastrowid

    def buscar_por_id(self, id: int) -> Optional[sqlite3.Row]:
        with self.db_config.get_conn() as conn:
            return conn.execute("SELECT id, email, nome, cpf, data_nascimento, senha FROM gerente WHERE id = ?", (id,)).fetchone()

    def remover(self, id: int) -> bool:
        with self.db_config.get_conn() as conn:
            res = conn.execute("DELETE FROM gerente WHERE id = ?", (id,))
            conn.commit()
            return res.rowcount > 0


class CategoriaDAO:
    def __init__(self):
        self.db_config = DatabaseConfig()

    def criar(self, dados: categoriaEntrada) -> int:
        with self.db_config.get_conn() as conn:
            cur = conn.execute("INSERT INTO categoria (categoria) VALUES (?)", (dados.categoria,))
            conn.commit()
            return cur.lastrowid


class ProdutoDAO:
    def __init__(self):
        self.db_config = DatabaseConfig()

    def criar(self, dados: produtoEntrada) -> int:
        with self.db_config.get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO produto (nome, preco, descrição, categoria_id) VALUES (?, ?, ?, ?)",
                (dados.nome, dados.preco, dados.descrição, dados.categoria_id)
            )
            conn.commit()
            return cur.lastrowid

    def listar(self) -> List[sqlite3.Row]:
        with self.db_config.get_conn() as conn:
            return conn.execute("SELECT id, nome, preco, descrição, categoria_id FROM produto").fetchall()

    def buscar_por_id(self, id: int) -> Optional[sqlite3.Row]:
        with self.db_config.get_conn() as conn:
            return conn.execute("SELECT id, nome, preco, descrição, categoria_id FROM produto WHERE id = ?", (id,)).fetchone()

    def remover(self, id: int) -> bool:
        with self.db_config.get_conn() as conn:
            res = conn.execute("DELETE FROM produto WHERE id = ?", (id,))
            conn.commit()
            return res.rowcount > 0


class PedidoDAO:
    def __init__(self):
        self.db_config = DatabaseConfig()

    def criar(self, dados: pedidoEntrada) -> int:
        with self.db_config.get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO pedido (numero_da_mesa, estado_pedido, funcionario_id, data_criacao) VALUES (?, ?, ?, ?)",
                (dados.numero_da_mesa, dados.estado_pedido, dados.funcionario_id, dados.data_criacao)
            )
            conn.commit()
            return cur.lastrowid

    def listar(self) -> List[sqlite3.Row]:
        with self.db_config.get_conn() as conn:
            return conn.execute("SELECT id, numero_da_mesa, estado_pedido, funcionario_id, data_criacao FROM pedido").fetchall()

    def buscar_por_id(self, id: int) -> Optional[sqlite3.Row]:
        with self.db_config.get_conn() as conn:
            return conn.execute("SELECT id, numero_da_mesa, estado_pedido, funcionario_id, data_criacao FROM pedido WHERE id = ?", (id,)).fetchone()

    def atualizar_estado(self, id: int, novo_estado: str) -> bool:
        with self.db_config.get_conn() as conn:
            res = conn.execute("UPDATE pedido SET estado_pedido = ? WHERE id = ?", (novo_estado, id))
            conn.commit()
            return res.rowcount > 0

    def remover(self, id: int) -> bool:
        with self.db_config.get_conn() as conn:
            res = conn.execute("DELETE FROM pedido WHERE id = ?", (id,))
            conn.commit()
            return res.rowcount > 0


class PedidoProdutoDAO:
    def __init__(self):
        self.db_config = DatabaseConfig()

    def criar(self, dados: pedido_produtoEntrada) -> int:
        with self.db_config.get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO pedido_produto (quantidade, pedido_id, produto_id) VALUES (?, ?, ?)",
                (dados.quantidade, dados.pedido_id, dados.produto_id)
            )
            conn.commit()
            return cur.lastrowid

    def remover(self, id: int) -> bool:
        with self.db_config.get_conn() as conn:
            res = conn.execute("DELETE FROM pedido_produto WHERE id = ?", (id,))
            conn.commit()
            return res.rowcount > 0