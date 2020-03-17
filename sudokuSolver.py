from ortools.sat.python import cp_model
import random
import sudokuGUI


class SudokuSolver:
    def __init__(self,nbStartValues = 33): 
        #----GUI SETUP------
        self.gui = sudokuGUI.Sudoku()
        self.gui.window.bind('<KeyPress>',self.action)
        self.select = [0,0]
        self.gui.buttonSolve['command'] = self.solve
        self.gui.buttonClear['command'] = self.clear
        self.gui.buttonGenerate['command'] = self.generateGame
        self.gridBgColors = ['white' for i in range(81)]
        for i in range(5):
            self.gui.buttonDifficulty[i]['command'] = lambda index=i:self.changeDifficulty(index)

        


        self.model = None
        self.nbStartValues = nbStartValues
        self.grid = []#The list which contains our NewIntVar for ortools
        self.gridSoluce = [' ' for i in range(81)]#The list which contains the values of our sudoku
        self.error = []
        self.initialCoord = []#The list wich contains the coordinates of the inital values


#----GUI FUNCTIONS----    
    def action(self,evt):
        if evt.keysym=='Up':
            self.select[0] = 8 if self.select[0]==0 else self.select[0]-1
        if evt.keysym=='Down':
            self.select[0] = 0 if self.select[0]==8 else self.select[0]+1
        if evt.keysym=='Left':
            self.select[1] = 8 if self.select[1]==0 else self.select[1]-1
        if evt.keysym=='Right':
            self.select[1] = 0 if self.select[1]==8 else self.select[1]+1
        if evt.char.isdigit()  and self.select not in self.initialCoord:
            if int(evt.char)==0:
                self.gridSoluce[self.select[0]*9+self.select[1]] = ' '
            else:
                self.gridSoluce[self.select[0]*9+self.select[1]] = int(evt.char)
        self.verify()
        self.updateDisplay()
        
    def updateDisplay(self):
        #----CLEAR----
        self.gui.clearBg()
        self.gridBgColors = ['white' for i in range(81)]

        #----DISPLAY ERROR & SELECTION----
        for coord in self.error:
            self.gridBgColors[coord[0]*9+coord[1]] = 'FireBrick1'#Error
        if(tuple(self.select) in self.error):
            self.gridBgColors[self.select[0]*9 + self.select[1]] = 'FireBrick3'#Error + Select
        else:
            self.gridBgColors[self.select[0]*9 + self.select[1]] = 'lightgrey'#Select

        #----DISLPAY INITIAL VALUES----
        for coord in self.initialCoord:
            self.gui[coord[0],coord[1],'fg'] = 'SpringGreen4'
        self.gui['bg'] = self.gridBgColors
        self.gui['text'] = self.gridSoluce
        self.displaygridTerminal(self.gridSoluce)
    
    def displaygridTerminal(self,grid):
        strStart = '┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓\n'
        for i in range(9):
            strStart+='┃'
            for j in range(9):
                strStart+=' ' + str(grid[i*9+j]) + ' '
                if j%3==2:
                    strStart+='┃'
                else:
                    strStart+='│'
            strStart+='\n'
            if i!=8:
                if not i%3==2:
                    strStart+='┠───┼───┼───╂───┼───┼───╂───┼───┼───┨\n'
                else:
                    strStart+='┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫\n'
        strStart += '┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛\n'
        print(strStart)

