from PyQt5.QtWidgets import QWidget, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd


class GraphPage(QWidget):

    def __init__(self, data):
        super(GraphPage, self).__init__()
        self.data = data

        self.figure = plt.figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)

        self.grid = QGridLayout()
        self.grid.addWidget(self.canvas)
        self.setLayout(self.grid)

        axes = plt.subplot()
        history = self.__process_data(self.data)

        # Labelling
        axes.set_title("Balance history of the selected account")
        axes.set_xlabel("Transactions")
        axes.set_ylabel("Total balance")

        # Styling
        fill = axes.fill_between(range(len(history)), history)
        fill.set_facecolor((.5, .5, .8, .3))
        fill.set_edgecolor((0, 0, .5, .3))
        fill.set_linewidth(3)
        axes.set_xlim(0, len(history))
        axes.set_ylim(0, max(history)*1.5)
        axes.set_xticks(range(0, len(history), 2))
        axes.xaxis.set_tick_params(size=0)
        axes.yaxis.set_tick_params(size=0)
        axes.spines['right'].set_color((.8, .8, .8))
        axes.spines['top'].set_color((.8, .8, .8))
        axes.ticklabel_format(style='plain')
        axes.xaxis.get_label().set_style('italic')
        axes.yaxis.get_label().set_style('italic')
        axes.xaxis.get_label().set_size(10)
        axes.yaxis.get_label().set_size(10)
        axes.title.set_weight('bold')

        axes.plot(range(len(history)), history)

    def __process_data(self, data):
        """Takes the full dataframe to return only history of balance"""
        money = [amount for amount in data['Balance']]
        return money[::-1]
