import sys
import pandas as pd
from NetworkPage import NetworkPage
from TablePage import TablePage
from GraphPage import GraphPage
from PyQt5.QtWidgets import QApplication, QTabWidget, QStyleFactory, QWidget, QGridLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QGroupBox


# bc1qw9uxxvkf6qk98ly5u0s4ehtl5cf8wjl0jy6cql

class MainPage(QWidget):

    BASE_URL = 'https://blockchain.info/rawaddr/'

    def __init__(self):
        super(MainPage, self).__init__()

        self.address = ""

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

        button.clicked.connect(self.retrieve_transactions)

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

    def retrieve_transactions(self):
        print('sus')
        self.address = self.textbox.text()
        full_url = self.BASE_URL + self.address

        content = pd.read_json(full_url)
        self.process_data(content['txs'])

    def process_data(self, transactions):
        """Processes the data retrieved from APIs to retrieve only useful parameters"""
        data = list()
        for transaction in transactions:  # Extraction of useful data from the original dataframe
            record = dict()
            amount = transaction['result']
            record['IsReceived'] = amount > 0
            record['Amount'] = amount
            record['Balance'] = transaction['balance']

            # Checking if the selected address is a sender or a receiver
            senders = []
            recipients = []
            if record['IsReceived']:
                senders = self.get_senders(transaction)
                recipients = self.address
            else:
                senders = self.address
                recipients = self.get_recipients(transaction)

            record['Senders'] = senders
            record['Recipients'] = recipients

            data.append(record)

        self.set_pages(pd.DataFrame(data))  # Final DataFrame processed

    def set_pages(self, transactions):
        """Sets the pages of the UI"""
        self.network.address = self.address
        self.network.transactions = transactions
        self.network.draw_network()
        self.table.data = transactions
        self.table.draw_table()
        self.graph.data = transactions
        self.graph.draw_graph()

    def get_senders(self, transaction):
        """Returns all the sender addresses in a transaction"""
        senders = list()
        for send in transaction['inputs']:
            senders.append(send['prev_out']['addr'])
        return senders

    def get_recipients(self, transaction):
        """Returns all the recipient addresses in a transaction"""
        recipients = list()
        for recpt in transaction['out']:
            recipients.append(recpt['addr'])
        return recipients


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("gtk"))  # idk what this does...

    page = MainPage()
    page.show()

    sys.exit(app.exec_())