#----GENERATION, VERIFICATION, AND RESOLUTION OF THE SUDOKU----
    def isValidValue(self,coord,value,checkSameCoordinates = True):
        if checkSameCoordinates and self.gridSoluce[coord[0]*9+coord[1]]!=' ':#if coord is already assigned
            return False
        existingIndex = [(i,j) for i in range(9) for j in range(9) if self.gridSoluce[i*9+j]!= ' ' and (i,j)!=coord]
        for c in existingIndex:
            if value == self.gridSoluce[c[0]*9+c[1]] and (c[0]==coord[0] or c[1]==coord[1]):#if there is already a value equal to 'value' in the same row or column
                return False
            if value == self.gridSoluce[c[0]*9+c[1]] and (int(c[0]/3)*3+int(c[1]/3))==(int(coord[0]/3)*3+int(coord[1]/3)):#if there is already a value equal to 'value' in the same square
                return False
        return True

    def generate(self,nbGenerate):
        nb = nbGenerate
        possibleCoord = [(i,j) for i in range(9) for j in range(9)]
        coord = []
        while nb!=0:
            coord.append(random.choices(possibleCoord)[0])
            possibleCoord.remove(coord[nbGenerate - nb])
            nb-=1
        for c in coord :
            value = random.randint(1,9)
            while(not self.isValidValue(c,value)):
                value = random.randint(1,9)
            self.gridSoluce[c[0]*9+c[1]] = value

    def createConstraint(self):
        self.model = cp_model.CpModel()
        #Variables
        self.grid = [[self.model.NewIntVar(1,9,f'[{i},{j}]') for j in range(0,9)] for i in range(0,9)]
        column =  [[self.grid[i][j] for i in range(0,9)] for j in range(0,9)]

        #Constraints : Starting values
        existIndex = [(i,j) for i in range(9) for j in range(9) if self.gridSoluce[i*9+j]!= ' ']
        for coord in existIndex:
            self.model.Add(self.grid[coord[0]][coord[1]] == self.gridSoluce[coord[0]*9+coord[1]])

        #Constraints : Different numbers in row and column
        for i in range(0,9):
            self.model.AddAllDifferent(self.grid[i])
            self.model.AddAllDifferent(column[i])

        #Constraints : Each of the nine 'box" contains different numbers
        box = [[],[],[],[],[],[],[],[],[]] 
        for i in range(0,9):
            for j in range(0,9):
                partI = 0 if i<=2 else 1 if i<=5 else 2
                partJ = 0 if j<=2 else 1 if j<=5 else 2
                part = partJ+partI*3
                box[part].append(self.grid[i][j])

        for b in box:
            self.model.AddAllDifferent(b)

    def solve(self,display = True):
        print(self.grid)
        self.createConstraint()
        print(self.grid)
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        if status == cp_model.FEASIBLE:
            for line in range(9):
                for column in range(9):
                    self.gridSoluce[line*9+column] = solver.Value(self.grid[line][column])
                print()
            if display:
                self.updateDisplay()
        else:
            print('Not solvable')
 
    def verify(self):
        self.error = []
        for i in range(9):
            for j in range(9):
                if self.gridSoluce[i*9+j]==' ':
                    continue
                isValid = self.isValidValue((i,j),self.gridSoluce[i*9+j],False)
                if not isValid:
                    self.error.append((i,j))
    
    def clearAll(self):
        self.error = []
        self.initialCoord = []
        self.gridSoluce = [' ' for i in range(81)]
        self.grid = []
        self.gridBgColors = [' ' for i in range(81)]
        self.gui.clearFg()

    def clear(self):
        for i in range(9):
            for j in range(9):
                if [i,j] not in self.initialCoord:
                    self.gridSoluce[i*9+j] = ' '
        self.verify()
        self.updateDisplay()

    def changeDifficulty(self,index):
        if index==0:
            self.nbStartValues = 50
        elif index==1:
            self.nbStartValues = 40
        elif index==2:
            self.nbStartValues = 33
        elif index==3:
            self.nbStartValues = 26
        elif index==4:
            self.nbStartValues = 17
        for i in range(5):
            if index==i:
                self.gui.buttonDifficulty[i]['bg'] = 'dark green'
            else:
                self.gui.buttonDifficulty[i]['bg'] = 'dark sea green'

    def generateGame(self):
        self.clearAll()
        self.generate(6)
        self.solve(False)
        self.displaygridTerminal(self.gridSoluce)
        while sum(1 for i in range(81) if self.gridSoluce[i]!=' ')>self.nbStartValues: 
            index = random.randint(0,80)
            self.gridSoluce[index] = ' '       
        self.initialCoord = [[int(i/9),i-int(i/9)*9] for i in range(81) if self.gridSoluce[i]!=' ']
        self.updateDisplay()   

    def play(self):
        self.generateGame()
        self.gui.start()


sudoSolver = SudokuSolver()
sudoSolver.play()









