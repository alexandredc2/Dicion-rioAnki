class Word:
    def __init__(self,tipo,categoria,genero,palavra_pt,palavra_de,exemplo_pt,exemplo_de,id=None):
        self.id = id
        self.tipo = tipo
        self.categoria = categoria
        self.genero = genero
        self.palavra_pt = palavra_pt
        self.palavra_de = palavra_de
        self.exemplo_pt = exemplo_pt
        self.exemplo_de = exemplo_de