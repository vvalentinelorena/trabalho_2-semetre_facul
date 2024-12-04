import sqlite3

class Model:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Criação da tabela apenas se ela não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS banco_tine (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor REAL NOT NULL,
                datadgasto TEXT NOT NULL,
                quant TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_data(self, nome, valor, datadgasto, quant):
        print("Inserindo dados:", nome, valor, datadgasto, quant)
        self.cursor.execute('''
            INSERT INTO banco_tine (nome, valor, datadgasto, quant)
            VALUES (?, ?, ?, ?)
        ''', (nome, valor, datadgasto, quant))
        self.conn.commit()

    def update_data(self, id, nome, valor, datadgasto, quant):
        print("Atualizando dados do ID:", id)
        self.cursor.execute('''
            UPDATE banco_tine
            SET nome=?, valor=?, datadgasto=?, quant=?
            WHERE id=?
        ''', (nome, valor, datadgasto, quant, id))
        self.conn.commit()

    def delete_data(self, id):
        print("Excluindo dado com ID:", id)
        self.cursor.execute('''
            DELETE FROM banco_tine WHERE id=?
        ''', (id,))
        self.conn.commit()

    def get_data(self):
        print("Buscando todos os dados")
        self.cursor.execute("SELECT * FROM banco_tine")
        return self.cursor.fetchall()

    def close_connection(self):
        print("Fechando conexão com o banco")
        self.conn.close()
