from sqlite3 import connect

class DatabaseManager:
    def __init__(self):
        self.db = connect('database/dicionario.db')
        self.cursor = self.db.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pastas (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME TEXT NOT NULL
        )''')
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

    def criar_pasta(self, nome):
        self.cursor.execute('INSERT INTO pastas (nome) VALUES (?)',(nome,))
        self.db.commit()
        return self.cursor.lastrowid

    def renomear_pasta(self, id, novo_nome):
        self.cursor.execute('UPDATE pastas SET nome = ? WHERE id = ?',(novo_nome,id))
        self.db.commit()

    def deletar_pasta(self, id):
        self.cursor.execute('DELETE FROM pastas WHERE id = ?',(id,))
        self.db.commit()

    def buscar_pastas(self):
        self.cursor.execute('SELECT id, nome FROM pastas')
        return self.cursor.fetchall()

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

    def buscar_filtrado(self, tipo=None, texto=None):
        query = 'SELECT * FROM dicionario'
        params = []
        condicoes = []

        if tipo:
            condicoes.append('TIPO = ?')
            params.append(tipo)

        if texto:
            condicoes.append('PALAVRA_PT LIKE ?')
            params.append(f'%{texto}%')

        if condicoes:
            query += ' WHERE ' + ' AND '.join(condicoes)

        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()