from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QMainWindow, QSplitter, QWidget, QVBoxLayout, QGridLayout, QLabel, QComboBox, QLineEdit, \
    QPushButton, QTextEdit, QTreeWidget, QHBoxLayout, QTreeWidgetItem, QMenu, QTableWidget, QHeaderView, QMessageBox, \
    QTableWidgetItem
import os


class MainWindow(QMainWindow):

    def __init__(self,banco):
        super().__init__()
        self.setWindowTitle('Dicionário Anki')
        self.setMinimumSize(1000,800)
        self.icon_pasta = os.path.join(os.path.dirname(__file__), "..", "assets", "pasta_icon.png")
        self.icon_table = os.path.join(os.path.dirname(__file__), "..", "assets", "table_icon.png")
        self.icon       = os.path.join(os.path.dirname(__file__), "..", "assets", "main_ico.ico")
        self.setWindowIcon(QIcon(self.icon))
        self.banco = banco
        self.banco_selecionado = None
        self._setup_ui()
        self._carregar_pastas_combo()
        self._connect_signals()

        css_path = os.path.join(os.path.dirname(__file__), "..","assets","style.css")
        with open(css_path,"r") as f:
            self.setStyleSheet(f.read())

    def _menu_arvore(self, position):
        item = self.arvore_bancos.itemAt(position)
        tipo = item.data(0,Qt.UserRole+1) if item else None

        menu = QMenu()

        if tipo == "banco":
            act_renomear = menu.addAction("Renomear Tabela")
            act_deletar  = menu.addAction("Deletar Tabela")
            action = menu.exec_(self.arvore_bancos.viewport().mapToGlobal(position))
            if action == act_renomear:
                self._renomear_banco()
            elif action == act_deletar:
                self._deletar_banco()

        else:
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
        item.setData(0, Qt.UserRole+1,"pasta")
        self._carregar_pastas_combo()
        return item

    def _renomear_pasta(self):
        item = self.arvore_bancos.currentItem()
        if item is not None:
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.arvore_bancos.editItem(item,0)

    def _on_pasta_renomeada(self, item, coluna):
        tipo = item.data(0, Qt.UserRole + 1)
        id_item = item.data(0, Qt.UserRole)
        novo_nome = item.text(0)

        if tipo == "pasta":
            self.banco.renomear_pasta(id_item, novo_nome)
            self._carregar_pastas_combo()
        elif tipo == "banco":
            self.banco.renomear_banco(id_item, novo_nome)

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
        self.pn_bancos.setFixedSize(QSize(400,410))
        self.pn_palavras.setMinimumSize(QSize(635,0))

        # --> Layout dentro dos paineis
        self.layout_bancos =   QVBoxLayout()
        self.layout_palavras = QGridLayout()
        self.layout_tabela =   QVBoxLayout()
        self.layout_mainwindow.setContentsMargins(5,5,5,5)

        # --> Definição de Layout central
        self.setCentralWidget(self.layout_mainwindow)

        # --> Criação do Menu Superior e do Rodapé
        menu_bar = self.menuBar()
        menu_file = menu_bar.addMenu("Arquivos")
        menu_about = menu_bar.addMenu("Sobre")
        self.act_gerenciar_banco = menu_file.addAction("Gerenciar Bancos de Dados")
        self.act_sair = menu_file.addAction("Sair")
        status_bar = self.statusBar()
        status_bar.setSizeGripEnabled(False)

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
        self.arvore_bancos.setFixedHeight(293)
        self.arvore_bancos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.arvore_bancos.customContextMenuRequested.connect(self._menu_arvore)
        pastas_map = {}
        for id_pasta, nome in self.banco.buscar_pastas():
            item = QTreeWidgetItem(self.arvore_bancos, [nome])
            item.setIcon(0, QIcon(self.icon_pasta))
            item.setData(0, Qt.UserRole, id_pasta)
            item.setData(0, Qt.UserRole + 1, "pasta")
            pastas_map[id_pasta] = item
        for id_banco, nome, parent_id in self.banco.buscar_bancos():
            if parent_id in pastas_map:
                filho = QTreeWidgetItem(pastas_map[parent_id], [nome])
                filho.setIcon(0, QIcon(self.icon_table))
                filho.setData(0, Qt.UserRole, id_banco)
                filho.setData(0, Qt.UserRole+1,"banco")
                pastas_map[parent_id].setExpanded(True)
        self.layout_bancos.addWidget(self.arvore_bancos)
        self.layout_bancos.addStretch()


        # --> Organização do Painel de Palavras:
        self.pn_palavras.setLayout(self.layout_palavras)
        self.lbl_tipo = QLabel("Tipo de Palavra")
        self.lbl_categoria = QLabel("Categoria da Palavra")
        self.lbl_genero = QLabel("Gênero")
        self.lbl_singular = QLabel("Singular")
        self.lbl_plural = QLabel("Plural")
        self.lbl_plv_portugues = QLabel("Palavra em Português")
        self.lbl_plv_alemao = QLabel("Palavra em Alemão")
        self.lbl_portugues = QLabel("Português")
        self.lbl_alemao = QLabel("Alemão")
        self.lbl_ex_presente = QLabel("Exemplo no Presente")
        self.lbl_ex_passado = QLabel("Exemplo no Passado")
        self.lbl_ex_futuro = QLabel("Exemplo no Futuro")
        self.lbl_observacoes = QLabel("Observações")
        self.lbl_tipo.setObjectName("labelNegrito")
        self.lbl_categoria.setObjectName("labelNegrito")
        self.lbl_genero.setObjectName("labelNegrito")
        self.lbl_singular.setObjectName("labelNegrito")
        self.lbl_plural.setObjectName("labelNegrito")
        self.lbl_plv_portugues.setObjectName("labelNegrito")
        self.lbl_plv_alemao.setObjectName("labelNegrito")
        self.lbl_portugues.setObjectName("labelNegrito")
        self.lbl_alemao.setObjectName("labelNegrito")
        self.lbl_ex_presente.setObjectName("labelNegrito")
        self.lbl_ex_passado.setObjectName("labelNegrito")
        self.lbl_ex_futuro.setObjectName("labelNegrito")
        self.lbl_observacoes.setObjectName("labelNegrito")
        self.btn_add_palavra = QPushButton("Adicionar Palavra à Tabela")
        self.btn_add_palavra.setMinimumSize(QSize(360,0))
        self.btn_add_palavra.setObjectName("buttonNegrito")
        self.tipo = QComboBox()
        self.tipo.addItems(['', 'Substantivo', 'Verbo', 'Preposição', 'Adjetivo', 'Advérbio', 'Conjunção'])
        self.categoria = QLineEdit()
        self.categoria.setPlaceholderText("Inserir o contexto ao qual pertence a palavra")
        self.genero = QComboBox()
        self.genero.addItems(['-', 'Masculino', 'Feminino', 'Neutro'])
        self.plv_sing_pt = QLineEdit()
        self.plv_sing_de = QLineEdit()
        self.plv_plur_pt = QLineEdit()
        self.plv_plur_de = QLineEdit()
        self.observacoes = QTextEdit()
        self.txt_ex_pt_presente = QTextEdit()
        self.txt_ex_de_presente = QTextEdit()
        self.txt_ex_pt_passado = QTextEdit()
        self.txt_ex_de_passado = QTextEdit()
        self.txt_ex_pt_futuro = QTextEdit()
        self.txt_ex_de_futuro = QTextEdit()
        self.txt_ex_pt_presente.setMaximumSize(QSize(1360,30))
        self.txt_ex_de_presente.setMaximumSize(QSize(1360, 30))
        self.txt_ex_pt_passado.setMaximumSize(QSize(1360, 30))
        self.txt_ex_de_passado.setMaximumSize(QSize(1360, 30))
        self.txt_ex_pt_futuro.setMaximumSize(QSize(1360, 30))
        self.txt_ex_de_futuro.setMaximumSize(QSize(1360, 30))

        self.layout_palavras.addWidget(self.lbl_tipo,0,0)
        self.layout_palavras.addWidget(self.tipo,0,1,1,2)
        self.layout_palavras.addWidget(self.lbl_categoria,1,0)
        self.layout_palavras.addWidget(self.categoria,1,1,1,2)
        self.layout_palavras.addWidget(self.lbl_genero,2,0)
        self.layout_palavras.addWidget(self.genero,2,1,1,2)
        self.layout_palavras.addWidget(self.lbl_singular,3,1,1,1,Qt.AlignCenter)
        self.layout_palavras.addWidget(self.lbl_plural,3,2,1,1,Qt.AlignCenter)
        self.layout_palavras.addWidget(self.lbl_plv_portugues,4,0)
        self.layout_palavras.addWidget(self.plv_sing_pt,4,1)
        self.layout_palavras.addWidget(self.plv_plur_pt,4,2)
        self.layout_palavras.addWidget(self.lbl_plv_alemao,5,0)
        self.layout_palavras.addWidget(self.plv_sing_de,5,1)
        self.layout_palavras.addWidget(self.plv_plur_de,5,2)
        self.layout_palavras.addWidget(self.lbl_portugues,6,1,1,1,Qt.AlignCenter)
        self.layout_palavras.addWidget(self.lbl_alemao,6,2,1,1,Qt.AlignCenter)
        self.layout_palavras.addWidget(self.lbl_ex_presente,7,0)
        self.layout_palavras.addWidget(self.txt_ex_pt_presente,7,1)
        self.layout_palavras.addWidget(self.txt_ex_de_presente,7,2)
        self.layout_palavras.addWidget(self.lbl_ex_passado,8,0)
        self.layout_palavras.addWidget(self.txt_ex_pt_passado,8,1)
        self.layout_palavras.addWidget(self.txt_ex_de_passado,8,2)
        self.layout_palavras.addWidget(self.lbl_ex_futuro,9,0)
        self.layout_palavras.addWidget(self.txt_ex_pt_futuro,9,1)
        self.layout_palavras.addWidget(self.txt_ex_de_futuro,9,2)
        self.layout_palavras.addWidget(self.lbl_observacoes,10,0)
        self.layout_palavras.addWidget(self.observacoes,10,1,1,2)
        self.layout_palavras.addWidget(self.btn_add_palavra, 11, 0, 1, 3, Qt.AlignCenter)
        self.layout_palavras.setRowStretch(self.layout_palavras.rowCount(),1)

        # -> Organização do painel de visualização
        self.pn_tabela.setLayout(self.layout_tabela)
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(13)
        self.tabela.setHorizontalHeaderLabels(['ID','TIPO','CATEGORIA','GÊNERO','PALAVRA(PT)','PALAVRA(DE)','PRESENTE(PT)','PRESENTE(DE)','PASSADO(PT)','PASSADO(DE)','FUTURO(PT)','FUTURO(DE)','OBSERVAÇÕES'])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tabela.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.tabela.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.tabela.setColumnWidth(0, 20)
        self.tabela.setColumnWidth(1, 70)
        self.tabela.setColumnWidth(3, 70)
        self.layout_tabela.addWidget(self.tabela)
        self.tabela.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabela.customContextMenuRequested.connect(self._menu_tabela)
        self.tabela.setColumnHidden(0,True)

    def _on_add_banco(self):
        nome = self.line_nome_banco.text().strip()
        parent_id = self.combo_nome_pasta.currentData()
        if nome and parent_id:
            id_banco = self.banco.criar_banco(nome, parent_id)
            for i in range(self.arvore_bancos.topLevelItemCount()):
                item = self.arvore_bancos.topLevelItem(i)
                if item.data(0, Qt.UserRole) == parent_id:
                    filho = QTreeWidgetItem(item, [nome])
                    filho.setIcon(0, QIcon(self.icon_table))
                    filho.setData(0,Qt.UserRole,id_banco)
                    filho.setData(0,Qt.UserRole+1,"banco")
                    item.setExpanded(True)
                    break

    def _renomear_banco(self):
        item = self.arvore_bancos.currentItem()
        if item is not None:
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.arvore_bancos.editItem(item,0)

    def _deletar_banco(self):
        item = self.arvore_bancos.currentItem()
        if item is not None:
            id_banco = item.data(0,Qt.UserRole)
            self.banco.deletar_banco(id_banco)
            parent = item.parent() or self.arvore_bancos.invisibleRootItem()
            parent.removeChild(item)

    def _connect_signals(self):
        self.arvore_bancos.itemChanged.connect(self._on_pasta_renomeada)
        self.btn_add_banco.clicked.connect(self._on_add_banco)
        self.arvore_bancos.itemClicked.connect(self._on_item_selecionado)
        self.btn_add_palavra.clicked.connect(self._on_add_palavra)

    def _on_item_selecionado(self,item,coluna):
        tipo = item.data(0,Qt.UserRole+1)
        if tipo == "banco":
            self.banco_selecionado = item.text(0)
            self._carregar_tabela()
        else:
            self.banco_selecionado = None
            self.tabela.setRowCount(0)

    def _on_add_palavra(self):
        if not self.banco_selecionado:
            QMessageBox.warning(self,"Atenção","Selecione uma tabela à esquerda antes de adicionar uma palavra.")
        else:
            campos_obrigatorios = [
                self.tipo.currentText(),
                self.categoria.text(),
                self.plv_sing_pt.text(),
                self.plv_sing_de.text(),
                self.txt_ex_pt_presente.toPlainText(),
                self.txt_ex_de_presente.toPlainText(),
                self.txt_ex_pt_passado.toPlainText(),
                self.txt_ex_de_passado.toPlainText(),
                self.txt_ex_pt_futuro.toPlainText(),
                self.txt_ex_de_futuro.toPlainText(),
            ]

            if not all(campos_obrigatorios):
                msg_erro = QMessageBox()
                msg_erro.setIcon(QMessageBox.Information)
                msg_erro.setText("Preencha todos os campos obrigatórios")
                msg_erro.setWindowTitle("Aviso!")
                msg_erro.exec_()
                return
            try:
                tipo = self.tipo.currentText()
                categoria = self.categoria.text()
                genero = self.genero.currentText()
                palavra_pt = f"{self.plv_sing_pt.text()}\n{self.plv_plur_pt.text()}"
                palavra_de = f"{self.plv_sing_de.text()}\n{self.plv_plur_de.text()}"
                txt_ex_pt_presente = self.txt_ex_pt_presente.toPlainText()
                txt_ex_de_presente = self.txt_ex_de_presente.toPlainText()
                txt_ex_pt_passado = self.txt_ex_pt_passado.toPlainText()
                txt_ex_de_passado = self.txt_ex_de_passado.toPlainText()
                txt_ex_pt_futuro = self.txt_ex_pt_futuro.toPlainText()
                txt_ex_de_futuro = self.txt_ex_de_futuro.toPlainText()
                observacoes = self.observacoes.toPlainText()

                self.banco.inserir_palavra(self.banco_selecionado, tipo, categoria, genero,
                                           palavra_pt, palavra_de,
                                           txt_ex_pt_presente, txt_ex_de_presente,
                                           txt_ex_pt_passado, txt_ex_de_passado,
                                           txt_ex_pt_futuro, txt_ex_de_futuro,
                                           observacoes)

                msg_ok = QMessageBox()
                msg_ok.setIcon(QMessageBox.Information)
                msg_ok.setText("Palavra inserida!")
                msg_ok.setWindowTitle("Aviso!")
                msg_ok.exec_()

                self._carregar_tabela()

            except Exception as e:
                print(f'Erro ao salvar: {e}')

    def _carregar_tabela(self):
        if not self.banco_selecionado:
            return
        dados = self.banco.buscar_palavras(self.banco_selecionado)
        self.tabela.setRowCount(0)
        self.tabela.setWordWrap(True)
        self.tabela.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        for row_idx, row_data in enumerate(dados):
            self.tabela.insertRow(row_idx)
            for col_idx, valor in enumerate(row_data):
                item = QTableWidgetItem(str(valor) if valor else "")
                self.tabela.setItem(row_idx, col_idx, item)

    def _menu_tabela(self, position):
        item = self.tabela.itemAt(position)
        if item is None:
            return

        menu = QMenu()
        act_editar = menu.addAction("Editar")
        act_remover = menu.addAction("Remover")

        action = menu.exec_(self.tabela.viewport().mapToGlobal(position))

        if action == act_editar:
            self._editar_palavra()
        elif action == act_remover:
            self._remover_palavra()

    def _remover_palavra(self):
        row = self.tabela.currentRow()
        if row < 0:
            return
        id_palavra = int(self.tabela.item(row,0).text())
        self.banco.deletar_palavra(self.banco_selecionado, id_palavra)
        self.tabela.removeRow(row)