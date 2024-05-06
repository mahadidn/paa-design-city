import numpy as np
import cv2

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

# BIG BUILDING====================================================================================================================
bigBuilding_img = cv2.imread('images/big-building.png')
bigBuilding_imgResized = cv2.resize(bigBuilding_img, (10 * cell_size, 5 * cell_size))  # Resize sesuai ukuran grid

# posisi big building di grid
start_row_bigBuilding = 20 * cell_size
start_col_bigBuilding = 20 * cell_size

# tempatkan gambar bangunan besar di grid
grid[start_row_bigBuilding:start_row_bigBuilding + 5 * cell_size, start_col_bigBuilding:start_col_bigBuilding + 10 * cell_size] = bigBuilding_imgResized
# =================================================================================================================================

# HOUSE ============================================================================================================================
house_img = cv2.imread('images/house.png')
house_imgResized = cv2.resize(house_img, (1 * cell_size, 2 * cell_size))

# posisi house di grid
start_row_house = 1 * cell_size
start_col_house = 1 * cell_size

# tempatkan gambar rumah di grid
grid[start_row_house:start_row_house + 2 * cell_size, start_col_house:start_col_house + cell_size] = house_imgResized
# ==================================================================================================================================



# Tampilkan map
cv2.imshow("Grid Map", grid)
cv2.waitKey(0)
cv2.destroyAllWindows()
