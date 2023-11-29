from PyQt5.QtWidgets import QWidget, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class GraphPage(QWidget):

    def __init__(self):
        super(GraphPage, self).__init__()
        self.data = None

        self.figure = plt.figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        self.grid = QGridLayout()
        self.axes = plt.subplot()

    def draw_graph(self):
        """Draw the graph in the page"""

        self.grid.addWidget(self.canvas)
        self.setLayout(self.grid)

        history = self.__process_data(self.data)

        # Labelling
        self.axes.set_title("Balance history of the selected account")
        self.axes.set_xlabel("Transactions")
        self.axes.set_ylabel("Total balance")

        # Styling
        fill = self.axes.fill_between(range(len(history)), history)
        fill.set_facecolor((.5, .5, .8, .3))
        fill.set_edgecolor((0, 0, .5, .3))
        fill.set_linewidth(3)
        self.axes.set_xlim(0, len(history))
        self.axes.set_ylim(0, max(history) * 1.5)
        self.axes.set_xticks(range(0, len(history), 2))
        self.axes.xaxis.set_tick_params(size=0)
        self.axes.yaxis.set_tick_params(size=0)
        self.axes.spines['right'].set_color((.8, .8, .8))
        self.axes.spines['top'].set_color((.8, .8, .8))
        self.axes.ticklabel_format(style='plain')
        self.axes.xaxis.get_label().set_style('italic')
        self.axes.yaxis.get_label().set_style('italic')
        self.axes.xaxis.get_label().set_size(10)
        self.axes.yaxis.get_label().set_size(10)
        self.axes.title.set_weight('bold')

        self.axes.plot(range(len(history)), history)

    def __process_data(self, data):
        """Takes the full dataframe to return only history of balance"""
        money = [amount for amount in data['Balance']]
        return money[::-1]
