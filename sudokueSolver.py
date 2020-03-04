from ortools.sat.python import cp_model
import sudokuGUI
import re

#Sudoku :
# 2 dimensional array, domaine : [1,9] pour chaque case.
# contraintes : somme des xij pour 0<=i<=9 et j fixé est égal à 45
#               somme des xij pour 0<=j<=9 et i fixé est égal à 45
#               xij != xik et xij!=xkj
#               somme des xij dans les box est égale à 45
#               les valeurs dans les box sont différentes

model = cp_model.CpModel()

#Initialize
choiceGenerate = 0
while choiceGenerate not in ('y','Y','n','N'):
    choiceGenerate = input("Generate sudoku ?")
    if choiceGenerate not in ('y','Y','n','N'):
        print('Enter y or n')
gui = sudokuGUI.Sudoku()

startValues = {}
regex = re.compile('[0-8],[0-8],[1-9]')
if choiceGenerate in ('y','Y'):
    print('TO DO')
else:
    stop = False
    while not stop:
        coord = input('Enter coordinates and value : (like this -> "i,j,value", or "stop" to continue)')
        if regex.fullmatch(coord)!=None:
            coord = coord.split(',') 
            #TO DO : verify that the value can be insterted in the current grid
            startValues[(int(coord[0]),int(coord[1]))] = int(coord[2])
            gui.setBox(int(coord[0]),int(coord[1]),int(coord[2]))
        else:
            if not coord=='stop':
                print('Not valid input')
        stop = coord == 'stop'

#Constrains
grid = [[model.NewIntVar(1,9,f'[{i},{j}]') for j in range(0,9)] for i in range(0,9)]
column =  [[grid[i][j] for i in range(0,9)] for j in range(0,9)]

for coord in startValues.keys():
    model.Add(grid[coord[0]][coord[1]] == startValues[coord])


for i in range(0,9):
    model.AddAllDifferent(grid[i])
    model.AddAllDifferent(column[i])

box = [[],[],[],[],[],[],[],[],[]] 
for i in range(0,9):
    for j in range(0,9):
        partI = 0 if i<=2 else 1 if i<=5 else 2
        partJ = 0 if j<=2 else 1 if j<=5 else 2
        part = partJ+partI*3
        box[part].append(grid[i][j])

print(box)
for b in box:
    model.AddAllDifferent(b)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.FEASIBLE:
    for line in range(0,9):
        for column in range(0,9):
            print(solver.Value(grid[line][column]),end ='')
            gui.setBox(line,column,solver.Value(grid[line][column]))
        print()
else:
    print('Not Feasible')
input()










