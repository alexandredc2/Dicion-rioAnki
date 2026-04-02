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
                                ANKI_CRIADO INTEGER NOT NULL DEFAULT 0
                                )''')
        self.db.commit()

    def close_connection(self):
        self.db.commit()
        self.db.close()

    def inserir_palavra(self,tipo,categoria,genero,palavra_pt,palavra_de,exemplo_pt,exemplo_de):


        self.cursor.execute('''
                            INSERT INTO dicionario (TIPO,CATEGORIA,GENERO,PALAVRA_PT,PALAVRA_DE,EXEMPLO_PT,EXEMPLO_DE)
                            VALUES (?,?,?,?,?,?,?)''',
                            (tipo,categoria,genero,palavra_pt,palavra_de,exemplo_pt,exemplo_de))
        self.db.commit()

    def buscar_categorias(self):
        self.cursor.execute('''SELECT DISTINCT CATEGORIA FROM dicionario''')
        lista_tuplas = self.cursor.fetchall()
        lista_categorias = [tpl[0] for tpl in lista_tuplas]
        return lista_categorias

    def verificar_similares(self, palavra_pt):
        self.cursor.execute('''SELECT PALAVRA_PT FROM dicionario WHERE PALAVRA_PT LIKE ?''',(f'%{palavra_pt}%',))
        lista_tuplas = self.cursor.fetchall()
        lista_palavras = [tpl[0] for tpl in lista_tuplas]
        return lista_palavras

    def buscar_todas(self):
        self.cursor.execute('''SELECT * FROM dicionario''')
        lista_completa = self.cursor.fetchall()
        return lista_completa
