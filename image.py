
class PGMImage:
   
    def __init__(self, width=0, height=0, maxval=255):
        self.width = width
        self.height = height
        self.maxval = maxval
        self.pixels = [[0 for _ in range(width)] for _ in range(height)]

    def read_from_file(self, filename):
        with open(filename, 'rb') as f:
            # Read header
            header = f.readline().decode().strip()
            if header != 'P5':
                raise ValueError('Not a PGM file')
            # Skip comments
            while True:
                line = f.readline().strip()
                if line and not line.startswith(b'#'):
                    break

            self.width, self.height = map(int, line.split())
            self.maxval = int(f.readline().strip())
            # Read data
            self.pixels = [
                [int.from_bytes(f.read(1), 'big') for _ in range(self.width)]
                for _ in range(self.height)
            ]

    def write_to_file(self, filename):
        with open(filename, 'wb') as f:
            # Write header
            f.write(f"P5\n{self.width} {self.height}\n{self.maxval}\n".encode())
            # Write data
            for row in self.pixels:
                for pixel in row:
                    # Clamp the pixel value within the 0-255 range
                    clamped_pixel = max(0, min(255, int(pixel)))
                    f.write(clamped_pixel.to_bytes(1, 'big'))

    def get_pixel(self, x, y):
        return self.pixels[y][x]

    def set_pixel(self, x, y, value):
        self.pixels[y][x] = value