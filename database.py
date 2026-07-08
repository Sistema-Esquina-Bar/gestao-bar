import sqlite3

DB_PATH = "bar.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS funcionario (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                email       TEXT NOT NULL,
                nome        TEXT NOT NULL,
                cpf         VARCHAR(11) NOT NULL,
                data_nascimento         DATE NOT NULL,
                cargo       TEXT NOT NULL,
                senha       TEXT NOT NULL
            ); 
            
            CREATE TABLE IF NOT EXISTS gerente (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                email       TEXT NOT NULL,
                nome        TEXT NOT NULL,
                cpf         VARCHAR(11) NOT NULL,
                data_nascimento         DATE NOT NULL,
                senha       TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS categoria (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria       TEXT NOT NULL           
            ); 

            CREATE TABLE IF NOT EXISTS produto (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nome            TEXT NOT NULL,
                preco           DECIMAL(4,2),
                descrição           TEXT NOT NULL,
                categoria_id            INTEGER NOT NULL,
                FOREIGN KEY (categoria_id)      REFERENCES categoria(id)
            );         

                CREATE TABLE IF NOT EXISTS pedido (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_da_mesa          INTEGER NOT NULL,
                estado_pedido           TEXT NOT NULL,        
                funcionario_id            INTEGER NOT NULL,
                data_criacao    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (funcionario_id)          REFERENCES funcionario(id)
            );            

                CREATE TABLE IF NOT EXISTS pedido_produto (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                quantidade          INTEGER NOT NULL,
                pedido_id           INTEGER NOT NULL,
                produto_id          INTEGER NOT NULL,
                FOREIGN KEY (pedido_id)          REFERENCES pedido(id),
                FOREIGN KEY (produto_id)          REFERENCES produto(id)  
            );

            """)