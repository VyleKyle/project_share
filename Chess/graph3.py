from PIL import Image, ImageDraw, ImageFont
from math import cos, sin, radians, sqrt

# Function to draw a hexagon at the specified location
def draw_hexagon(draw, center, size, fill=None, outline=None):
    x, y = center
    vertices = [(x + size * cos(radians(angle)), y + size * sin(radians(angle))) for angle in range(0, 360, 60)]
    draw.polygon(vertices, fill=fill, outline=outline)

# Parameters
num_rows = 11
num_cols = 11
hex_size = 40
img_size = hex_size * (2 * num_rows + 1)

# Create image
img = Image.new('RGB', (img_size, img_size), 'white')
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()

# Draw hexagonal grid
for q in range(-num_rows, num_rows + 1):
    for r in range(-num_cols, num_cols + 1):
        # Skip positions outside the hexagonal board
        if abs(q + r) > num_rows:
            continue

        # Convert axial coordinates to pixel coordinates
        x = hex_size * sqrt(3) * (r + q/2) + img_size / 2
        y = 3/2 * hex_size * q + img_size / 2

        # Draw hexagon
        draw_hexagon(draw, (x, y), hex_size, outline='black')

        # Draw label
        label = f"{q},{r}"
        label_w, label_h = draw.textsize(label, font=font)
        label_pos = (x - label_w / 2, y - label_h / 2)
        draw.text(label_pos, label, fill='black', font=font)

# Save image
img_path = "./tmp.png"
img.save(img_path)

img_path

