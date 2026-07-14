from openpyxl import Workbook
import sqlite3


class Database:

    def __init__(self):
        self.conexao = sqlite3.connect("clientes.db")
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        self.conexao.commit()

    def inserir_cliente(self, nome, cpf, telefone, email):
        self.cursor.execute("""
            INSERT INTO clientes (nome, cpf, telefone, email)
            VALUES (?, ?, ?, ?)
        """, (nome, cpf, telefone, email))
        self.conexao.commit()

    def listar_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def pesquisar_clientes(self, texto):
        self.cursor.execute("""
            SELECT * FROM clientes
            WHERE nome LIKE ?
               OR cpf LIKE ?
               OR telefone LIKE ?
               OR email LIKE ?
        """, (f"%{texto}%", f"%{texto}%", f"%{texto}%", f"%{texto}%"))

        return self.cursor.fetchall()

    def atualizar_cliente(self, id_cliente, nome, cpf, telefone, email):
        self.cursor.execute("""
            UPDATE clientes
            SET nome = ?, cpf = ?, telefone = ?, email = ?
            WHERE id = ?
        """, (nome, cpf, telefone, email, id_cliente))
        self.conexao.commit()

    def excluir_cliente(self, id_cliente):
        self.cursor.execute(
            "DELETE FROM clientes WHERE id = ?",
            (id_cliente,)
        )

    def exportar_para_excel(self, clientes):
        clientes = self.listar_clientes()
        workbook = Workbook()
        planilha = workbook.active
        planilha.title = "Clientes"
        planilha.append(["ID", "Nome", "CPF", "Telefone", "Email"])
        for cliente in clientes:
            planilha.append(cliente)
            workbook.save("clientes.xlsx")
        self.conexao.commit()