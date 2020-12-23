from struct import pack
from math import sin, pi


class ImageGenerator:
    def __init__(self, file_name, width, height, x, y, start_t, stop_t, step_t):
        self.file = file_name
        self.width = width
        self.height = height
        self.func_x = x
        self.func_y = y
        self.min_x = float('inf')
        self.min_y = float('inf')
        self.start_t = start_t
        self.stop_t = stop_t
        self.step_t = step_t
        self.round_t = len(str(step_t)) - 2

    def __header_creating(self):
        file_type = 19778
        res_1 = 0
        res_2 = 0
        pix_data = 62
        file_size = pix_data + self.width + self.height
        return pack('<HL2HL', file_type, file_size, res_1, res_2, pix_data)

    def __info_creating(self):
        header_size = 40
        planes = 1
        pix_bits = 8
        compression = 0
        image_size = 0
        x_pix_m = 0
        y_pix_m = 0
        total_colors = 2
        important_colors = 0
        return pack('<3L2H6L', header_size, self.width, self.height,
                    planes, pix_bits, compression, image_size, x_pix_m, y_pix_m,
                    total_colors, important_colors)

    def __color_table_creating(self):
        color_1 = (0, 0, 0, 0)
        color_2 = (255, 255, 255, 0)
        return pack('<8B', *color_1, *color_2)

    def __dots_creating(self):
        dots = []
        t = self.start_t
        while t <= self.stop_t:
            x = round(self.func_x(t), self.round_t)
            if x <= self.min_x:
                self.min_x = x
            y = round(self.func_y(t), self.round_t)
            if y <= self.min_y:
                self.min_y = y
            dots.append((x, y))
            t += self.step_t
        dots.reverse()
        return dots

    def file_writing(self):
        with open(f'{self.file}.bmp', 'wb') as f:
            f.write(self.__header_creating())
            f.write(self.__info_creating())
            f.write(self.__color_table_creating())
            dots = self.__dots_creating()
            pix_y = self.min_y
            for cyc_y in range(self.height):
                pix_x = self.min_x
                for cyc_x in range(self.width):
                    if (pix_x, pix_y) in dots:
                        f.write(pack('<B', 0))
                    else:
                        f.write(pack('<B', 1))
                    pix_x = round(pix_x + self.step_t, self.round_t)
                pix_y = round(pix_y + self.step_t, self.round_t)


if __name__ == '__main__':
    image = ImageGenerator(
        file_name='koala',
        width=300,
        height=300,
        start_t=0,
        stop_t=2 * pi,
        step_t=0.01,
        x=lambda t: sin(3*t + pi/2),
        y=lambda t: sin(2*t)
    )
    image.file_writing()
