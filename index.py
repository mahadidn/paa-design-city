import numpy as np
import cv2
import random

def draw_grid():
    # Inisialisasi ukuran grid
    grid_size = 150
    cell_size = 6  # 6 pixel

    # ukuran jendela tampilan agar 900 x 900 (agar pas 6 pixel, 150 x 150)
    window_size = grid_size * cell_size

    # Inisialisasi grid dengan warna hijau gelap (0, 100, 0)
    grid_color = (0, 100, 0)
    grid = np.ones((window_size, window_size, 3), dtype=np.uint8) * np.array(grid_color, dtype=np.uint8)

    # Gambar garis vertikal
    for i in range(1, grid_size):
        cv2.line(grid, (i * cell_size, 0), (i * cell_size, window_size), (0, 0, 0), 1)

    # Gambar garis horizontal
    for j in range(1, grid_size):
        cv2.line(grid, (0, j * cell_size), (window_size, j * cell_size), (0, 0, 0), 1)

    return grid

# acak posisi jalan
def create_roads():
    road_positions = {'horizontal': [], 'vertical': []}
    
    # Lebar jalan
    road_width = 4 * cell_size

    # Membuat random jalan horizontal
    for i in range(random.randint(2, 5)):
        start_row = random.randint(0, grid_size - 1) * cell_size
        while any(abs(start_row - row) < 10 * cell_size for row, i in road_positions['horizontal']):
            start_row = random.randint(0, grid_size - 1) * cell_size
        road_positions['horizontal'].append((start_row, 'straight'))

    # Membuat random jalan vertikal
    for i in range(random.randint(2, 4)):
        start_col = random.randint(0, grid_size - 1) * cell_size
        while any(abs(start_col - col) < 15 * cell_size for col, i in road_positions['vertical']):
            start_col = random.randint(0, grid_size - 1) * cell_size
        road_positions['vertical'].append((start_col, 'straight'))

    # Tambahkan jalan berbelok
    turn_direction = random.choice(['horizontal', 'vertical'])
    if turn_direction == 'horizontal':
        # Pilih salah satu jalan horizontal untuk berbelok
        index = random.randint(0, len(road_positions['horizontal']) - 1)
        turn_row = road_positions['horizontal'][index][0]
        turn_point = random.randint(20, grid_size - 20) * cell_size  # Titik belok di tengah-tengah
        road_positions['horizontal'][index] = (turn_row, 'turn', turn_point)
        # Pastikan jarak cukup dari jalan vertikal
        while any(abs(turn_point - col) < 15 * cell_size for col, i in road_positions['vertical']):
            turn_point = random.randint(20, grid_size - 20) * cell_size
        road_positions['horizontal'][index] = (turn_row, 'turn', turn_point)
    else:
        # Pilih salah satu jalan vertikal untuk berbelok
        index = random.randint(0, len(road_positions['vertical']) - 1)
        turn_col = road_positions['vertical'][index][0]
        turn_point = random.randint(20, grid_size - 20) * cell_size  # Titik belok di tengah-tengah
        road_positions['vertical'][index] = (turn_col, 'turn', turn_point)
        # Pastikan jarak cukup dari jalan horizontal
        while any(abs(turn_point - row) < 10 * cell_size for row, i in road_positions['horizontal']):
            turn_point = random.randint(20, grid_size - 20) * cell_size
        road_positions['vertical'][index] = (turn_col, 'turn', turn_point)

    return road_positions, road_width

