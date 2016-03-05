"""
Conway's Game of Life

Joel Hill - 2016
joel.hill.87@gmail.com
"""


class Conway:
    data = [] #array to hold all cells
    changedCells = [] #array to hold all changed cells
    width = 20
    height = 20

    def __init__(self, width = 20, height = 20):
        """
        Initialize Conway class.
        """
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


    #####################################################################
    ####################  GET CELL NIEGHBOURS  ##########################
    #####################################################################
    def getNeighbours(self, index):
        return [self.getTopN(index),
                        self.getBottomN(index),
                        self.getLeftN(index),
                        self.getRightN(index),
                        self.getTopRightN(index),
                        self.getTopLeftN(index),
                        self.getBottomLeftN(index),
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
        """
        index: index of cell to kill
        post: The cell located at index is set to dead
              Revived cell is added to changed cells list
        """
        if(self.validIndex(index)):
            self.data[index] = 0
            self.changedCells.append(index)
            

    def reviveCell(self, index):
        """
        index: index of cell to revive
        post: The cell located at index is set to alive
              Revived cell is added to changed cells list
        """
        if(self.validIndex(index)):
            self.data[index] = 1
            self.changedCells.append(index)
            

    def isCellAlive(self, index):
        return self.data[index] > 0


    def applyRulesToCell(self, index, newGen):
        """
        index: the index of the cell to check
        newGen: The array of cells to update
        Post: newGen is populated with updated cells
        """
        nbrs = self.getNeighbours(index)
        numAlive = 0
        for cellIndex in range(len(nbrs)):
            if(self.isCellAlive(nbrs[cellIndex])):
                numAlive = numAlive + 1

        if(not self.isCellAlive(index) and numAlive == 3):
            newGen[index] = 1

        elif(self.isCellAlive(index) and (numAlive == 3 or numAlive == 2)):
            newGen[index] = 1
        else:
            newGen[index] = 0

        if(newGen[index] != self.data[index]):
            self.changedCells.append(index)
            

    def newGeneration(self):
        """
        Updates self.data to reflect the new state after one generation
        """
        ng = self.data[:]   #make copy of original data
        lastGen = self.changedCells[:] 
        for i in range(len(self.changedCells)):
            lastGen = lastGen + self.getNeighbours(self.changedCells[i])
        lastGen = list(set(lastGen))
        #print(str(lastGen))
        self.changedCells = []
        for index in range(len(lastGen)):
            self.applyRulesToCell(lastGen[index], ng)
        self.data = ng
        if(len(self.data)< len(lastGen)):
            print("WARNING: ALGORITHM NO LONGER MORE EFFECTIVE THAN BRUTE FORCE")
