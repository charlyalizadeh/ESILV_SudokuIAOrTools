from ortools.sat.python import cp_model
import random
try:
    import sudokuGUI
except ImportError:
    print("Can't display GUI, sudokuGUI module not find")

class SudokuSolver:
    def __init__(self,nbStartValues = 13): 
        #----GUI SETUP------
        self.gui = sudokuGUI.Sudoku()
        self.gui.window.bind('<KeyPress>',self.action)
        self.currentSelect = [0,0]
        self.gui.buttonSolve['command'] = self.solve



        self.model = cp_model.CpModel()
        self.nbStartValues = nbStartValues
        self.grid = []#The list which contains our NewIntVar for ortools
        self.gridSoluce = [' ' for i in range(81)]#The list which contains the values of our sudoku
        self.initialCoord = []#The list wich contains the coordinates of the inital values


   #----GUI FUNCTIONS----    

    def action(self,evt):
        if evt.keysym=='Up':
            self.currentSelect[0] = 8 if self.currentSelect[0]==0 else self.currentSelect[0]-1
        if evt.keysym=='Down':
            self.currentSelect[0] = 0 if self.currentSelect[0]==8 else self.currentSelect[0]+1
        if evt.keysym=='Left':
            self.currentSelect[1] = 8 if self.currentSelect[1]==0 else self.currentSelect[1]-1
        if evt.keysym=='Right':
            self.currentSelect[1] = 0 if self.currentSelect[1]==8 else self.currentSelect[1]+1
        if evt.char.isdigit() and self.currentSelect not in self.initialCoord:
            self.gridSoluce[self.currentSelect[0]*9+self.currentSelect[1]] = int(evt.char)
        self.updateDisplay()
        
    def updateDisplay(self):
        self.gui.clearBg()
        self.gui.setBoxBg(self.currentSelect[0],self.currentSelect[1],'lightgrey')
        self.displaygridGUI(self.gridSoluce)

    def displaygridGUI(self,grid):
        existIndex = [(i,j) for i in range(9) for j in range(9) if self.gridSoluce[i*9+j]!= ' ']
        for coord in existIndex:
            self.gui.setBox(coord[0],coord[1],grid[coord[0]*9+coord[1]])
        self.gui.window.update()

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

#----GENERATION OF THE SUDOKU----
    def isValidValue(self,coord,value):
        if self.gridSoluce[coord[0]*9+coord[1]]!=' ':#if coord is already assigned
            return False
        existingIndex = [(i,j) for i in range(9) for j in range(9) if self.gridSoluce[i*9+j]!= ' ']
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
        self.createConstraint()
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
 
    def generateGame(self):
        self.generate(6)
        self.solve(False   )
        #self.displaygridTerminal(self.gridSoluce)
        while sum(1 for i in range(81) if self.gridSoluce[i]!=' ')>self.nbStartValues:
            index = random.randint(0,80)
            self.gridSoluce[index] = ' '
            
        self.initialCoord = [[int(i/9),i-int(i/9)*9] for i in range(81) if self.gridSoluce[i]!=' ']
        for coord in self.initialCoord:
            self.gui.setBoxFg(coord[0],coord[1],'red')
        self.displaygridTerminal(self.gridSoluce)
        self.displaygridGUI(self.gridSoluce)

    def play(self):
        self.generateGame()
        self.gui.window.mainloop()


sudoSolver = SudokuSolver(20)
sudoSolver.play()









