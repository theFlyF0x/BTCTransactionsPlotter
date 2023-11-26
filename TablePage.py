from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class TablePage(QTableWidget):

    def __init__(self, data):
        super(TablePage, self).__init__()
        self.data = data.values.tolist()

        self.setColumnCount(5)
        self.setRowCount(len(data.index))

        self.set_data(self.data)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()


    def set_data(self, data):
        for row, transaction in enumerate(data):
            if transaction[0]:
                self.setItem(row, 0, QTableWidgetItem('Sent'))
                self.setItem(row, 3, QTableWidgetItem(';  '.join(transaction[3])))
                self.setItem(row, 4, QTableWidgetItem(transaction[4]))
            else:
                self.setItem(row, 0, QTableWidgetItem('Received'))
                self.setItem(row, 3, QTableWidgetItem(transaction[3]))
                self.setItem(row, 4, QTableWidgetItem(';  '.join(transaction[4])))

            self.setItem(row, 1, QTableWidgetItem(str(transaction[1])))
            self.setItem(row, 2, QTableWidgetItem(str(transaction[2])))

        self.setHorizontalHeaderLabels(['Sent/Received', 'Amount', 'Tot. Balance', 'Sender(s)', 'Receiver(s)'])
