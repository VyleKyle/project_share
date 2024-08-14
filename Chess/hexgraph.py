from PIL import Image, ImageDraw

# Size of image and hexagon
width, height = 400, 400
hex_size = 40

# Create a new image with white background
img = Image.new('RGB', (width, height), 'white')
d = ImageDraw.Draw(img)

# Draw hexagonal grid
for row in range(height // hex_size):
    for col in range(width // hex_size):
        x = col * hex_size
        y = row * hex_size
        hex = [(x, y), (x + hex_size, y), (x + hex_size * 1.5, y + hex_size * 0.5),
               (x + hex_size, y + hex_size), (x, y + hex_size), (x - hex_size * 0.5, y + hex_size * 0.5)]
        d.line(hex + [hex[0]], fill='black', width=1)

# Save image
img.save('hex_grid.png')
