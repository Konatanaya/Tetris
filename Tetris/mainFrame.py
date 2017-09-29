from Tetris.Board import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.board = Board()
        # Status
        self.statusBar().showMessage('Ready')

        vbox = QVBoxLayout()
        # vbox.addWidget(self.board)
        self.setCentralWidget(self.board)
        self.setLayout(vbox)
        self.resize(600, 800)
        self.center()
        self.Menubar()
        self.setWindowTitle('Tetris')
        self.show()

    def Menubar(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


