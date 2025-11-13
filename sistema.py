import datetime
import sqlite3

conn = sqlite3.connect("tarefas.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(tarefas)")
colunas = cursor.fetchall()
print(colunas)
conn.close()


class Tarefa:
    def __init__(self, id, descricao, cliente, data_pedido, status, prazo=None, valor = 0.0):
        self.id = id
        self.descricao = descricao
        self.data_pedido = data_pedido
        self.cliente = cliente
        self.prazo = prazo
        self.status = status
        self.valor = valor

    def atualizar_status(self, novo_status):
        self.status = novo_status
    
    def __str__(self):
        return f"Tarefa {self.id}: {self.descricao} | Data de emissão: {self.data_pedido} | Nome do cliente: {self.cliente} | Prazo: {self.prazo} | Status: {self.status} | Valor do pedido : R${self.valor:.2f}"
    
class GerenciadorDeTarefas:
    def __init__(self, db_nome = "tarefas.db"):
        self.conn = sqlite3.connect(db_nome)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        
    
    def criar_tabela(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tarefas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                cliente TEXT NOT NULL,
                data_pedido TEXT NOT NULL,
                status TEXT,
                prazo TEXT,
                valor REAL
            )   
        """)      
        self.conn.commit()

    
    def adicionar_tarefa(self, descricao, cliente, status, prazo = None, valor = 0.0):
        data_pedido = datetime.date.today().isoformat()
        self.cursor.execute("""
                INSERT INTO tarefas (descricao, cliente, data_pedido, status, prazo, valor) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (descricao, cliente, data_pedido, status, prazo, valor))             
        self.conn.commit()
        
    
    def listar_tarefas(self):
        self.cursor.execute("SELECT * FROM tarefas")
        registros = self.cursor.fetchall()
        tarefas = []
        for r in registros:
            id, descricao, cliente, data_pedido, status, prazo, valor = r
            tarefas.append(Tarefa(id, descricao, cliente, data_pedido, status, prazo, valor))
        return tarefas
        
    
    def atualizar_status(self, id, novo_status):
        self.cursor.execute("UPDATE tarefas SET status = ? WHERE id = ?", (novo_status, id))
        self.conn.commit()
        
    
    def remover_tarefa(self, id):
        self.cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))
        self.conn.commit()
    
    
    def verificador_prazos(self, proximos_dias = 0):
        hoje = datetime.date.today()
        self.cursor.execute("SELECT * FROM  tarefas WHERE prazo IS NOT NULL")
        tarefas = self.cursor.fetchall()
        alertas = []

        for tarefa in tarefas:
            id, descricao, cliente, data_pedido, prazo_str, status, valor = tarefa
            prazo = datetime.datetime.strptime(prazo_str, "%Y-%m-%d").date()

            if status.lower() != "concluído":
                if prazo < hoje:
                    alertas.append((id,descricao, prazo_str, "❌ Vencido ❌"))
                elif(prazo - hoje).days <= proximos_dias:
                    alertas.append((id, descricao, prazo_str, "⚠️ Prazo próximo ⚠️"))
            
        return alertas
