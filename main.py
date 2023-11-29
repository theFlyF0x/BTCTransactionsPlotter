import sys
import pandas as pd
from NetworkPage import NetworkPage
from TablePage import TablePage
from GraphPage import GraphPage
from PyQt5.QtWidgets import QApplication, QTabWidget, QStyleFactory, QWidget, QGridLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QGroupBox
from utils import retrieve_transactions, process_data


class MainPage(QWidget):

    def __init__(self):
        super(MainPage, self).__init__()

        self.address = ""
        self.created = False

        grid = QGridLayout()
        self.setLayout(grid)
        self.resize(1350, 1000)  # Size of the window. Should be changed eventually

        # Upper section with input box for address
        upper_layout = QHBoxLayout()
        self.textbox = QLineEdit()
        upper_layout.addWidget(self.textbox)
        button = QPushButton('Go')
        upper_layout.addWidget(button)
        upper_section = QGroupBox()
        upper_section.setLayout(upper_layout)
        grid.addWidget(upper_section, 0, 0)

        button.clicked.connect(self.on_click)

        # Lower portion of the screen with tabs for the content
        tabs = QTabWidget()
        tabs.setWindowTitle("BTC Transactions Plotter")
        self.network = NetworkPage()
        tabs.addTab(self.network, "Network")  # First tab - network page
        self.table = TablePage()
        tabs.addTab(self.table, "Table View")  # Second tab - table page
        self.graph = GraphPage()
        tabs.addTab(self.graph, "Graph View")  # Third tab - graph page
        grid.addWidget(tabs, 1, 0)

    def on_click(self):
        """Actions performed on click of button"""
        self.address = self.textbox.text()
        raw_transactions = retrieve_transactions(self.address)
        transactions = process_data(raw_transactions, self.address)

        self.set_pages(transactions)

    def set_pages(self, transactions):
        """Sets the pages of the UI"""
        if self.created:  # If data is already inserted, clear it
            self.network.clear_network()
            self.table.clear_table()
            self.graph.figure.clear()

        self.network.address = self.address
        self.network.transactions = transactions
        self.network.draw_network()
        self.table.data = transactions
        self.table.draw_table()
        self.graph.data = transactions
        self.graph.draw_graph()

        self.created = True


if __name__ == '__main__':

    app = QApplication(sys.argv)  # Create main object
    app.setStyle(QStyleFactory.create("Fusion"))  # Set style of the window

    page = MainPage()
    page.show()  # Show the contents of the page

    sys.exit(app.exec_())
