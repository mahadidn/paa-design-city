import numpy as np
import cv2
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def buatGrid():
    gridColor = (0, 100, 0)
    grid = np.ones((windowSize, windowSize, 3), dtype=np.uint8) * np.array(gridColor, dtype=np.uint8)
    
    # Gambar garis vertikal
    # for i in range(1, gridSize):
    #     cv2.line(grid, (i * cellSize, 0), (i * cellSize, windowSize), (0, 0, 0), 1)

    # # Gambar garis horizontal
    # for j in range(1, gridSize):
    #     cv2.line(grid, (0, j * cellSize), (windowSize, j * cellSize), (0, 0, 0), 1)
    
    return grid

# untuk menempatkan jalan
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
    
    roadWidth = 3 * cellSize
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
    lineColor = (0, 0, 0)
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
                        grid[centerY - (cellSize - 1):centerY - (cellSize - 2), col + i:col + i + 2] = dashLineColor
                        grid[centerY:centerY + 1, col + i:col + i + 8] = lineColor
                        grid[centerY + (cellSize - 2):centerY + (cellSize - 1), col + i:col + i + 2] = dashLineColor
            centerX = turnPoint + roadWidth // 2
            for row in range(turnRow, gridSize * cellSize, dashLength + dashGap):
                for i in range(dashLength):
                    if row + i < gridSize * cellSize:
                        grid[row + i:row + i + 1, centerX - (cellSize - 1):centerX - (cellSize - 2)] = dashLineColor
                        grid[row + i:row + i + 8, centerX:centerX + 1] = lineColor
                        grid[row + i:row + i + 1, centerX + (cellSize - 2):centerX + (cellSize - 1)] = dashLineColor
        else:
            row, pos = road
            centerY = row + roadWidth // 2
            for col in range(0, gridSize * cellSize, dashLength + dashGap):
                for i in range(dashLength):
                    if col + i < gridSize * cellSize:
                        grid[centerY - (cellSize - 1):centerY - (cellSize - 2), col + i:col + i + 2] = dashLineColor
                        grid[centerY:centerY + 1, col + i:col + i + 8] = lineColor
                        grid[centerY + (cellSize - 2):centerY + (cellSize - 1), col + i:col + i + 2] = dashLineColor

    # Buat garis putih putus-putus untuk jalan vertikal
    for road in posisiJalan['vertical']:
        if road[1] == 'turn':
            turnCol, pos, turnPoint = road
            centerX = turnCol + roadWidth // 2
            for row in range(0, turnPoint, dashLength + dashGap):
                for i in range(dashLength):
                    if row + i < turnPoint:
                        grid[row + i:row + i + 1, centerX - (cellSize - 1):centerX - (cellSize - 2)] = dashLineColor
                        grid[row + i:row + i + 8, centerX:centerX + 1] = lineColor
                        grid[row + i:row + i + 1, centerX + (cellSize - 2):centerX + (cellSize - 1)] = dashLineColor
            centerY = turnPoint + roadWidth // 2
            for col in range(turnCol, gridSize * cellSize, dashLength + dashGap):
                for i in range(dashLength):
                    if col + i < gridSize * cellSize:
                        grid[centerY - (cellSize - 1):centerY - (cellSize - 2), col + i:col + i + 2] = dashLineColor
                        grid[centerY:centerY + 1, col + i:col + i + 8] = lineColor
                        grid[centerY + (cellSize - 2):centerY + (cellSize - 1), col + i:col + i + 2] = dashLineColor
        else:
            col, pos = road
            centerX = col + roadWidth // 2
            for row in range(0, gridSize * cellSize, dashLength + dashGap):
                for i in range(dashLength):
                    if row + i < gridSize * cellSize:
                        grid[row + i:row + i + 1, centerX - (cellSize - 1):centerX - (cellSize - 2)] = dashLineColor
                        grid[row + i:row + i + 8, centerX:centerX + 1] = lineColor
                        grid[row + i:row + i + 1, centerX + (cellSize - 2):centerX + (cellSize - 1)] = dashLineColor

    return grid


