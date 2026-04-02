from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QComboBox, QLineEdit, QCheckBox, QPushButton, \
    QMessageBox, QCompleter, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QLabel, QFrame
from utils.formatter import formatar_palavra

class MainWindow(QMainWindow):
    def __init__(self, banco):
        super().__init__()
        self.setWindowTitle('Dicionário Anki')
        self.setMinimumSize(1000,800)
        self.banco = banco
        self._setup_ui()
        self._connect_signals()
        self._atualizar_tabela()

    def _setup_ui(self):
        #Organização dos Layouts
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.form_layout = QFormLayout()
        self.main_layout.addLayout(self.form_layout)
        self.filtro_layout = QHBoxLayout()
        self.main_layout.addLayout(self.filtro_layout)
        #Objetos criados dentro de cada layout
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(['Substantivo','Verbo','Adjetivo','Advérbio','Preposição','Conjunção'])
        self.form_layout.addRow('Tipo', self.combo_tipo)
        self.input_categoria = QLineEdit()
        self.input_categoria.setPlaceholderText('Inserir categoria que a palavra se encaixa...')
        categorias = self.banco.buscar_categorias()
        completer = QCompleter(categorias)
        self.input_categoria.setCompleter(completer)
        self.form_layout.addRow('Categoria', self.input_categoria)
        self.combo_genero = QComboBox()
        self.combo_genero.addItems(['Masculino','Feminino','Neutro'])
        self.form_layout.addRow('Gênero', self.combo_genero)
        self.input_palavra_pt = QLineEdit()
        self.input_palavra_pt.setPlaceholderText('Inserir palavra em português...')
        self.form_layout.addRow('Palavra em PT', self.input_palavra_pt)
        self.input_palavra_de = QLineEdit()
        self.input_palavra_de.setPlaceholderText('Inserir palavra em alemão...')
        self.form_layout.addRow('Palavra em DE', self.input_palavra_de)
        self.input_exemplo_pt = QLineEdit()
        self.input_exemplo_pt.setPlaceholderText('Inserir um exemplo em português...')
        self.form_layout.addRow('Exemplo em PT', self.input_exemplo_pt)
        self.input_exemplo_de = QLineEdit()
        self.input_exemplo_de.setPlaceholderText('Inserir um exemplo em alemão...')
        self.form_layout.addRow('Exemplo em DE', self.input_exemplo_de)
        self.input_anki_check = QCheckBox()
        self.input_anki_check.setChecked(False)
        self.form_layout.addRow('Palavra já foi inserida no Banco?', self.input_anki_check)
        self.output_formatted = QLineEdit()
        self.output_formatted.setReadOnly(True)
        self.form_layout.addRow('Texto para Anki', self.output_formatted)
        self.btn_salvar = QPushButton('Salvar no Banco de Dados')
        self.form_layout.addWidget(self.btn_salvar)
        # Objetos do Layout Horizontal:
        self.label_filtro = QLabel()
        self.label_filtro.setText("Filtro para Tipo de Palavra:")
        self.filtro_layout.addWidget(self.label_filtro)
        self.tipos_combo = QComboBox()
        self.tipos_combo.addItems(['Todos','Substantivo','Verbo','Adjetivo','Advérbio','Preposição','Conjunção'])
        self.filtro_layout.addWidget(self.tipos_combo)
        self.label_palavra = QLabel()
        self.label_palavra.setText("Inserir palavra de filtro:")
        self.filtro_layout.addWidget(self.label_palavra)
        self.input_palavra_filtro = QLineEdit()
        self.filtro_layout.addWidget(self.input_palavra_filtro)
        # Objetos do Layout Main:
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(9)
        self.tabela.setHorizontalHeaderLabels(['ID','TIPO','CATEGORIA','GÊNERO','PALAVRA_PT','PALAVRA_DE','EXEMPLO_PT','EXEMPLO_DE','ANKI'])
        self.main_layout.addWidget(self.tabela)
        self.tabela.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #5a5a5a; color: white; font-weight: bold; padding: 4px; }"
        )
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _connect_signals(self):
        self.combo_tipo.currentTextChanged.connect(self._on_tipo_changed)
        self.combo_tipo.currentTextChanged.connect(self._on_palavra_de_changed)
        self.input_palavra_de.textChanged.connect(self._on_palavra_de_changed)
        self.combo_genero.currentTextChanged.connect(self._on_palavra_de_changed)
        self.btn_salvar.clicked.connect(self._on_salvar)
        self.tipos_combo.currentTextChanged.connect(self._atualizar_tabela)
        self.input_palavra_filtro.textChanged.connect(self._atualizar_tabela)


    def _on_tipo_changed(self, texto):
        if texto != 'Substantivo':
            self.combo_genero.setVisible(False)
        else:
            self.combo_genero.setVisible(True)

    def _on_palavra_de_changed(self):
        saida = formatar_palavra(self.combo_tipo.currentText(),self.input_palavra_de.text(),self.combo_genero.currentText())
        self.output_formatted.setText(saida)

    def _on_salvar(self):

        # Primeira Etapa é verificar se existem campos vazios
        campos_obrigatorios = [
            self.combo_tipo.currentText(),
            self.input_categoria.text(),
            self.input_palavra_pt.text(),
            self.input_palavra_de.text(),
            self.input_exemplo_pt.text(),
            self.input_exemplo_de.text()
        ]

        if not all(campos_obrigatorios):
            msg_erro = QMessageBox()
            msg_erro.setIcon(QMessageBox.Information)
            msg_erro.setText("Preencha todos os campos obrigatórios")
            msg_erro.setWindowTitle("Aviso!")
            msg_erro.exec_()
            return

        # Segunda Etapa é verificar se existem palavras similares
        lista_similares = self.banco.verificar_similares(self.input_palavra_pt.text())

        if lista_similares:
            resposta = QMessageBox.question(self, "Atenção", f"Palavras similares encontradas: {lista_similares}\nDeseja continuar?", QMessageBox.Yes | QMessageBox.No)

            if resposta == QMessageBox.No:
                return

        try:
            tipo = self.combo_tipo.currentText()
            categoria = self.input_categoria.text()
            genero = self.combo_genero.currentText() if tipo == 'Substantivo' else None
            palavra_pt = self.input_palavra_pt.text()
            palavra_de = self.input_palavra_de.text()
            exemplo_pt = self.input_exemplo_pt.text()
            exemplo_de = self.input_exemplo_de.text()

            self.banco.inserir_palavra(tipo,categoria,genero,palavra_pt,palavra_de,exemplo_pt,exemplo_de)

            msg_ok = QMessageBox()
            msg_ok.setIcon(QMessageBox.Information)
            msg_ok.setText(f"Palavra {self.input_palavra_pt.text()} inserida com sucesso!")
            msg_ok.setWindowTitle("Aviso!")
            msg_ok.exec_()
            self._limpar_campos()
            self._atualizar_tabela()

        except Exception as e:
            print(f'Erro ao salvar: {e}')

    def _limpar_campos(self):
        self.input_categoria.clear()
        self.input_palavra_pt.clear()
        self.input_palavra_de.clear()
        self.input_exemplo_pt.clear()
        self.input_exemplo_de.clear()

    def _atualizar_tabela(self):
        tipo = self.tipos_combo.currentText()
        tipo = None if tipo == 'Todos' else tipo
        lista_completa = self.banco.buscar_filtrado(tipo,self.input_palavra_filtro.text())
        self.tabela.setRowCount(len(lista_completa))

        for linha_idx, linha in enumerate(lista_completa):
            for coluna_idx, valor in enumerate(linha):
                item_widget = QTableWidgetItem(str(valor))
                if coluna_idx == 0:
                    item_widget.setTextAlignment(Qt.AlignCenter)
                self.tabela.setItem(linha_idx, coluna_idx, item_widget)