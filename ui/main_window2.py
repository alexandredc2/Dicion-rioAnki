from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QMainWindow, QSplitter, QWidget, QVBoxLayout, QGridLayout, QLabel, QComboBox, QLineEdit, \
    QPushButton, QTextEdit, QTreeWidget, QHBoxLayout, QTreeWidgetItem, QMenu
import os


class MainWindow(QMainWindow):

    def __init__(self,banco):
        super().__init__()
        self.setWindowTitle('Dicionário Anki')
        self.setMinimumSize(1000,800)
        self.icon_pasta = os.path.join(os.path.dirname(__file__), "..", "assets", "pasta_icon.png")
        self.banco = banco
        self._setup_ui()
        self._carregar_pastas_combo()
        self._connect_signals()

        css_path = os.path.join(os.path.dirname(__file__), "..","assets","style.css")
        with open(css_path,"r") as f:
            self.setStyleSheet(f.read())

    def _menu_arvore(self, position):
        item = self.arvore_bancos.itemAt(position)

        menu = QMenu()
        act_criar = menu.addAction("Criar Pasta")
        act_renomear = menu.addAction("Renomear Pasta")
        act_deletar = menu.addAction("Deletar Pasta")

        act_renomear.setEnabled(item is not None)
        act_deletar.setEnabled(item is not None)

        action = menu.exec_(self.arvore_bancos.viewport().mapToGlobal(position))

        if action == act_criar:
            self._criar_pasta()
        elif action == act_renomear:
            self._renomear_pasta()
        elif action == act_deletar:
            self._deletar_pasta()

    def _criar_pasta(self, nome="Nova Pasta"):
        id_pasta = self.banco.criar_pasta(nome)
        item = QTreeWidgetItem(self.arvore_bancos,[nome])
        item.setIcon(0,QIcon(self.icon_pasta))
        item.setData(0, Qt.UserRole, id_pasta)
        self._carregar_pastas_combo()
        return item

    def _renomear_pasta(self):
        item = self.arvore_bancos.currentItem()
        if item is not None:
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.arvore_bancos.editItem(item,0)

    def _on_pasta_renomeada(self, item, coluna):
        id_pasta = item.data(0, Qt.UserRole)
        novo_nome = item.text(0)
        self.banco.renomear_pasta(id_pasta, novo_nome)
        self._carregar_pastas_combo()

    def _deletar_pasta(self):
        item = self.arvore_bancos.currentItem()
        if item is not None:
            id_pasta = item.data(0, Qt.UserRole)
            self.banco.deletar_pasta(id_pasta)
            parent = item.parent() or self.arvore_bancos.invisibleRootItem()
            parent.removeChild(item)
            self._carregar_pastas_combo()

    def _carregar_pastas_combo(self):
        self.combo_nome_pasta.clear()
        for id_pasta, nome in self.banco.buscar_pastas():
            self.combo_nome_pasta.addItem(nome, id_pasta)

    def _setup_ui(self):
        # --> Definição de todos layouts:
        self.layout_mainwindow = QSplitter(Qt.Vertical)
        self.layout_superior   = QSplitter(Qt.Horizontal)

        # --> Definição dos Paineis
        self.pn_bancos =   QWidget()
        self.pn_palavras = QWidget()
        self.pn_tabela =   QWidget()
        self.pn_bancos.setObjectName("pnBancos")
        self.pn_palavras.setObjectName("pnPalavras")
        self.pn_tabela.setObjectName("pnTabela")
        self.pn_bancos.setFixedSize(QSize(400,400))
        self.pn_palavras.setMinimumSize(QSize(635,0))

        # --> Layout dentro dos paineis
        self.layout_bancos =   QVBoxLayout()
        self.layout_palavras = QGridLayout()
        self.layout_tabela =   QVBoxLayout()
        self.layout_mainwindow.setContentsMargins(5,5,5,5)

        # --> Definição de Layout central
        self.setCentralWidget(self.layout_mainwindow)

        # --> Organização do Painel de Bancos:
        self.layout_superior.addWidget(self.pn_bancos)
        self.layout_superior.addWidget(self.pn_palavras)
        self.layout_mainwindow.addWidget(self.layout_superior)
        self.layout_mainwindow.addWidget(self.pn_tabela)
        self.pn_bancos.setLayout(self.layout_bancos)

        self.lbl_bancos1 = QLabel("Criação de Bancos de Dados")
        self.lbl_bancos1.setObjectName("labelNegrito")
        self.layout_bancos.addWidget(self.lbl_bancos1)

        row_banco = QHBoxLayout()
        self.lbl_nome_banco = QLabel("Nome do Banco de Dados: ")
        self.line_nome_banco = QLineEdit()
        row_banco.addWidget(self.lbl_nome_banco)
        row_banco.addWidget(self.line_nome_banco)
        self.layout_bancos.addLayout(row_banco)

        row_pasta = QHBoxLayout()
        self.lbl_nome_pasta = QLabel("Selecione a Pasta: ")
        self.combo_nome_pasta = QComboBox()
        self.combo_nome_pasta.setFixedWidth(247)
        row_pasta.addWidget(self.lbl_nome_pasta)
        row_pasta.addWidget(self.combo_nome_pasta)
        self.layout_bancos.addLayout(row_pasta)

        self.btn_add_banco = QPushButton("Adicionar Banco de Dados")
        self.btn_add_banco.setObjectName("buttonNegrito")
        self.layout_bancos.addWidget(self.btn_add_banco)

        self.arvore_bancos = QTreeWidget()
        self.arvore_bancos.setHeaderHidden(True)
        self.arvore_bancos.setFixedHeight(283)
        self.arvore_bancos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.arvore_bancos.customContextMenuRequested.connect(self._menu_arvore)
        for id_pasta, nome in self.banco.buscar_pastas():
            item = QTreeWidgetItem(self.arvore_bancos, [nome])
            item.setIcon(0, QIcon(self.icon_pasta))
            item.setData(0, Qt.UserRole, id_pasta)
        self.layout_bancos.addWidget(self.arvore_bancos)
        self.layout_bancos.addStretch()


        # --> Organização do Painel de Palavras:
        self.pn_palavras.setLayout(self.layout_palavras)
        self.lbl_tipo = QLabel("Tipo de Palavra")
        self.lbl_categoria = QLabel("Categoria da Palavra")
        self.lbl_singular = QLabel("Singular")
        self.lbl_plural = QLabel("Plural")
        self.lbl_plv_portugues = QLabel("Palavra em Português")
        self.lbl_plv_alemao = QLabel("Palavra em Alemão")
        self.lbl_ex_presente = QLabel("Exemplo no Presente")
        self.lbl_ex_passado = QLabel("Exemplo no Passado")
        self.lbl_ex_futuro = QLabel("Exemplo no Futuro")
        self.lbl_tipo.setObjectName("labelNegrito")
        self.lbl_categoria.setObjectName("labelNegrito")
        self.lbl_singular.setObjectName("labelNegrito")
        self.lbl_plural.setObjectName("labelNegrito")
        self.lbl_plv_portugues.setObjectName("labelNegrito")
        self.lbl_plv_alemao.setObjectName("labelNegrito")
        self.lbl_ex_presente.setObjectName("labelNegrito")
        self.lbl_ex_passado.setObjectName("labelNegrito")
        self.lbl_ex_futuro.setObjectName("labelNegrito")
        self.btn_add_palavra = QPushButton("Adicionar Palavra ao BD")
        self.btn_add_palavra.setMinimumSize(QSize(360,0))
        self.btn_add_palavra.setObjectName("buttonNegrito")
        self.txt_ex_pt_presente = QTextEdit()
        self.txt_ex_de_presente = QTextEdit()
        self.txt_ex_pt_passado = QTextEdit()
        self.txt_ex_de_passado = QTextEdit()
        self.txt_ex_pt_futuro = QTextEdit()
        self.txt_ex_de_futuro = QTextEdit()
        self.txt_ex_pt_presente.setMaximumSize(QSize(1360,40))
        self.txt_ex_de_presente.setMaximumSize(QSize(1360, 40))
        self.txt_ex_pt_passado.setMaximumSize(QSize(1360, 40))
        self.txt_ex_de_passado.setMaximumSize(QSize(1360, 40))
        self.txt_ex_pt_futuro.setMaximumSize(QSize(1360, 40))
        self.txt_ex_de_futuro.setMaximumSize(QSize(1360, 40))
        self.layout_palavras.addWidget(self.lbl_tipo,0,0)
        self.layout_palavras.addWidget(QComboBox(),0,1,1,2)
        self.layout_palavras.addWidget(self.lbl_categoria,1,0)
        self.layout_palavras.addWidget(QLineEdit(),1,1,1,2)
        self.layout_palavras.addWidget(self.lbl_singular,2,1,1,1,Qt.AlignCenter)
        self.layout_palavras.addWidget(self.lbl_plural,2,2,1,1,Qt.AlignCenter)
        self.layout_palavras.addWidget(self.lbl_plv_portugues,3,0)
        self.layout_palavras.addWidget(QLineEdit(),3,1)
        self.layout_palavras.addWidget(QLineEdit(),3,2)
        self.layout_palavras.addWidget(self.lbl_plv_alemao,4,0)
        self.layout_palavras.addWidget(QLineEdit(),4,1)
        self.layout_palavras.addWidget(QLineEdit(),4,2)
        self.layout_palavras.addWidget(self.lbl_ex_presente,5,0)
        self.layout_palavras.addWidget(self.txt_ex_pt_presente,5,1)
        self.layout_palavras.addWidget(self.txt_ex_de_presente,5,2)
        self.layout_palavras.addWidget(self.lbl_ex_passado,6,0)
        self.layout_palavras.addWidget(self.txt_ex_pt_passado,6,1)
        self.layout_palavras.addWidget(self.txt_ex_de_passado,6,2)
        self.layout_palavras.addWidget(self.lbl_ex_futuro,7,0)
        self.layout_palavras.addWidget(self.txt_ex_pt_futuro,7,1)
        self.layout_palavras.addWidget(self.txt_ex_de_futuro,7,2)
        self.layout_palavras.addWidget(self.btn_add_palavra, 8, 0, 1, 3, Qt.AlignCenter)
        self.layout_palavras.setRowStretch(self.layout_palavras.rowCount(),1)

    def _connect_signals(self):
        self.arvore_bancos.itemChanged.connect(self._on_pasta_renomeada)