# untuk menempatkan bangunan
def isValidPlace(x, y, width, height, placedPosition, roadCell):
    for i in range(y, y + height, cellSize):
        for j in range(x, x + width, cellSize):
            if (i, j) in placedPosition or (i, j) in roadCell:
                return False
            else:
                placedPosition.add((i, j))
                
    return True

# prune search 
def placeBuildingNearRoad(building, placedPosition, roadCell):
    count = building['count']
    width, height = building['size']
    img = building['img']
    attempt = 0
    maxAttemp = 1000

    for i in range(count):
        placed = False
        while not placed and attempt < maxAttemp:
            roadType = random.choice(['horizontal', 'vertical'])
            if roadType == 'horizontal' and roadPosition['horizontal']:
                road = random.choice(roadPosition['horizontal'])
                roadRow = road[0]
                if road[1] == 'turn':
                    y = roadRow + roadWidth
                    x = road[2] + roadWidth
                else:
                    y = roadRow + roadWidth
                    x = random.randint(0, gridSize - width) * cellSize
                
                # Prune search, jika posisi tidak valid ga usah dijalanin bawahnya
                if x + width * cellSize > windowSize or y + height * cellSize > windowSize:
                    # print("tidak diperlukan horizontal ", x, " ", y)
                    attempt += 1
                    continue
                
                
                if isValidPlace(x, y, width * cellSize, height * cellSize, placedPosition, roadCell):
                    grid[y:y + height * cellSize, x:x + width * cellSize] = img
                    placed = True
            elif roadType == 'vertical' and roadPosition['vertical']:
                road = random.choice(roadPosition['vertical'])
                roadCol = road[0]
                if road[1] == 'turn':
                    x = roadCol + roadWidth
                    y = road[2] + roadWidth
                else:
                    x = roadCol + roadWidth
                    y = random.randint(0, gridSize - height) * cellSize
                    
                # Prune search, jika posisi tidak valid, continue
                if x + width * cellSize > windowSize or y + height * cellSize > windowSize:
                    # print("tidak diperlukan vertical ", x, " ", y)
                    attempt += 1
                    continue
                
                if isValidPlace(x, y, width * cellSize, height * cellSize, placedPosition, roadCell):
                    grid[y:y + height * cellSize, x:x + width * cellSize] = img
                    placed = True
            attempt += 1

def buildingRandomPlace(building, placedPosition, roadCell):
    width, height = building['size']
    img = building['img']
    count = building['count']
    maxAttemp = 1000

    
    # print(building['count'])
    for i in range(count):
        attempt = 0
        placed = False
        # print("asd")
        while not placed and attempt < maxAttemp:
            x = random.randint(0, gridSize - width) * cellSize
            y = random.randint(0, gridSize - height) * cellSize
            if x + width * cellSize <=windowSize and y + height * cellSize <=windowSize:
                if isValidPlace(x, y, width * cellSize, height * cellSize, placedPosition, roadCell):
                    grid[y:y + height * cellSize, x:x + width * cellSize] = img
                    placed = True
            attempt += 1

