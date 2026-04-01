from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QComboBox, QLineEdit, QCheckBox, QPushButton
from utils.formatter import formatar_palavra

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dicionário Anki')
        self.setMinimumSize(600,800)
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
        self.layout.addRow('Categoria',self.input_categoria)
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
        pass