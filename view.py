from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class UserInterface(QWidget):
    
    def __init__(self, graph, address):
        super(UserInterface, self).__init__()
        font = QFont()
        self.graph = graph
        self.address = address

    def initUI(self):
        self.setGeometry(100, 100, 1300, 1100)
        self.center()
        self.setWindowTitle('Titolo')

        grid = QGridLayout()
        self.setLayout(grid)
        #self.createVerticalGroupBox()

        buttonLayout = QVBoxLayout()
        #buttonLayout.addWidget(self.verticalGroupBox)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)
        grid.addLayout(buttonLayout, 0, 0)

        center_node = self.address
        edge_nodes = set(self.graph) - {center_node}
        pos = nx.circular_layout(self.graph.subgraph(edge_nodes))
        pos[center_node] = np.array([0, 0])
        options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9}
        nx.draw(self.graph, pos, with_labels=False, **options)
        nx.draw_networkx_labels(self.graph, pos, self.__get_labels(set(self.graph)))

        plt.title('BTC addresses linked to ' + self.address)
        plt.legend(scatterpoints=1)
        plt.axis('off')

    def __get_labels(self, addresses):
        labels = dict()
        for address in addresses:
            labels[address] = address[0:3] + '-' + address[-4:-1]
        return labels

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createVerticalGroupBox(self):
        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()
        for i in  self.NumButtons:
            button = QPushButton(i)
            button.setObjectName(i)
            layout.addWidget(button)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)
            button.clicked.connect(self.submitCommand)