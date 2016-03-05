
class Conway:
    data = []
    changedCells = []
    lookup = [-1] * 512
    width = 20
    height = 20

    def __init__(self, width = 20, height = 20):
        self.width = width
        self.height = height
        print(len(self.data))
        for index in range(self.width * self.height):
            self.data.append(0);

    def display(self):
        out = ""
        count=0
        for index in range(len(self.data)):
            out = out + " " + str(self.data[index]) + " "
            count = count + 1
            if(count == self.width):
                count = 0
                print(out)
                out = ""

    def validIndex(self, index):
        return index >= 0 and index < len(self.data)

    def environmentVariable(self, neighbours, index):
        out = self.data[index]*16
        out = out + self.data[neighbours[0]]*256
        out = out + self.data[neighbours[1]]*32
        out = out + self.data[neighbours[2]]*4
        out = out + self.data[neighbours[3]]*128
        out = out + self.data[neighbours[4]]*2
        out = out + self.data[neighbours[5]]*64
        out = out + self.data[neighbours[6]]*8
        out = out + self.data[neighbours[7]]*1
        return out

    def getNeighbours(self, index):
        return [self.getTopLeftN(index),
                self.getTopN(index),
                self.getTopRightN(index),
                                self.getLeftN(index),
                                self.getRightN(index),
                                self.getBottomLeftN(index),
                                self.getBottomN(index),
                                self.getBottomRightN(index)]

    def getRightN(self, index):
        if(self.validIndex(index) == False): return -1;
        n = index + 1
        if(n % self.width == 0):
            n = n - self.width
        return n

    def getLeftN(self, index):
        if(self.validIndex(index) == False): return -1;
        n = index - 1
        if(n < 0 or index % self.width == 0):
            n = n + self.width
        return n

    def getTopN(self, index):
        if(self.validIndex(index) == False): return -1;
        n = index - self.width
        if(n < 0):
            n = n + len(self.data)
        return n

    def getBottomN(self, index):
        if(self.validIndex(index) == False): return -1;
        n = index + self.width
        if(n >= len(self.data)):
            n = n - len(self.data)
        return n

    def getTopLeftN(self, index):
        return self.getLeftN(self.getTopN(index))

    def getTopRightN(self, index):
        return self.getRightN(self.getTopN(index))

    def getBottomRightN(self, index):
        return self.getRightN(self.getBottomN(index))

    def getBottomLeftN(self, index):
        return self.getLeftN(self.getBottomN(index))

    def killCell(self, index):
        if(self.validIndex(index)):
            self.data[index] = 0
            self.changedCells.append(index)
            

    def reviveCell(self, index):
        if(self.validIndex(index)):
            self.data[index] = 1
            self.changedCells.append(index)
           
    def isCellAlive(self, index):
        return self.data[index] > 0

    def applyRulesToCell(self, index, newGen):
        nbrs = self.getNeighbours(index)
        env = self.environmentVariable(nbrs, index)

        if(self.lookup[env] >= 0):
            newGen[index] = self.lookup[env]
            if(newGen[index] != self.data[index]):
                self.changedCells.append(index)
            return
        else:
            numAlive = 0;

            for cellIndex in range(len(nbrs)):
                if(self.isCellAlive(nbrs[cellIndex])):
                    numAlive = numAlive + 1

                if(not self.isCellAlive(index) and numAlive == 3):
                    newGen[index] = 1

                elif(self.isCellAlive(index) and (numAlive == 3 or numAlive == 2)):
                    newGen[index] = 1
                else:
                    newGen[index] = 0

                self.lookup[env] = newGen[index]

                if(newGen[index] != self.data[index]):
                    self.changedCells.append(index)

    def newGeneration(self):
        ng = self.data[:]
        lastGen = self.changedCells[:]
        for i in range(len(self.changedCells)):
        	lastGen = lastGen + self.getNeighbours(self.changedCells[i])
        lastGen = list(set(lastGen))
        self.changedCells = []
        for index in range(len(lastGen)):
        	self.applyRulesToCell(lastGen[index], ng)
        self.data = ng
"""      
c = Conway(5,5)
c.display()
print("")
c.data[0] = 1
c.data[5] = 1
c.data[10] = 1
c.data[1] = 1
c.data[6] = 1
c.data[11] = 1
c.data[2] = 1
c.data[7] = 1
c.data[12] = 1
print(str(c.environmentVariable(c.getNeighbours(6), 6)))
c.display()
print("")
c.newGeneration()
print("changed cell indexes: " + str(c.changedCells))
c.display()

print("")
c.newGeneration()
print("changed cell indexes: " + str(c.changedCells))
c.display()
"""
