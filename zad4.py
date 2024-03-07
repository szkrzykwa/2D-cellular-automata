import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def automation_2d(board):
    size = board.shape[0]
    photos = []
    inp = int(input("Boundary condition type (1 - periodic, 2 - absorptive, 3 - reflective)): "))
    for simulations in range(10):
        photos.append(board)
        new_board = board.copy()
        for row in range(size):
            for col in range(size):
                neighbors = 0
                match inp:
                    case 1: # perdiodic
                        for i in range(row - 1, row + 2):
                            for j in range(col - 1, col + 2):
                                if i == row and j == col:
                                    continue
                                neighbors += board[i%size, j%size]
                    case 2: # absorptive
                        for i in range(max(0, row - 1), min(size , row + 2)):
                            for j in range(max(0, col - 1), min(size , col + 2)):
                                if i != row or j != col:
                                    neighbors += board[i, j]
                    case 3: # reflective
                        for i in range(row - 1, row + 2):
                            for j in range(col - 1, col + 2):
                                if i == row and j == col:
                                    continue
                                if i < 0:
                                    i = 1
                                if i > size-1:
                                    i = size-2
                                if j < 0:
                                    j = 1
                                if j > size-1:
                                    j = size-2      
                if board[row, col] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_board[row, col] = 0
                else:
                    if neighbors == 3:
                        new_board[row, col] = 1
        board = new_board
    return photos

def update_image(index):
    ax.clear()
    ax.imshow(photos[index], cmap="gray")
    canvas.draw()

def next_image():
    global index
    if index < len(photos) - 1:
        index += 1
        update_image(index)

def previous_image():
    global index
    if index > 0:
        index -= 1
        update_image(index)

if __name__ == "__main__":
    s = 10
    inp = int(input("Starting condition type (1 - glider, 2 - oscilator, 3 - random, 4 - unchanged)): "))
    match inp:
        case 1:        
            board = np.zeros((s,s), dtype=int)
            board[1, 2] = 1
            board[2, 3] = 1
            board[3, 1] = 1
            board[3, 2] = 1
            board[3, 3] = 1 
        case 2:
            board = np.zeros((s,s), dtype=int)
            board[3, 5] = 1
            board[4, 5] = 1
            board[5, 5] = 1
        case 3:
            board = np.random.choice([0,1], size=(s,s))
        case 4:
            board = np.zeros((s,s), dtype=int)
            board[2, 3] = 1
            board[2, 4] = 1
            board[4, 3] = 1
            board[4, 4] = 1
            board[3, 2] = 1
            board[3, 5] = 1          
    try:
        photos = automation_2d(board)
        index = 0
        root = tk.Tk()
        frame = tk.Frame(root)
        frame.pack()
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.imshow(photos[index], cmap="gray")
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        previous_button = tk.Button(root, text="Previous", command=previous_image)
        previous_button.pack(side="left")
        next_button = tk.Button(root, text="Next", command=next_image)
        next_button.pack(side="right")
        root.mainloop()
    except:
        print("wrong condiiton")