def placeBuilding(grid, roadPosition, roadWidth):
    buildings = {
        'big_building': {'count': 1, 'size': (10, 5), 'img': big_building_img},
        'medium_building': {'count': 4, 'size': (5, 3), 'img': medium_building_img},
        'small_building': {'count': 16, 'size': (2, 2), 'img': small_building_img},
        'house': {'count': 27, 'size': (1, 2), 'img': house_img},
        'field': {'count': 2, 'size': (5, 10), 'img': lapangan_img},
        'pool': {'count': 1, 'size': (10, 5), 'img': pool_img},
        'pohon': {'count': 100, 'size': (1, 1), 'img': pohon_img},
    }

    placedPosition = set()
    roadCell = set()

    for road in roadPosition['horizontal']:
        row = road[0]
        if road[1] == 'straight':
            for col in range(0, gridSize * cellSize, cellSize):
                for offset in range(roadWidth):
                    roadCell.add((row + offset, col))
        elif road[1] == 'turn':
            turnPoint = road[2]
            for col in range(0, turnPoint, cellSize):
                for offset in range(roadWidth):
                    roadCell.add((row + offset, col))
            for offset in range(roadWidth):
                for step in range(roadWidth - offset):
                    roadCell.add((row + offset + step, turnPoint + offset))
            for rowOffset in range(roadWidth):
                for row in range(row + rowOffset, gridSize * cellSize, cellSize):
                    for offset in range(roadWidth):
                        roadCell.add((row, turnPoint + offset))

    for road in roadPosition['vertical']:
        col = road[0]
        if road[1] == 'straight':
            for row in range(0, gridSize * cellSize, cellSize):
                for offset in range(roadWidth):
                    roadCell.add((row, col + offset))
        elif road[1] == 'turn':
            turnPoint = road[2]
            for row in range(0, turnPoint, cellSize):
                for offset in range(roadWidth):
                    roadCell.add((row, col + offset))
            for offset in range(roadWidth):
                for step in range(roadWidth - offset):
                    roadCell.add((turnPoint + offset, col + offset + step))
            for colOffset in range(roadWidth):
                for col in range(col + colOffset, gridSize * cellSize, cellSize):
                    for offset in range(roadWidth):
                        roadCell.add((turnPoint + offset, col))

    for buildingName, building in buildings.items():
        if buildingName in ['field', 'pool', 'pohon']:
            buildingRandomPlace(building, placedPosition, roadCell)
        else:
            placeBuildingNearRoad(building, placedPosition, roadCell)

# acak posisi jalan dan menggambar ulang grid
def randomAndRedraw():
    global grid, roadPosition, roadWidth
    
    # Gambar grid
    grid = buatGrid()
    
    # panggil fungsi untuk acak jalan
    roadPosition, roadWidth = buatJalan()
    
    # Gambar jalan di grid
    gambarJalan(grid, roadPosition, cellSize, roadWidth)
    
    # tempatkan bangunan
    placeBuilding(grid, roadPosition, roadWidth)
    
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

# Inisialisasi ukuran grid, cell size, dan window size
gridSize = 150
cellSize = 5
windowSize = gridSize * cellSize

# Load building images
big_building_img = cv2.imread('images/big-building.png')
medium_building_img = cv2.imread('images/medium-building.png')
small_building_img = cv2.imread('images/small-building.png')
house_img = cv2.imread('images/house.png')
lapangan_img = cv2.imread('images/lapangan.png')  # Load lapangan image
pool_img = cv2.imread('images/kolam.png')
pohon_img = cv2.imread('images/pohon.png')

def resizeImage(img, width, height):
    return cv2.resize(img, (width * cellSize, height * cellSize))

# Resize building images according to their sizes
big_building_img = resizeImage(big_building_img, 10, 5)
medium_building_img = resizeImage(medium_building_img, 5, 3)
small_building_img = resizeImage(small_building_img, 2, 2)
house_img = resizeImage(house_img, 1, 2)
lapangan_img = resizeImage(lapangan_img, 5, 10)  # Resize lapangan image
pool_img = resizeImage(pool_img, 10, 5)
pohon_img = resizeImage(pohon_img, 1, 1)

root = tk.Tk()
root.title("IKN Map")

canvas = tk.Canvas(root, width=800, height=800, bg="white")
canvas.grid(row=0, column=0, padx=0, pady=0)

scrollX = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scrollY = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)
scrollX.grid(row=1, column=0, sticky="ew")
scrollY.grid(row=0, column=1, sticky="ns")


canvas.bind("<Left>", scrollLeft)
canvas.bind("<Right>", scrollRight)
canvas.bind("<Up>", scrollUp)
canvas.bind("<Down>", scrollDown)

root.bind("<Left>", scrollLeft)
root.bind("<Right>", scrollRight)
root.bind("<Up>", scrollUp)
root.bind("<Down>", scrollDown)

redrawButton = tk.Button(root, text="Generate Map", command=randomAndRedraw)
redrawButton.grid(row=15, column=0, padx=10, pady=10)

grid = buatGrid()
roadPosition, roadWidth = buatJalan()
gambarJalan(grid, roadPosition, cellSize, roadWidth)

# tempatkan bangunan
placeBuilding(grid, roadPosition, roadWidth)

scale = 1.0
displayGUI()

root.mainloop()