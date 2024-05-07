import numpy as np
import cv2
import random

# Inisialisasi ukuran grid
grid_size = 150
cell_size = 5  # Ukuran setiap sel (misalnya, 5 pixel)

# Inisialisasi ukuran jendela tampilan
window_size = grid_size * cell_size

# Inisialisasi grid dengan warna putih (255)
grid = np.ones((window_size, window_size, 3), dtype=np.uint8) * 255

# Gambar garis vertikal
for i in range(1, grid_size):
    cv2.line(grid, (i * cell_size, 0), (i * cell_size, window_size), (0, 0, 0), 1)

# Gambar garis horizontal
for j in range(1, grid_size):
    cv2.line(grid, (0, j * cell_size), (window_size, j * cell_size), (0, 0, 0), 1)


# take images===
# big building
bigBuilding_img = cv2.imread('images/big-building.png')
bigBuilding_imgResized = cv2.resize(bigBuilding_img, (10 * cell_size, 5 * cell_size))  # Resize sesuai ukuran grid
# house
house_img = cv2.imread('images/house.png')
house_imgResized = cv2.resize(house_img, (1 * cell_size, 2 * cell_size))
# medium building
medium_building = cv2.imread('images/medium-building.png')
medium_buildingResized = cv2.resize(medium_building, (5 * cell_size, 3 * cell_size))
# small building
smallBuilding = cv2.imread('images/small-building.png')
smallBuilding_resized = cv2.resize(smallBuilding, (2 * cell_size, 2 * cell_size))
# road
roadColor = (128, 128, 128)
# green lawn (rumput hijau)
greenLawn = (92, 169, 4)



# atur posisi bangunan di grid
# atur untuk 1 big building di grid
start_row_bigBuilding = random.randint(0, grid_size - 5) * cell_size
start_col_bigBuilding = random.randint(0, grid_size - 10) * cell_size
house_positions = []
medium_buildingPosition = []
small_buildingPosition = []
road_position = []
greenLawn_position = []

for i in range(10):
    # atur untuk 10 house
    start_row_house = random.randint(0, grid_size - 2) * cell_size  # -2 karena rumah memiliki tinggi 2 sel
    start_col_house = random.randint(0, grid_size - 1) * cell_size
    house_positions.append((start_row_house, start_col_house))

    # atur untuk 4 medium building
    if i < 4:
        startRow_mediumBuilding = random.randint(0, grid_size - 3) * cell_size
        startCol_mediumBuilding = random.randint(0, grid_size - 5) * cell_size
        medium_buildingPosition.append((startRow_mediumBuilding, startCol_mediumBuilding))
    
    # atur untuk 10 small building
    startRow_smallBuilding = random.randint(0, grid_size - 2) * cell_size
    startCol_smallBuilding = random.randint(0, grid_size - 2) * cell_size
    small_buildingPosition.append((startRow_smallBuilding, startCol_smallBuilding))

    # atur untuk road
    startRow_road = 0 * cell_size
    startCol_road = i * cell_size
    road_position.append((startRow_road, startCol_road))

    # atur untuk green lawn (rumpu hijau)
    startRow_greenLawn = 3 * cell_size
    startCol_greenLawn = i * cell_size
    greenLawn_position.append((startRow_greenLawn, startCol_greenLawn))


# tempatkan lokasi di grid
# tempatkan lokasi 1 big building
grid[start_row_bigBuilding:start_row_bigBuilding + 5 * cell_size, start_col_bigBuilding:start_col_bigBuilding + 10 * cell_size] = bigBuilding_imgResized
i = 0
for start_row_house, start_col_house in house_positions:
    # tempatkan lokasi 10 house
    grid[start_row_house:start_row_house + 2 * cell_size, start_col_house:start_col_house + cell_size] = house_imgResized
    # tempatkan lokasi 10 small building
    grid[small_buildingPosition[i][0]:small_buildingPosition[i][0] + 2 * cell_size, small_buildingPosition[i][1]:small_buildingPosition[i][1] + 2 * cell_size] = smallBuilding_resized
    
    # tempatkan lokasi 4 medium building
    if i < 4:
        grid[medium_buildingPosition[i][0]:medium_buildingPosition[i][0] + 3 * cell_size, medium_buildingPosition[i][1]:medium_buildingPosition[i][1] + 5 * cell_size] = medium_buildingResized
    
    # tempatkan road didalam grid
    grid[road_position[i][0]:road_position[i][0] + cell_size, road_position[i][1]:road_position[i][1] + 1 * cell_size] = roadColor

    # tempatkan green lawn didalam grid
    grid[greenLawn_position[i][0]:greenLawn_position[i][0] + cell_size, greenLawn_position[i][1]:greenLawn_position[i][1] + 1 * cell_size] = greenLawn

    i = i + 1


# =========================================================================================================================================
# Tampilkan grid dengan ukuran jendela yang lebih besar
cv2.imshow("Grid Map", grid)
cv2.waitKey(0)
cv2.destroyAllWindows()
