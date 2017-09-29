from Tetris.mainFrame import *
from PyQt5.QtWidgets import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
