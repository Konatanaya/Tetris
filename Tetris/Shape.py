class block:
    NoShape = 0
    Square = 1
    Line = 2
    TShape = 3
    LShape = 4
    MLShape = 5
    ZShape = 6
    MZShape = 7


class shape:
    shapeTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((-1, 0), (0, 0), (0, -1), (-1, -1)),
        ((-2, 0), (-1, 0), (0, 0), (1, 0)),
        ((-1, -1), (0, -1), (0, 0), (1, -1)),
        ((0, 0), (0, -1), (0, -2), (1, -2)),
        ((-1, -2), (0, -2), (0, -1), (0, 0)),
        ((-1, 0), (0, 0), (0, -1), (1, -1)),
        ((-1, -1), (0, -1), (0, 0), (1, 0)),
    )

    def __init__(self):
        self.location = [[0, 0] for i in range(4)]
        self.shape = block.NoShape
        self.setShape(self.shape)

    def getShape(self):
        return self.shape

    def setShape(self, s):
        table = self.shapeTable[s]
        for i in range(4):
            for j in range(2):
                self.location[i][j] = table[i][j]
        self.shape = s

    def getBlockInShape(self, index):
        return self.location[index]

    def setBlockLocation(self,index, x, y):
        self.location[index][0] = x
        self.location[index][1] = y

    def getBlockX(self, index):
        return self.location[index][0]

    def getBlockY(self, index):
        return self.location[index][1]

    def rotateL(self):
        if self.shape == block.Square:
            return self
        temp = shape()
        temp.shape = self.shape
        for i in range(4):
            temp.setBlockLocation(i, self.getBlockY(i), -self.getBlockX(i))
        return temp

    def rotateR(self):
        if self.shape == block.Square:
            return self
        temp = shape()
        temp.shape = self.shape
        for i in range(4):
            temp.setBlockLocation(i, -self.getBlockY(i), self.getBlockX(i))
        return temp