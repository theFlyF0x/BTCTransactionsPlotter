from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class NetworkPage(QWidget):
    
    def __init__(self):
        super(NetworkPage, self).__init__()
        font = QFont()
        self.address = ''
        self.transactions = None

    def draw_network(self):  # TODO rethink a pair of things
        """Draws the network in the page"""
        grid = QGridLayout()
        self.setLayout(grid)
        #self.createVerticalGroupBox()

        buttonLayout = QVBoxLayout()  # TODO place in a button box for graph interaction
        #buttonLayout.addWidget(self.verticalGroupBox)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1)
        grid.addLayout(buttonLayout, 0, 0)

        graph = nx.DiGraph()
        for i, element in self.transactions.iterrows():  # Add edges to the network
            if element['IsReceived']:
                for sender in element['Senders']:  # Multiple senders handling
                    graph.add_edge(self.address, sender, is_received=True)
            else:
                for recipient in element['Recipients']:  # Multiple recipients handling
                    graph.add_edge(self.address, recipient, is_received=False)

        center_node = self.address
        edge_nodes = set(graph) - {center_node}
        pos = nx.circular_layout(graph.subgraph(edge_nodes))
        pos[center_node] = np.array([0, 0])

        options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9}
        # Color nodes
        green, red, yellow = self.__get_colors(self.transactions)
        nx.draw_networkx_nodes(graph, pos, nodelist=green, node_color="tab:green", **options)
        nx.draw_networkx_nodes(graph, pos, nodelist=red, node_color="tab:red", **options)
        nx.draw_networkx_nodes(graph, pos, nodelist=yellow, node_color="tab:yellow", **options)

        nx.draw_networkx_edges(graph, pos, arrows=False)  # Draw edges
        nx.draw_networkx_labels(graph, pos, self.__get_labels(set(graph)))  # Process labels and place them

        legend = [  # Contents of the legend
            Line2D([0], [0], marker='o', color='w', label='Transaction Sent to', markerfacecolor='r', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='Transaction Received from', markerfacecolor='g',
                   markersize=15),
            Line2D([0], [0], marker='o', color='w', label='Both Received and Sent to', markerfacecolor='y',
                   markersize=15),
        ]

        plt.title('BTC addresses linked to ' + self.address)
        plt.legend(handles=legend, loc='upper right')
        plt.axis('off')

    def __get_labels(self, addresses):
        """Returns the shortened BTC addresses for better readability"""
        labels = dict()
        for address in addresses:
            labels[address] = address[0:3] + '-' + address[-4:-1]
        return labels

    def __get_colors(self, transactions):
        """Sorts the colors based on whether coins were received, sent or both"""
        green, red, yellow = [], [], []
        for _, transaction in transactions.iterrows():  # loop all the edges in the network
            # Check if the address was already processed
            if transaction['IsReceived']:
                for tr in transaction['Senders']:
                    if tr in red:
                        yellow.append(tr)
                        red.remove(tr)
                    else:
                        green.append(tr)
            else:
                for tr in transaction['Recipients']:
                    if tr in green:
                        yellow.append(tr)
                        green.remove(tr)
                    else:
                        red.append(tr)

        return green, red, yellow

    def createVerticalGroupBox(self):  # TODO rewrite this copy-pasted code
        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()
        for i in  self.NumButtons:
            button = QPushButton(i)
            button.setObjectName(i)
            layout.addWidget(button)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)
            button.clicked.connect(self.submitCommand)
