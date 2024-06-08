import numpy as np
import cv2
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Inisialisasi ukuran grid, cell size, dan window size
gridSize = 150
cellSize = 6
windowSize = gridSize * cellSize

def buatGrid():
    gridColor = (0, 100, 0)
    grid = np.ones((windowSize, windowSize, 3), dtype=np.uint8) * np.array(gridColor, dtype=np.uint8)
    
    # Gambar garis vertikal
    for i in range(1, gridSize):
        cv2.line(grid, (i * cellSize, 0), (i * cellSize, windowSize), (0, 0, 0), 1)

    # Gambar garis horizontal
    for j in range(1, gridSize):
        cv2.line(grid, (0, j * cellSize), (windowSize, j * cellSize), (0, 0, 0), 1)
    
    return grid

# Periksa jarak antar jalan 
def isSafe(posisiJalan, posisi, arah, minJarak=15, minBelokanJarak=10):
    if arah == 'horizontal':
        for row, pos, *turn in posisiJalan['horizontal']:
            if abs(posisi - row) < minJarak * cellSize:
                return False
        for row, pos, turnPoint in [x for x in posisiJalan['horizontal'] if len(x) == 3]:
            if abs(turnPoint - posisi) < minBelokanJarak * cellSize:
                return False
        for col, pos, *turn in posisiJalan['vertical']:
            if len(turn) == 1 and abs(turn[0] - posisi) < minBelokanJarak * cellSize:
                return False
    elif arah == 'vertical':
        for col, pos, *turn in posisiJalan['vertical']:
            if abs(posisi - col) < minJarak * cellSize:
                return False
        for col, pos, turnPoint in [x for x in posisiJalan['vertical'] if len(x) == 3]:
            if abs(turnPoint - posisi) < minBelokanJarak * cellSize:
                return False
        for row, pos, *turn in posisiJalan['horizontal']:
            if len(turn) == 1 and abs(turn[0] - posisi) < minBelokanJarak * cellSize:
                return False
    return True

# Backtracking untuk cari posisi jalan
def backtrack(posisiJalan, horizontalCount, verticalCount, roadWidth, maxTurn, currentTurn = 0, attemp = 0):
    
    # untuk menghindari error memory stack, rekursif makin dalam
    if attemp > 1000:
        return False

    if horizontalCount == 0 and verticalCount == 0:
        return True
    
    # untuk jalan tanpa belokan
    if horizontalCount > 0:
        newRow = random.randint(0, gridSize - 1) * cellSize
        if isSafe(posisiJalan, newRow, 'horizontal'):
            posisiJalan['horizontal'].append((newRow, 'straight'))
            if backtrack(posisiJalan, horizontalCount - 1, verticalCount, roadWidth, maxTurn, currentTurn, attemp + 1):
                # print(currentTurn)
                return True
            posisiJalan['horizontal'].pop()

    if verticalCount > 0:
        newCol = random.randint(0, gridSize - 1) * cellSize
        if isSafe(posisiJalan, newCol, 'vertical'):
            posisiJalan['vertical'].append((newCol, 'straight'))
            if backtrack(posisiJalan, horizontalCount, verticalCount - 1, roadWidth, maxTurn, currentTurn, attemp + 1):
                return True
            posisiJalan['vertical'].pop()
            
    # untuk jalan berbelok
    if currentTurn < maxTurn:
        turn = random.choice(['horizontal', 'vertical'])
        if turn == 'horizontal' and posisiJalan['horizontal']:
            i = random.randint(0, len(posisiJalan['horizontal']) - 1)
            turnRow = posisiJalan['horizontal'][i][0]
            turnPoint = random.randint(10, gridSize - 10) * cellSize
            # apakah jarak aman
            if isSafe(posisiJalan, turnPoint, 'vertical', minJarak = 15, minBelokanJarak = 10):
                posisiJalan['horizontal'][i] = (turnRow, 'turn', turnPoint)
                if backtrack(posisiJalan, horizontalCount, verticalCount, roadWidth, maxTurn, currentTurn + 1, attemp + 1):
                    return True
                posisiJalan['horizontal'][i] = (turnRow, 'straight')
        elif turn == 'vertical' and posisiJalan['vertical']:
            i = random.randint(0, len(posisiJalan['vertical']) - 1)
            turnCol = posisiJalan['vertical'][i][0]
            turnPoint = random.randint(10, gridSize - 10) * cellSize
            if isSafe(posisiJalan, turnPoint, 'horizontal', minJarak = 15, minBelokanJarak = 10):
                posisiJalan['vertical'][i] = (turnCol, 'turn', turnPoint)
                if backtrack(posisiJalan, horizontalCount, verticalCount, roadWidth, maxTurn, currentTurn + 1, attemp + 1):
                    return True
                posisiJalan['vertical'][i] = (turnCol, 'straight')

    return False

# Acak posisi jalan
def buatJalan():
    posisiJalan = {'horizontal': [], 'vertical': []}
    
    roadWidth = 1 * cellSize
    horizontalCount = random.randint(4, 7)
    verticalCount = random.randint(3, 5)
    maxTurn = random.randint(1, 3)
    
    while True:
        if backtrack(posisiJalan, horizontalCount, verticalCount, roadWidth, maxTurn):
            break
    
    return posisiJalan, roadWidth

