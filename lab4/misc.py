import math


def draw_star(canvas, x, y, size, color):
    cx = x + size // 2
    cy = y + size // 2
    outer_radius = size // 2
    inner_radius = size // 4

    points = []
    for i in range(10):
        angle = math.pi / 5 * i
        radius = outer_radius if i % 2 == 0 else inner_radius
        px = cx + radius * math.cos(angle)
        py = cy - radius * math.sin(angle)
        points.append((px, py))

    flat_points = [coord for point in points for coord in point]
    canvas.create_polygon(flat_points, fill=color, outline="")
