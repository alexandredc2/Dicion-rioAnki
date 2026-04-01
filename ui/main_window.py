from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QComboBox, QLineEdit, QCheckBox, QPushButton, \
    QMessageBox, QCompleter
from utils.formatter import formatar_palavra

class MainWindow(QMainWindow):
    def __init__(self, banco):
        super().__init__()
        self.setWindowTitle('Dicionário Anki')
        self.setMinimumSize(600,800)
        self.banco = banco
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QFormLayout()
        self.central_widget.setLayout(self.layout)
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(['Substantivo','Verbo','Adjetivo','Advérbio','Preposição','Conjunção'])
        self.layout.addRow('Tipo',self.combo_tipo)
        self.input_categoria = QLineEdit()
        self.input_categoria.setPlaceholderText('Inserir categoria que a palavra se encaixa...')
        categorias = self.banco.buscar_categorias()
        completer = QCompleter(categorias)
        self.input_categoria.setCompleter(completer)
        self.layout.addRow('Categoria', self.input_categoria)
        self.combo_genero = QComboBox()
        self.combo_genero.addItems(['Masculino','Feminino','Neutro'])
        self.layout.addRow('Gênero',self.combo_genero)
        self.input_palavra_pt = QLineEdit()
        self.input_palavra_pt.setPlaceholderText('Inserir palavra em português...')
        self.layout.addRow('Palavra em PT',self.input_palavra_pt)
        self.input_palavra_de = QLineEdit()
        self.input_palavra_de.setPlaceholderText('Inserir palavra em alemão...')
        self.layout.addRow('Palavra em DE', self.input_palavra_de)
        self.input_exemplo_pt = QLineEdit()
        self.input_exemplo_pt.setPlaceholderText('Inserir um exemplo em português...')
        self.layout.addRow('Exemplo em PT', self.input_exemplo_pt)
        self.input_exemplo_de = QLineEdit()
        self.input_exemplo_de.setPlaceholderText('Inserir um exemplo em alemão...')
        self.layout.addRow('Exemplo em DE', self.input_exemplo_de)
        self.input_anki_check = QCheckBox()
        self.input_anki_check.setChecked(False)
        self.layout.addRow('Palavra já foi inserida no Banco?', self.input_anki_check)
        self.output_formatted = QLineEdit()
        self.output_formatted.setReadOnly(True)
        self.layout.addRow('Texto para Anki', self.output_formatted)
        self.btn_salvar = QPushButton('Salvar no Banco de Dados')
        self.layout.addWidget(self.btn_salvar)

    def _connect_signals(self):
        self.combo_tipo.currentTextChanged.connect(self._on_tipo_changed)
        self.combo_tipo.currentTextChanged.connect(self._on_palavra_de_changed)
        self.input_palavra_de.textChanged.connect(self._on_palavra_de_changed)
        self.combo_genero.currentTextChanged.connect(self._on_palavra_de_changed)
        self.btn_salvar.clicked.connect(self._on_salvar)

    def _on_tipo_changed(self, texto):
        if texto != 'Substantivo':
            self.combo_genero.setVisible(False)
        else:
            self.combo_genero.setVisible(True)

    def _on_palavra_de_changed(self):
        saida = formatar_palavra(self.combo_tipo.currentText(),self.input_palavra_de.text(),self.combo_genero.currentText())
        self.output_formatted.setText(saida)

    def _on_salvar(self):
        try:
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

        except Exception as e:
            print(f'Erro ao salvar: {e}')

    def _limpar_campos(self):
        self.input_categoria.clear()
        self.input_palavra_pt.clear()
        self.input_palavra_de.clear()
        self.input_exemplo_pt.clear()
        self.input_exemplo_de.clear()