from struct import pack
import numpy as np


def dots_creating():
    t = np.linspace(0, 2*np.pi, 300)
    np_x = np.sin(3*t+np.pi/2)
    np_y = np.sin(2*t)
    x = [round(i, 2) for i in np_x]
    y = [round(i, 2) for i in np_y]
    x_min, y_min = min(x), min(y)
    dots = [(x[i], y[i]) for i in range(len(x))]
    dots.reverse()
    return x_min, y_min, dots


def header_creating(width, height):
    file_type = 19778
    res_1 = 0
    res_2 = 0
    pix_data = 62
    file_size = pix_data * width * height
    return pack('<HL2HL', file_type, file_size, res_1, res_2, pix_data)


def info_creating(width, height):
    header_size = 40
    image_width = width
    image_height = height
    planes = 1
    pix_bits = 8
    compression = 0
    image_size = 0
    x_pix = 0
    y_pix = 0
    total_colors = 2
    important_colors = 0
    return pack('<3L2H6L', header_size,
                image_width, image_height,
                planes, pix_bits, compression,
                image_size, x_pix, y_pix,
                total_colors, important_colors)


def color_table_creating():
    color_1 = (0, 0, 0, 0)
    color_2 = (255, 255, 255, 0)
    return pack('<8B', *color_1, *color_2)


def file_writing(step, width, height, file_name):
    with open(f'{file_name}.bmp', 'wb') as f:
        f.write(header_creating(width, height))
        f.write(info_creating(width, height))
        f.write(color_table_creating())
        x_min, y_min, dots = dots_creating()
        pix_y = y_min
        for i in range(height):
            pix_x = x_min
            for j in range(width):
                if (pix_x, pix_y) in dots:
                    f.write(pack('<B', 0))
                else:
                    f.write(pack('<B', 1))
                pix_x = round(pix_x + step, 2)
            pix_y = round(pix_y + step, 2)


if __name__ == '__main__':
    file_writing(0.01, 300, 300, 'koala')