# gambar jalan di grid
def draw_roads(grid, road_positions, cell_size, road_width, right_way = True):
    road_color = (128, 128, 128)

    iterator = 0
    # Gambar jalan horizontal
    for road in road_positions['horizontal']:
        # print(road)
        if road[1] == 'turn':
            turn_row, i, turn_point = road
            for col in range(0, turn_point, cell_size):
                grid[turn_row:turn_row + road_width, col:col + cell_size] = road_color
            # Gambar bagian yang berbelok
            for offset in range(road_width):
                grid[turn_row + offset:turn_row + road_width, turn_point:turn_point + road_width - offset] = road_color
            for row in range(turn_row, grid_size * cell_size, cell_size):
                grid[row:row + cell_size, turn_point:turn_point + road_width] = road_color
        else:
            # print(right_way)
            row, i = road
            if road_positions['vertical'][0][1] != 'turn' and road_positions['horizontal'][0][1] != 'turn' and right_way:
                # print(road_positions['vertical'][0][1])
                width = road_positions['vertical'][0][0]
                # print(width)
            else:
                right_way = False
                # print("ini di print")
                # print(road_positions['vertical'][1][1])
                
                width = road_positions['vertical'][0][0]
            
            for col in range(0, grid_size * cell_size, cell_size):
                if iterator <= width and right_way:
                    grid[row:row + road_width, width:width + cell_size] = road_color
                else:
                    grid[row:row + road_width, col:col + cell_size] = road_color
                # print(col)
                iterator += 6

    # Gambar jalan vertikal
    iterator = 0
    # w = 1
    for road in road_positions['vertical']:
        if road[1] == 'turn':
            turn_col, i, turn_point = road
            for row in range(0, turn_point, cell_size):
                grid[row:row + cell_size, turn_col:turn_col + road_width] = road_color
            # Gambar bagian yang berbelok
            for offset in range(road_width):
                grid[turn_point:turn_point + road_width - offset, turn_col + offset:turn_col + road_width] = road_color
            for col in range(turn_col, grid_size * cell_size, cell_size):
                grid[turn_point:turn_point + road_width, col:col + cell_size] = road_color
        else:
            col, i = road
            if road_positions['horizontal'][0][1] != 'turn' and road_positions['vertical'][0][1] != 'turn':
                # print(road_positions['horizontal'][0][1])
                width = road_positions['horizontal'][0][0]
            else:
                width = road_positions['horizontal'][1][0]
            for row in range(0, grid_size * cell_size, cell_size):
                if iterator < width:
                    grid[width:width + cell_size, col:col + road_width] = road_color
                    right_way = False
                else:
                    grid[row:row + cell_size, col:col + road_width] = road_color
                # print(col)
                iterator += 6
                # w += 1

# acak posisi jalan dan menggambar ulang grid
def randomize_and_redraw():

    # panggil fungsi untuk acak jalan
    road_positions, road_width = create_roads()

    # Bersihkan grid
    grid_color = (0, 100, 0)
    grid = np.ones((window_size, window_size, 3), dtype=np.uint8) * np.array(grid_color, dtype=np.uint8)

    # Menggambar grid
    grid = draw_grid()

    # Menggambar jalan di grid
    draw_roads(grid, road_positions, cell_size, road_width)
    
    for i in range(1, grid_size):
        cv2.line(grid, (i * cell_size, 0), (i * cell_size, window_size), (0, 0, 0), 1)

    # Gambar garis horizontal
    for j in range(1, grid_size):
        cv2.line(grid, (0, j * cell_size), (window_size, j * cell_size), (0, 0, 0), 1)

    # Tampilkan grid yang telah diacak
    cv2.imshow("IKN Map", grid)

# Inisialisasi ukuran jendela tampilan
window_size = 900  

# jendela tampilan
cv2.namedWindow("IKN Map")

# Inisialisasi ukuran grid
grid_size = 150
cell_size = 6  # Ukuran setiap sel (misalnya, 6 pixel)

# Menggambar grid awal
grid = draw_grid()

# Atur posisi jalan (acak posisi dipanggil dan sekalian cek collision tiap jalan)
road_positions, road_width = create_roads()

# gambar jalan di grid
draw_roads(grid, road_positions, cell_size, road_width)

cv2.imshow("IKN Map", grid)

while True:
    
    key = cv2.waitKey(0)

    # Periksa jika tombol spasi ditekan
    if key == 32:
        # jika ditekan maka acak dan gambar ulang
        randomize_and_redraw()
    # q untuk keluar dari aplikasi
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
