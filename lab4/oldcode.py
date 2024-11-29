# Инициализация Pygame
import pygame
import sys

pygame.init()

# Задаем размеры окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра в жизнь")

bg_color = (96, 153, 62)    # Цвет фона
grid_color = (0, 0, 0)  # Цвет сетки

# Задаем размеры клеток
cell_size = 50

# Заполняем фон
screen.fill(bg_color)


# Рисуем сетку
for x in range(0, width, cell_size):
    pygame.draw.line(screen, grid_color, (x, 0), (x, height))
for y in range(0, height, cell_size):
    pygame.draw.line(screen, grid_color, (0, y), (width, y))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()


кружочки - травоядные
треугольники - деревья
звёздочки - хищники


import pygame
import sys

# Конфигурация
CONFIG = {
    "width": 800,
    "height": 600,
    "_cell_size": 50,
    "bg_color": (96, 153, 62),
    "grid_color": (0, 0, 0),
    "herbivore_color": (0, 255, 0),  # Травоядное - зелёный
    "tree_color": (139, 69, 19),  # Дерево - коричневый
    "predator_color": (255, 0, 0),  # Хищник - красный
}


# Функция для отрисовки сетки
def draw_grid(screen, width, height, cell_size, grid_color):
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, grid_color, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, grid_color, (0, y), (width, y))


# Функция для отрисовки элементов по координатам
def draw_element(screen, x, y, cell_size, element_type):
    """
    Отрисовывает элемент на экране.
    screen: Экран Pygame.
    x: Координата X клетки.
    y: Координата Y клетки.
    _cell_size: Размер клетки.
    element_type: Тип элемента ("herbivore", "tree", "predator").
    """
    center_x = x * cell_size + cell_size // 2
    center_y = y * cell_size + cell_size // 2
    radius = cell_size // 3

    if element_type == "herbivore":  # Травоядное (кружок)
        pygame.draw.circle(screen, CONFIG["herbivore_color"], (center_x, center_y), radius)

    elif element_type == "tree":  # Дерево (треугольник)
        points = [
            (center_x, center_y - radius),  # Вершина треугольника
            (center_x - radius, center_y + radius),  # Левый нижний угол
            (center_x + radius, center_y + radius),  # Правый нижний угол
        ]
        pygame.draw.polygon(screen, CONFIG["tree_color"], points)

    elif element_type == "predator":  # Хищник (звёздочка)
        star_points = [
            (center_x, center_y - radius),  # Верхняя точка
            (center_x + radius // 2, center_y - radius // 2),
            (center_x + radius, center_y),
            (center_x + radius // 2, center_y + radius // 2),
            (center_x, center_y + radius),
            (center_x - radius // 2, center_y + radius // 2),
            (center_x - radius, center_y),
            (center_x - radius // 2, center_y - radius // 2),
        ]
        pygame.draw.polygon(screen, CONFIG["predator_color"], star_points)


# Основной цикл программы
def main():
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["width"], CONFIG["height"]))
    pygame.display.set_caption("Игра в жизнь")

    clock = pygame.time.Clock()

    # Пример хранилища состояния клеток
    grid_state = {
        (3, 4): "herbivore",  # Травоядное в клетке (3, 4)
        (5, 2): "tree",  # Дерево в клетке (5, 2)
        (7, 8): "predator",  # Хищник в клетке (7, 8)
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Рисуем фон
        screen.fill(CONFIG["bg_color"])

        # Рисуем сетку
        draw_grid(screen, CONFIG["width"], CONFIG["height"], CONFIG["_cell_size"], CONFIG["grid_color"])

        # Рисуем элементы на основе состояния клеток
        for (x, y), element_type in grid_state.items():
            draw_element(screen, x, y, CONFIG["_cell_size"], element_type)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

