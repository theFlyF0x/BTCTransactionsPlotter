from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class TablePage(QTableWidget):

    # Custom stylesheet
    style = """
        QHeaderView::section {
            background-color: rgba(0, 40, 118, 0.1);
            border: 1px solid black;
            font-size: 16px;
            gridline-color: black;
            font-weight: 450;
            font-family: cursive;
        }
        
        QTableWidget {
            border: 0.5px solid black;
            font-family: system-ui;
        }
    """

    def __init__(self):
        super(TablePage, self).__init__()
        self.data = None

    def draw_table(self):
        """Draw the table in the page"""
        self.setColumnCount(5)
        self.setRowCount(len(self.data.index))

        self.set_data(self.data)  # Fills up the table
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setStyleSheet(self.style)  # Set the custom stylesheet
        self.color_table()

    def set_data(self, data):
        """Populates the table by parsing the transactions to add cells"""
        data = data.values.tolist()
        for row, transaction in enumerate(data):
            if transaction[0]:  # If transaction was received
                self.setItem(row, 0, QTableWidgetItem('Received'))
                self.setItem(row, 3, QTableWidgetItem(';  \n'.join(transaction[3])))
                self.setItem(row, 4, QTableWidgetItem(transaction[4]))
            else:  # If transaction was sent
                self.setItem(row, 0, QTableWidgetItem('Sent'))
                self.setItem(row, 3, QTableWidgetItem(transaction[3]))
                self.setItem(row, 4, QTableWidgetItem(';  \n'.join(transaction[4])))

            # Set amount and total balance
            self.setItem(row, 1, QTableWidgetItem(str(transaction[1])))
            self.setItem(row, 2, QTableWidgetItem(str(transaction[2])))

        # Set headers of the table
        self.setHorizontalHeaderLabels(['Sent/Received', 'Amount', 'Tot. Balance', 'Sender(s)', 'Receiver(s)'])

    def color_table(self):
        """Colors rows based on the type of transaction"""
        for row in range(self.rowCount()):
            for col in range(4):
                if self.item(row, 0):
                    self.item(row, col).setBackground(QColor(0, 255, 0, 0.34))
                else:
                    self.item(row, col).setBackground(QColor(255, 0, 0, 0.43))
