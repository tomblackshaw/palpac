'''
Created on Jun 2, 2024

@author: Tom Blackshaw
'''

from PyQt5.QtWidgets import QMainWindow, QApplication

import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Temperature vs time plot
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        self.plot_graph.plot(time, temperature)


if __name__ == '__main__':
    app = QApplication([])
    main = MainWindow()
    main.show()
    app.exec()

