from sqlite3 import connect
import os

"""
-> Configuração da Tabela de Dados para as Palavras:
|  ID  |   TIPO   |   CATEGORIA   |  GÊNERO  |  PALAVRA(PT) | PALAVRA(DE) | PRESENTE(PT) | PRESENTE(DE) | PASSADO(PT) | PASSADO(DE) | FUTURO(PT) | FUTURO(DE) | OBSERVAÇÕES |
"""

class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "dicionario.db")
        self.db = connect(self.db_path)
        self.cursor = self.db.cursor()

        # -> Banco de Dados: Armazenamento das informações de Pastas criadas:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pastas (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOME TEXT NOT NULL
                            )''')

        # -> Banco de Dados: Armazenamento das informações de Palavras criadas:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dicionario
                                (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                TIPO TEXT NOT NULL,
                                CATEGORIA TEXT NOT NULL,
                                GENERO TEXT,
                                PALAVRA_PT TEXT NOT NULL,
                                PALAVRA_DE TEXT NOT NULL,
                                PRESENTE_PT TEXT NOT NULL,
                                PRESENTE_DE TEXT NOT NULL,
                                PASSADO_PT TEXT NOT NULL,
                                PASSADO_DE TEXT NOT NULL,
                                FUTURO_PT TEXT NOT NULL,
                                FUTURO_DE TEXT NOT NULL,
                                OBSERVACOES TEXT DEFAULT NULL 
                                )''')
        
        # -> Banco de Dados: Armazenamento das informações de Tabelas criadas:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bancos(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOME TEXT NOT NULL,
                            PARENT_ID INTEGER NOT NULL,
                            FOREIGN KEY (PARENT_ID) REFERENCES pastas (ID))''')
        
        self.db.commit()

    def criar_banco(self,nome,parent_id):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {nome} (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            TIPO TEXT NOT NULL,
                            CATEGORIA TEXT NOT NULL,
                            GENERO TEXT,
                            PALAVRA_PT TEXT NOT NULL,
                            PALAVRA_DE TEXT NOT NULL,
                            PRESENTE_PT TEXT NOT NULL,
                            PRESENTE_DE TEXT NOT NULL,
                            PASSADO_PT TEXT NOT NULL,
                            PASSADO_DE TEXT NOT NULL,
                            FUTURO_PT TEXT NOT NULL,
                            FUTURO_DE TEXT NOT NULL,
                            OBSERVACOES TEXT DEFAULT NULL 
                            )''')
        self.cursor.execute('INSERT INTO bancos (NOME, PARENT_ID) VALUES (?,?)', (nome,parent_id))
        self.db.commit()
        return self.cursor.lastrowid

    def deletar_banco(self, id):
        self.cursor.execute('DELETE FROM bancos WHERE ID = ?', (id,))
        self.db.commit()

    def renomear_banco(self,id,novo_nome):
        self.cursor.execute('UPDATE bancos SET NOME = ? WHERE ID = ?', (novo_nome, id))
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

    def buscar_bancos(self):
        self.cursor.execute('SELECT ID, NOME, PARENT_ID FROM bancos')
        return self.cursor.fetchall()

    def buscar_palavras(self,tabela):
        self.cursor.execute(f'SELECT * FROM {tabela}')
        return self.cursor.fetchall()

    def close_connection(self):
        self.db.commit()
        self.db.close()

    def inserir_palavra(self, tabela, tipo, cat, gen, palavra_pt, palavra_de,
                        prept, prede, paspt, pasde, futpt, futde, obs):
        self.cursor.execute(f'''INSERT INTO {tabela}
                            (TIPO, CATEGORIA, GENERO, PALAVRA_PT, PALAVRA_DE,
                            PRESENTE_PT, PRESENTE_DE, PASSADO_PT, PASSADO_DE,
                            FUTURO_PT, FUTURO_DE, OBSERVACOES)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                            (tipo, cat, gen, palavra_pt, palavra_de,
                             prept, prede, paspt, pasde, futpt, futde, obs))
        self.db.commit()

    def deletar_palavra(self,tabela,id):
        self.cursor.execute(f'DELETE FROM {tabela} WHERE ID = ?',(id,))
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