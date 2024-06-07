import numpy as np
import cv2
import random

# inisialisasi ukuran grid, cell size, dan window size
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


# acak posisi jalan
def buatJalan():
    
    posisiJalan = {'horizontal': [], 'vertical': []}
    
    # ukuran jalan 1 cell
    roadWidth = 1 * cellSize
    maks = 100

    # Horizontal road
    for i in range(random.randint(4, 7)):
        startRow = random.randint(0, gridSize - 1) * cellSize
        coba = 0
        # 
        while any(abs(startRow - row) < 15 * cellSize for row, * i in posisiJalan['horizontal']):
            startRow = random.randint(0, gridSize - 1) * cellSize
            coba += 1
            if coba >= maks:
                break
        if coba < maks:
            posisiJalan['horizontal'].append((startRow, 'straight'))

    # Vertical road
    for i in range(random.randint(3, 5)):
        startCol = random.randint(0, gridSize - 1) * cellSize
        coba = 0
        # 
        while any(abs(startCol - col) < 15 * cellSize for col, * i in posisiJalan['vertical']):
            startCol = random.randint(0, gridSize - 1) * cellSize
            coba += 1
            if coba >= maks:
                break
        if coba < maks:
            posisiJalan['vertical'].append((startCol, 'straight'))

    # Jalan belokan
    for i in range(random.randint(2, 3)):
        turn = random.choice(['horizontal', 'vertical'])
        if turn == 'horizontal' and posisiJalan['horizontal']:
            index = random.randint(0, len(posisiJalan['horizontal']) - 1)
            turnRow = posisiJalan['horizontal'][index][0]
            turnPoint = random.randint(20, gridSize - 20) * cellSize
            coba = 0
            # 
            while (any(abs(turnPoint - col) < 20 * cellSize for col, * i in posisiJalan['vertical']) or
                   any(abs(turnPoint - otherTurn[2]) < 20 * cellSize for otherTurn in posisiJalan['horizontal'] if len(otherTurn) > 2)):
                turnPoint = random.randint(20, gridSize - 20) * cellSize
                coba += 1
                if coba >= maks:
                    break
            if coba < maks:
                posisiJalan['horizontal'][index] = (turnRow, 'turn', turnPoint)
        elif turn == 'vertical' and posisiJalan['vertical']:
            index = random.randint(0, len(posisiJalan['vertical']) - 1)
            turnCol = posisiJalan['vertical'][index][0]
            turnPoint = random.randint(20, gridSize - 20) * cellSize
            coba = 0
            # 
            while (any(abs(turnPoint - row) < 20 * cellSize for row, * i in posisiJalan['horizontal']) or
                   any(abs(turnPoint - otherTurn[2]) < 20 * cellSize for otherTurn in posisiJalan['vertical'] if len(otherTurn) > 2)):
                turnPoint = random.randint(20, gridSize - 20) * cellSize
                coba += 1
                if coba >= maks:
                    break
            if coba < maks:
                posisiJalan['vertical'][index] = (turnCol, 'turn', turnPoint)

    return posisiJalan, roadWidth

# gambar jalan di grid
def gambarJalan(grid, posisiJalan, cellSize, roadWidth):
    roadColor = (128, 128, 128)
    
    # for dashed line (pembatas jalan)
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
            # print(road)
            for row in range(0, gridSize * cellSize, cellSize):
                grid[row:row + cellSize, col:col + roadWidth] = roadColor

    # Buat garis putih putus-putus untuk jalan horizontal
    for road in posisiJalan['horizontal']:
        if road[1] == 'turn':
            turnRow, pos, turnPoint = road
            # print(road)
            centerY = turnRow + roadWidth // 2
            for col in range(0, turnPoint, dashLength + dashGap):
                for i in range(dashLength):
                    if col + i < turnPoint:
                        grid[centerY:centerY + 1, col + i:col + i + 1] = dashLineColor
            centerX = turnPoint + roadWidth // 2
            for row in range(turnRow, gridSize * cellSize, dashLength + dashGap):
                for i in range(dashLength):
                    if row + i < gridSize * cellSize:
                        # print(centerX)
                        grid[row + i:row + i + 1, centerX:centerX + 1] = dashLineColor
        else:
            row, pos = road
            # print(road)
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
