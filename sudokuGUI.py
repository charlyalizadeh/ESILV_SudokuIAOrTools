import tkinter as tk
import tkinter.font as tkFont

class Sudoku:
    def __init__(self):
        #----WINDOW----
        self.window = tk.Tk()
        self.window.geometry("600x400")
        for i in range(3):
            self.window.grid_columnconfigure(i,weight = 1)
            self.window.grid_rowconfigure(i,weight = 1)
        self.window.grid_rowconfigure(3,weight = 1)

        #----MAIN FRAMES : the big squares----
        self.mainFrames = []
        iColumn = 0
        iRow = 0
        for i in range(9):
            self.mainFrames.append(tk.Frame(self.window,bd=1,bg='black'))
            self.mainFrames[i].grid(column = iColumn, row = iRow,sticky = 'WESN')
            if iColumn == 2:
                iColumn=0
                iRow+=1
            else:
                iColumn+=1

        #----SECOND FRAMES & LABELS : the little squares----
        self.numbers = []
        self.secondFrames = []
        fontStyle = tkFont.Font(family="Lucida Grande", size=20)
        for i in range(9):
            for j in range(3):
                self.mainFrames[i].grid_rowconfigure(j,weight = 1)
                self.mainFrames[i].grid_columnconfigure(j,weight = 1)
            iColumn = 0
            iRow = 0
            index = 0
            self.secondFrames.append([])
            self.numbers.append([])
            for j in range(9):
                self.secondFrames[i].append(tk.Frame(self.mainFrames[i],bd = 1,bg='black'))
                self.numbers[i].append(tk.Label(self.secondFrames[i][index],text = ' ',bg='white',fg='black',bd=4,font = fontStyle))
                self.secondFrames[i][index].grid(column=iColumn,row = iRow,sticky='WESN')
                self.numbers[i][index].pack(fill='both',expand=True)
                index+=1
                if iColumn==2:
                    iColumn=0
                    iRow+=1
                else:
                    iColumn+=1

        #----BUTTON SOLVE,VERIFY----
        self.menuFrame = tk.Frame(self.window,bg = 'lightgrey')
        self.menuFrame.grid(row = 3,sticky = 'WESN',columnspan = 3)
        self.menuFrame.grid_rowconfigure(0,weight=1)
        for i in range(2):
            self.menuFrame.grid_columnconfigure(i,weight=1)
        self.buttonVerify = tk.Button(self.menuFrame,text='VERIFY')
        self.buttonVerify.grid(row=0,column=0,sticky = 'WESN')
        self.buttonSolve = tk.Button(self.menuFrame,text='SOLVE')
        self.buttonSolve.grid(row=0,column=1,sticky='WESN')


    def setBox(self,indexI,indexJ,nb):
        part,index = self.translateCoordinates(indexI,indexJ)
        self.numbers[part][index]['text'] = str(nb) 

    def setBoxBg(self,indexI,indexJ,color):
        part,index = self.translateCoordinates(indexI,indexJ)
        self.numbers[part][index]['bg'] = color 
    
    def setBoxFg(self,indexI,indexJ,color):
        part,index = self.translateCoordinates(indexI,indexJ)
        self.numbers[part][index]['fg'] = color 

    def translateCoordinates(self,indexI,indexJ):
        partI = 0 if indexI<=2 else 1 if indexI<=5 else 2
        partJ = 0 if indexJ<=2 else 1 if indexJ<=5 else 2
        part = partJ+partI*3
        index = indexJ%3 + indexI%3*3
        return part,index

    def display(self,grid):
        for i in range(9):
            for j in range(9):
                self.setBox(i,j,grid[i][j])

    def clearBg(self):
        for i in range(9):
            for j in range(9):
                self.numbers[i][j].config(bg = 'white')

    def start(self):
        self.window.mainloop()

    def close(self):
        self.window.destroy()

