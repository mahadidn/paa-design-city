import numpy as np
import cv2
import random

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
def isSafe(posisiJalan, newPosition, posisi):
    jarak = 15 * cellSize
    if posisi == 'horizontal':
        newRow = newPosition
        for row, i in posisiJalan['horizontal']:
            if abs(newRow - row) < jarak:
                return False
    elif posisi == 'vertical':
        newCol = newPosition
        for col, i in posisiJalan['vertical']:
            if abs(newCol - col) < jarak:
                return False
    return True

# Backtracking untuk cari posisi jalan
def backtrack(posisiJalan, horizontalCount, verticalCount, roadWidth, attemp=0, maxAttemp=1000):
    
    # untuk menghindari error memory stack, rekursif makin dalam
    if attemp > maxAttemp:
        return False

    if horizontalCount == 0 and verticalCount == 0:
        return True
    
    if horizontalCount > 0:
        newRow = random.randint(0, gridSize - 1) * cellSize
        if isSafe(posisiJalan, newRow, 'horizontal'):
            posisiJalan['horizontal'].append((newRow, 'straight'))
            if backtrack(posisiJalan, horizontalCount - 1, verticalCount, roadWidth, attemp + 1):
                return True
            posisiJalan['horizontal'].pop()

    if verticalCount > 0:
        newCol = random.randint(0, gridSize - 1) * cellSize
        if isSafe(posisiJalan, newCol, 'vertical'):
            posisiJalan['vertical'].append((newCol, 'straight'))
            if backtrack(posisiJalan, horizontalCount, verticalCount - 1, roadWidth, attemp + 1):
                return True
            posisiJalan['vertical'].pop()

    return False

# Acak posisi jalan
def buatJalan():
    posisiJalan = {'horizontal': [], 'vertical': []}
    
    roadWidth = 1 * cellSize
    horizontalCount = random.randint(4, 7)
    verticalCount = random.randint(3, 5)
    
    while True:
        if backtrack(posisiJalan, horizontalCount, verticalCount, roadWidth):
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
        
    cv2.imshow("IKN Map", grid)


# Inisialisasi ukuran jendela tampilan
windowSize = 900  

# jendela tampilan
cv2.namedWindow("IKN Map")

# Inisialisasi ukuran grid
gridSize = 150
cellSize = 6  # Ukuran setiap sel (6 pixel)

# Menggambar grid awal
grid = buatGrid()

# Atur posisi jalan (acak posisi dipanggil dan sekalian cek collision tiap jalan)
roadPosition, roadWidth = buatJalan()

# gambar jalan di grid
gambarJalan(grid, roadPosition, cellSize, roadWidth)

cv2.imshow("IKN Map", grid)

while True:
    
    key = cv2.waitKey(0)

    # Periksa jika tombol spasi ditekan
    if key == 32:
        # jika ditekan maka acak dan gambar ulang
        randomAndRedraw()
    # q untuk keluar dari aplikasi
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
