import sqlite3
import json
from datetime import datetime

class GerenciadorBancoDados:
    """Gerencia todas as operações com o banco de dados SQLite."""

    def __init__(self, nome_bd="historico_quantiscanner.db"):
        self.nome_bd = nome_bd
        self.conn = sqlite3.connect(nome_bd)
        self.criar_tabela()

    def criar_tabela(self):
        """Cria a tabela de histórico se ela não existir."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                dados_json TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def salvar_analise(self, nome, dados):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dados_json = json.dumps(dados)
        cursor.execute("INSERT INTO analises (nome, timestamp, dados_json) VALUES (?, ?, ?)",
                       (nome, timestamp, dados_json))
        self.conn.commit()
        return cursor.lastrowid

    def obter_historico(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, timestamp FROM analises ORDER BY timestamp DESC")
        return cursor.fetchall()

    def carregar_analise(self, id_analise):
        cursor = self.conn.cursor()
        cursor.execute("SELECT dados_json FROM analises WHERE id = ?", (id_analise,))
        resultado = cursor.fetchone()
        if resultado:
            return json.loads(resultado[0])
        return None

    def renomear_analise(self, id_analise, novo_nome):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE analises SET nome = ? WHERE id = ?", (novo_nome, id_analise))
        self.conn.commit()
        
    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
