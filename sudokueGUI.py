import tkinter as tk

class Sudoku:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("350x200")
        for i in range(3):
            self.window.grid_columnconfigure(i,weight = 1)
            self.window.grid_rowconfigure(i,weight = 1)

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
        self.numbers = []
        self.secondFrames = []

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
                self.numbers[i].append(tk.Label(self.secondFrames[i][index],text = ' ',bg='white',fg='black',bd=4))
                self.secondFrames[i][index].grid(column=iColumn,row = iRow,sticky='WESN')
                self.numbers[i][index].pack(fill='both',expand=True)
                index+=1
                if iColumn==2:
                    iColumn=0
                    iRow+=1
                else:
                    iColumn+=1
    

    def setBox(self,indexI,indexJ,nb):
        part,index = self.translateCoordinates(indexI,indexJ)
        self.numbers[part][index]['text'] = str(nb) 
        
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

    def start(self):
        self.window.mainloop()

    def close(self):
        self.window.destroy()

