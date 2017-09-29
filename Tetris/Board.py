from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Tetris.Shape import *
import sys, random


class gameBoard(QWidget):
    Width = 20
    Height = 40
    speed = 300

    def __init__(self):
        super(gameBoard, self).__init__()
        self.initFunctionBoard()
        self.initUI()
        self.initBoard()
        # self.startGame()

    def initUI(self):
        palette = QPalette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setFixedWidth(400)


    def initFunctionBoard(self):

        self.functionBoard = QWidget()
        palette = QPalette()
        palette.setColor(self.functionBoard.backgroundRole(), QColor(192, 253, 123))
        self.functionBoard.setPalette(palette)
        self.functionBoard.setAutoFillBackground(True)

        self.functionBoard.setFixedWidth(200)
        label = QLabel('<p style=\'color: red; text-align: center; font-size: 18pt\'><b>Next Shape</b></p>')
        cb = controlBar(self)
        self.shapeBoard = nextShapeBoard()
        self.labelScore = QLabel('<p style=\'color: red; text-align: center; font-size: 18pt\'><b>0</b></p>')
        btn = QPushButton('New Game', self)
        btn.clicked.connect(self.startClicked)
        hbox = QHBoxLayout()
        hbox.addWidget(self.shapeBoard)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addLayout(hbox)
        vbox.addWidget(cb)
        vbox.addWidget(self.labelScore)
        vbox.addStretch(1)
        vbox.addWidget(btn)
        self.functionBoard.setLayout(vbox)

    def setSpeed(self, value):
        self.speed = value

    def setScore(self, value):
        self.labelScore.setText('<p style=\'color: red; text-align: center; font-size: 18pt\'><b>'+str(value)+'</b></p>')

    def startClicked(self):
        self.startGame()
        self.clearBoard()

    def initBoard(self):
        self.isStarted = False
        self.isPaused = False
        self.isReached = False
        self.timer = QBasicTimer()
        self.RemovedLine = 0
        self.blockList = []
        self.clearBoard()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setNextShape()
        self.currentShape = None
        self.x = 0
        self.y = 0

    def paintEvent(self, e):
        if self.isStarted:
            painter = QPainter(self)
            rect = self.contentsRect()
            boardTop = rect.bottom() - self.Height * self.getBlockHeight()
            for i in range(self.Height):
                for j in range(self.Width):
                    shapeA = self.getBlockAt(j, self.Height - i - 1)
                    if shapeA != block.NoShape:
                        self.drawBlock(painter,
                                       rect.left() + j * self.getBlockWidth(),
                                       boardTop + (self.Height - i - 1) * self.getBlockHeight(),
                                       shapeA)

            if self.currentShape.getShape() != block.NoShape:
                for i in range(4):
                    blockx = self.x + self.currentShape.getBlockX(i)
                    blocky = self.y - self.currentShape.getBlockY(i)
                    self.drawBlock(painter, rect.left() + blockx * self.getBlockWidth(),
                                   boardTop + blocky * self.getBlockHeight(),
                                   self.currentShape.getShape())

    def timerEvent(self, e):
        if self.isStarted:
            if e.timerId() == self.timer.timerId():
                if self.isReached:
                    self.isReached = False
                    self.newShape()
                else:
                    self.autoDrop()
            else:
                super(gameBoard, self).timerEvent(e)

    def keyPressEvent(self, e):
        if not self.isStarted or self.currentShape == block.NoShape:
            super(gameBoard, self).keyPressEvent(e)
            return

        key = e.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        if key == Qt.Key_Left:
            self.move(self.currentShape, self.x - 1, self.y)
        elif key == Qt.Key_Right:
            self.move(self.currentShape, self.x + 1, self.y)
        elif key == Qt.Key_Up:
            self.move(self.currentShape.rotateL(), self.x, self.y)
        elif key == Qt.Key_Down:
            self.move(self.currentShape.rotateR(), self.x, self.y)
        elif key == Qt.Key_Space:
            self.immeDrop()
        elif key == Qt.Key_D:
            self.autoDrop()
        else:
            super(gameBoard, self).keyPressEvent(e)

    def move(self, newShape, newX, newY):
        for i in range(4):
            nx = newX + newShape.getBlockX(i)
            ny = newY - newShape.getBlockY(i)

            if nx < 0 or nx >= self.Width or ny >= self.Height or ny < 0:
                return False
            if self.getBlockAt(nx, ny) != block.NoShape:
                return False

        self.currentShape = newShape
        self.x = newX
        self.y = newY
        self.update()

        return True

    def immeDrop(self):
        newY = self.y
        while newY > 0:
            if not self.move(self.currentShape, self.x, self.y + 1):
                break

        for i in range(4):
            newX = self.x + self.currentShape.getBlockX(i)
            newY = self.y - self.currentShape.getBlockY(i)
            self.setBlockAt(newX, newY, self.currentShape.getShape())

        self.removeLine()

        if not self.isReached:
            self.newShape()

    def autoDrop(self):
        if not self.move(self.currentShape, self.x, self.y + 1):
            for i in range(4):
                newX = self.x + self.currentShape.getBlockX(i)
                newY = self.y - self.currentShape.getBlockY(i)
                self.setBlockAt(newX, newY, self.currentShape.getShape())

            self.removeLine()

            if not self.isReached:
                self.newShape()

    def removeLine(self):
        NumOfLine = 0
        rows = []

        for i in range(self.Height):
            n = 0
            for j in range(self.Width):
                if self.getBlockAt(j, self.Height - i - 1) != block.NoShape:
                    n += 1

            if n == self.Width:
                rows.append(self.Height - i - 1)

        rows.reverse()

        for m in rows:
            for r in range(1, m):
                for c in range(self.Width):
                    self.setBlockAt(c, m - r + 1, self.getBlockAt(c, m - r))

        NumOfLine = NumOfLine + len(rows) ** 2 / 2

        if NumOfLine > 0:
            self.RemovedLine = self.RemovedLine + NumOfLine
            self.isReached = True
            self.currentShape.setShape(block.NoShape)
            self.update()
        self.setScore(100 * self.RemovedLine)

    def startGame(self):
        if self.isPaused:
            return
        self.isStarted = True
        self.isReached = False
        self.RemovedLine = 0
        self.setScore(100 * self.RemovedLine)
        self.clearBoard()

        self.newShape()
        self.timer.start(self.speed, self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
        else:
            self.timer.start(self.speed, self)

        self.update()

    def newShape(self):
        self.currentShape = shape()
        self.currentShape.setShape(self.getNextShape())
        self.setNextShape()
        self.shapeBoard.setStart()
        self.shapeBoard.update()
        self.x = self.Width // 2 + 1
        self.y = 0

        if not self.move(self.currentShape, self.x, self.y):
            self.currentShape.setShape(block.NoShape)
            self.timer.stop()
            self.isStarted = False
            reply = QMessageBox.information(self, 'Tetris', 'You Lose!',
                                            QMessageBox.Yes | QMessageBox.No)
            self.shapeBoard.setEnd()

    def setNextShape(self):
        self.next = random.randint(1, 7)
        temp = shape()
        temp.setShape(self.next)
        self.shapeBoard.setNextShape(temp)


    def getNextShape(self):
        return self.next

    def drawBlock(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.getBlockWidth() - 2, self.getBlockHeight() - 2, color)
        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.getBlockHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.getBlockWidth() - 1, y)
        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.getBlockHeight() - 1, x + self.getBlockWidth() - 1, y + self.getBlockHeight() - 1)
        painter.drawLine(x + self.getBlockWidth() - 1, y + self.getBlockHeight() - 1, x + self.getBlockWidth() - 1, y + 1)

    def getBlockWidth(self): # The width of each block
        return self.contentsRect().width() // self.Width

    def getBlockHeight(self): # The height of each block
        return self.contentsRect().height() // self.Height

    def getBlockAt(self, x, y):
        return self.blockList[y * self.Width + x]

    def setBlockAt(self, x, y, shape):
        self.blockList[y * self.Width + x] = shape

    def clearBoard(self):
        self.blockList.clear()
        for i in range(self.Width*self.Height):
            self.blockList.append(block.NoShape)


