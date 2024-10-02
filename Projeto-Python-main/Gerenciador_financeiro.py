import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt

# Função para carregar as despesas do arquivo
def carregar_despesas(arquivo):
    despesas = []
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            for linha in f:
                dados = linha.strip().split(';')
                if len(dados) == 4:
                    despesas.append(dados[:3])  # Removendo o último campo vazio
    return despesas

# Função para salvar as despesas no arquivo
def salvar_despesas(arquivo, despesas):
    with open(arquivo, 'w') as f:
        for despesa in despesas:
            f.write(';'.join(map(str, despesa)) + ';\n')

# Classe principal do aplicativo
class GerenciadorFinanceiro(QMainWindow):
    def __init__(self):
        super().__init__()

        self.despesas = carregar_despesas('base_despesas.txt')
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gerenciador Financeiro")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #A020F0;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #A020F0;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #A020F0;
                color: white;
                padding: 5px;
                border: none;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout para formulário de entrada
        form_layout = QHBoxLayout()
        
        # Descrição
        self.descricao_label = QLabel("Descrição:")
        self.descricao_input = QLineEdit()
        self.descricao_input.setPlaceholderText("Ex: Mercado")
        form_layout.addWidget(self.descricao_label)
        form_layout.addWidget(self.descricao_input)
        
        # Valor
        self.valor_label = QLabel("Valor:")
        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("Ex: 100.0")
        form_layout.addWidget(self.valor_label)
        form_layout.addWidget(self.valor_input)
        
        # Data
        self.data_label = QLabel("Data:")
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("Ex: 23/10/2023")
        form_layout.addWidget(self.data_label)
        form_layout.addWidget(self.data_input)
        
        # Botão de adicionar despesa
        self.adicionar_btn = QPushButton("Adicionar")
        self.adicionar_btn.clicked.connect(self.adicionar_despesa)
        form_layout.addWidget(self.adicionar_btn)

        # Tabela de despesas
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Descrição", "Valor", "Data"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.atualizar_tabela()

        # Layout de botões de ação (Salvar e Remover)
        action_layout = QHBoxLayout()

        # Botão de salvar despesas
        self.salvar_btn = QPushButton("Salvar")
        self.salvar_btn.clicked.connect(self.salvar_despesas)
        action_layout.addWidget(self.salvar_btn)

        # Botão de remover despesa
        self.remover_btn = QPushButton("Remover")
        self.remover_btn.clicked.connect(self.remover_despesa)
        action_layout.addWidget(self.remover_btn)

        # Adicionar layouts no layout principal
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(action_layout)

        # Definir o widget central
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def atualizar_tabela(self):
        """Atualiza a tabela com as despesas carregadas."""
        self.table.setRowCount(len(self.despesas))
        for i, (descricao, valor, data) in enumerate(self.despesas):
            self.table.setItem(i, 0, QTableWidgetItem(descricao))
            self.table.setItem(i, 1, QTableWidgetItem(str(valor)))
            self.table.setItem(i, 2, QTableWidgetItem(data))

    def adicionar_despesa(self):
        """Adiciona uma nova despesa à lista e à tabela."""
        descricao = self.descricao_input.text()
        valor = self.valor_input.text()
        data = self.data_input.text()

        if descricao and valor and data:
            try:
                valor_float = float(valor)
                self.despesas.append([descricao, valor_float, data])
                self.atualizar_tabela()
                self.limpar_campos()
            except ValueError:
                QMessageBox.critical(self, "Erro", "Por favor, insira um valor numérico válido.")
        else:
            QMessageBox.critical(self, "Erro", "Preencha todos os campos!")

    def limpar_campos(self):
        """Limpa os campos de entrada."""
        self.descricao_input.clear()
        self.valor_input.clear()
        self.data_input.clear()

    def remover_despesa(self):
        """Remove a despesa selecionada."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            resposta = QMessageBox.question(
                self, "Remover despesa", "Tem certeza que deseja remover essa despesa?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if resposta == QMessageBox.Yes:
                self.despesas.pop(selected_row)
                self.atualizar_tabela()
        else:
            QMessageBox.warning(self, "Erro", "Por favor, selecione uma despesa para remover.")

    def salvar_despesas(self):
        """Salva as despesas no arquivo."""
        salvar_despesas('base_despesas.txt', self.despesas)
        QMessageBox.information(self, "Sucesso", "Despesas salvas com sucesso!")


# Função principal
def main():
    app = QApplication(sys.argv)
    window = GerenciadorFinanceiro()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
