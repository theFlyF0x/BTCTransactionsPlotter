import sys
import pandas as pd
import networkx as nx
from NetworkPage import NetworkPage
from TablePage import TablePage
from GraphPage import GraphPage
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

BASE_URL = 'https://blockchain.info/rawaddr/'

address = 'bc1qw9uxxvkf6qk98ly5u0s4ehtl5cf8wjl0jy6cql'  # Selected address. TODO make this selectable by user
full_url = BASE_URL + address

content = pd.read_json(full_url)
transactions = content['txs']


def get_senders(transaction):
    """Returns all the sender addresses in a transaction"""
    senders = list()
    for send in transaction['inputs']:
        senders.append(send['prev_out']['addr'])
    return senders


def get_recipients(transaction):
    """Returns all the recipient addresses in a transaction"""
    recipients = list()
    for recpt in transaction['out']:
        recipients.append(recpt['addr'])
    return recipients


if __name__ == '__main__':
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
            senders = get_senders(transaction)
            recipients = address
        else:
            senders = address
            recipients = get_recipients(transaction)

        record['Senders'] = senders
        record['Recipients'] = recipients

        data.append(record)

    table_of_transactions = pd.DataFrame(data)  # Final DataFrame processed

    graph = nx.DiGraph()
    for i, element in table_of_transactions.iterrows():  # Add edges to the network
        if element['IsReceived']:
            for sender in element['Senders']:  # Multiple senders handling
                graph.add_edge(address, sender, is_received=True)
        else:
            for recipient in element['Recipients']:  # Multiple recipients handling
                graph.add_edge(address, recipient, is_received=False)

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("gtk"))  # idk what this does...

    tabs = QTabWidget()  # Object for multiple tabs in a page
    tabs.resize(1350, 1000)  # Size of the window. Should be changed eventually
    tabs.setWindowTitle("BTC Transacions Plotter")
    tabs.addTab(NetworkPage(graph, address, table_of_transactions), "Network")  # First tab
    tabs.addTab(TablePage(table_of_transactions), "Table View")  # Second tab
    tabs.addTab(GraphPage(table_of_transactions), "Graph View")  # Third tab
    tabs.show()

    sys.exit(app.exec_())