class nextShapeBoard(QWidget):
    def __init__(self):
        super(nextShapeBoard, self).__init__()
        self.initUI()

    def initUI(self):
        palette = QPalette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setFixedWidth(150)
        self.setFixedHeight(150)
        self.isStart = False
        self.length = 30
        self.shape = None

    def setNextShape(self, s):
        self.shape = s

    def setStart(self):
        self.isStart = True

    def setEnd(self):
        self.isStart = False

    def paintEvent(self, e):
        painter = QPainter(self)
        sx = 75
        sy = 30
        if self.isStart:
            for i in range(4):
                self.drawBlock(painter, sx + self.shape.getBlockX(i)*30, sy - self.shape.getBlockY(i)*30, self.shape.getShape())

    def drawBlock(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, 30 - 2, 30 - 2, color)
        painter.setPen(color.lighter())
        painter.drawLine(x, y + 30 - 1, x, y)
        painter.drawLine(x, y, x + 30 - 1, y)
        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + 30 - 1, x + 30 - 1, y + 30 - 1)
        painter.drawLine(x + 30 - 1, y + 30 - 1, x + 30 - 1, y + 1)


class controlBar(QWidget):
    def __init__(self, g):
        super(controlBar, self).__init__()
        self.initUI()
        self.gb = g

    def initUI(self):
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.valueChanged[int].connect(self.changeValue)
        sld.setTickPosition(QSlider.TicksBothSides)
        sld.setMaximum(10)
        sld.setTickInterval(1)
        sld.setSingleStep(1)
        sld.setPageStep(1)
        self.label = QLabel("0")

        hbox = QHBoxLayout()
        hbox.addWidget(sld)
        hbox.addWidget(self.label)
        self.setLayout(hbox)

    def changeValue(self, value):
        self.label.setText(str(value))
        self.gb.setSpeed((11 - value)*40)

class Board(QFrame):
    def __init__(self):
        super(Board, self).__init__()
        self.initUI()


    def initUI(self):
        self.gb = gameBoard()
        fb = self.gb.functionBoard

        hbox = QHBoxLayout()
        hbox.addWidget(self.gb)
        vbox = QVBoxLayout()
        vbox.addWidget(fb)
        hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.setFixedWidth(650)