# gambar jalan di grid
def gambarJalan(grid, posisiJalan, cellSize, roadWidth):
    roadColor = (128, 128, 128)
    
    # For dashed line (pembatas jalan)
    dashLineColor = (255, 255, 255)
    dashLength = 4  
    dashGap = 4     

    for road in posisiJalan['horizontal']:
        if road[1] == 'turn':
            turnRow, pos, turnPoint = road
            for col in range(0, turnPoint, cellSize):
                grid[turnRow:turnRow + roadWidth, col:col + cellSize] = roadColor
            for offset in range(roadWidth):
                grid[turnRow + offset:turnRow + roadWidth, turnPoint:turnPoint + roadWidth - offset] = roadColor
            for row in range(turnRow, gridSize * cellSize, cellSize):
                grid[row:row + cellSize, turnPoint:turnPoint + roadWidth] = roadColor
        else:
            row, pos = road
            for col in range(0, gridSize * cellSize, cellSize):
                grid[row:row + roadWidth, col:col + cellSize] = roadColor
    for road in posisiJalan['vertical']:
        if road[1] == 'turn':
            turnCol, pos, turnPoint = road
            for row in range(0, turnPoint, cellSize):
                grid[row:row + cellSize, turnCol:turnCol + roadWidth] = roadColor
            for offset in range(roadWidth):
                grid[turnPoint:turnPoint + roadWidth - offset, turnCol + offset:turnCol + roadWidth] = roadColor
            for col in range(turnCol, gridSize * cellSize, cellSize):
                grid[turnPoint:turnPoint + roadWidth, col:col + cellSize] = roadColor
        else:
            col, position = road
            for row in range(0, gridSize * cellSize, cellSize):
                grid[row:row + cellSize, col:col + roadWidth] = roadColor

    # Buat garis putih putus-putus untuk jalan horizontal
    for road in posisiJalan['horizontal']:
        if road[1] == 'turn':
            turnRow, pos, turnPoint = road
            centerY = turnRow + roadWidth // 2
            for col in range(0, turnPoint, dashLength + dashGap):
                for i in range(dashLength):
                    if col + i < turnPoint:
                        grid[centerY:centerY + 1, col + i:col + i + 1] = dashLineColor
            centerX = turnPoint + roadWidth // 2
            for row in range(turnRow, gridSize * cellSize, dashLength + dashGap):
                for i in range(dashLength):
                    if row + i < gridSize * cellSize:
                        grid[row + i:row + i + 1, centerX:centerX + 1] = dashLineColor
        else:
            row, pos = road
            centerY = row + roadWidth // 2
            for col in range(0, gridSize * cellSize, dashLength + dashGap):
                for i in range(dashLength):
                    if col + i < gridSize * cellSize:
                        grid[centerY:centerY + 1, col + i:col + i + 1] = dashLineColor

    # Buat garis putih putus-putus untuk jalan vertikal
    for road in posisiJalan['vertical']:
        if road[1] == 'turn':
            turnCol, pos, turnPoint = road
            centerX = turnCol + roadWidth // 2
            for row in range(0, turnPoint, dashLength + dashGap):
                for i in range(dashLength):
                    if row + i < turnPoint:
                        grid[row + i:row + i + 1, centerX:centerX + 1] = dashLineColor
            centerY = turnPoint + roadWidth // 2
            for col in range(turnCol, gridSize * cellSize, dashLength + dashGap):
                for i in range(dashLength):
                    if col + i < gridSize * cellSize:
                        grid[centerY:centerY + 1, col + i:col + i + 1] = dashLineColor
        else:
            col, pos = road
            centerX = col + roadWidth // 2
            for row in range(0, gridSize * cellSize, dashLength + dashGap):
                for i in range(dashLength):
                    if row + i < gridSize * cellSize:
                        grid[row + i:row + i + 1, centerX:centerX + 1] = dashLineColor

    return grid

# acak posisi jalan dan menggambar ulang grid
def randomAndRedraw():
    global grid, roadPosition, roadWidth
    
    # Gambar grid
    grid = buatGrid()
    
    # panggil fungsi untuk acak jalan
    roadPosition, roadWidth = buatJalan()
    
    # Gambar jalan di grid
    gambarJalan(grid, roadPosition, cellSize, roadWidth)
    
    # display GUI
    displayGUI()
        

# GUI dari tkinter
def displayGUI():
    global tk_image, scale
    image = cv2.cvtColor(grid, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = image.resize((int(image.width * scale), int(image.height * scale)), Image.Resampling.LANCZOS)
    tk_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=tk_image)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))
    

def scrollLeft(event):
    canvas.xview_scroll(-1, "units")

def scrollRight(event):
    canvas.xview_scroll(1, "units")

def scrollUp(event):
    canvas.yview_scroll(-1, "units")

def scrollDown(event):
    canvas.yview_scroll(1, "units")


root = tk.Tk()
root.title("IKN Map")

canvas = tk.Canvas(root, width=800, height=800, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

scrollX = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scrollY = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)

scrollX.pack(side=tk.BOTTOM, fill=tk.X)
scrollY.pack(side=tk.RIGHT, fill=tk.Y)

canvas.bind("<Left>", scrollLeft)
canvas.bind("<Right>", scrollRight)
canvas.bind("<Up>", scrollUp)
canvas.bind("<Down>", scrollDown)

root.bind("<Left>", scrollLeft)
root.bind("<Right>", scrollRight)
root.bind("<Up>", scrollUp)
root.bind("<Down>", scrollDown)

redraw_button = tk.Button(root, text="Redesign Map", command=randomAndRedraw)
redraw_button.pack()

grid = buatGrid()
roadPosition, roadWidth = buatJalan()
gambarJalan(grid, roadPosition, cellSize, roadWidth)

scale = 1.0
displayGUI()

root.mainloop()