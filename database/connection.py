from sqlite3 import connect

class DatabaseManager:
    def __init__(self):
        self.db = connect('database/dicionario.db')
        self.cursor = self.db.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dicionario
                                (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                TIPO TEXT NOT NULL,
                                CATEGORIA TEXT NOT NULL,
                                GENERO TEXT,
                                PALAVRA_PT TEXT NOT NULL,
                                PALAVRA_DE TEXT NOT NULL,
                                EXEMPLO_PT TEXT NOT NULL,
                                EXEMPLO_DE TEXT NOT NULL,
                                ANKI_CRIADO INTEGER NOT NULL
                                )''')
        self.db.commit()

    def close_connection(self):
        self.db.commit()
        self.db.close()