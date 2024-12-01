import math
import threading
import time
import tkinter as tk
from random import randint, random
from Predator import Predator
from Herbivore import Herbivore
from Tree import Tree

# Размеры поля и правила мира
tree_on_death = True
cell_size = 20

# width, height = 100, 80

# width, height = 50, 40


width, height = 25, 20

# width, height = 3, 3

# generation
tree_probability = 0.05
herbivore_probability = 0.01
predator_probability = 0.01

# Tree
tree_starting_energy = 5
tree_min_breeding_energy = 20
tree_breed_size = 1
# tree_consumption_energy = 20
tree_energy_per_tick = 1
tree_energy_for_breeding = 10

# Predator
predator_starting_energy = 5
predator_min_breeding_energy = 10
predator_breeding_cost = 5

# Herbivore
herbivore_starting_energy = 5
herbivore_min_breeding_energy = 10
herbivore_breeding_cost = 5



# Генерация начального состояния
def initialize_field(_field, probability=0.2):
    none_probability = 1 - tree_probability - herbivore_probability - predator_probability
    if none_probability <0:
        raise Exception("Сумма вероятностей появления больше 1")
    for y in range(len(_field)):
        for x in range(len(_field[y])):
            res = 0
            q = random()
            # Генерация
            if q > none_probability:
                if q <= 1 - herbivore_probability - predator_probability:
                    res = Tree(randint(0,20))
                elif q <= 1 - predator_probability:
                    res = Herbivore()
                else:
                    res = Predator()
            _field[y][x] = res



# Обновление поля
def update_field(_field):
    _height = len(_field)
    _width = len(_field[0])
    _new_field = [[0 for _ in range(width)] for _ in range(height)]
    # new_field = [[None for _ in range(_width)] for _ in range(_height)]


    for y in range(len(_field)):
        for x in range(len(_field[y])):
            if _field[y][x] is not None:

                if isinstance(_field[y][x], Tree):
                    _new_field[y][x] = _field[y][x]
                    if _field[y][x].energy >= tree_min_breeding_energy:

                        breed = tree_breed_size
                        # up
                        if breed != 0:
                            if y > 0:
                                if _field[y-1][x] == 0:
                                    _new_field[y-1][x] = Tree(tree_starting_energy)
                                    breed -= 1
                        # right
                        if breed != 0:
                            if x < width-1:
                                if _field[y][x+1] == 0:
                                    _new_field[y][x+1] = Tree(tree_starting_energy)
                                    breed -= 1
                        # down
                        if breed != 0:
                            if y < height - 1:
                                if _field[y+1][x] == 0:
                                    _new_field[y+1][x] = Tree(tree_starting_energy)
                                    breed -= 1
                        # left
                        if breed != 0:
                            if x > 0:
                                if _field[y][x-1] == 0:
                                    _new_field[y][x-1] = Tree(tree_starting_energy)
                                    breed -= 1
                        _new_field[y][x].energy -= tree_energy_for_breeding
                    _new_field[y][x].energy += tree_energy_per_tick



                elif isinstance(_field[y][x], Herbivore):
                    _new_field[y][x] = _field[y][x]
                elif isinstance(_field[y][x], Predator):
                    _new_field[y][x] = _field[y][x]



    return _new_field


# Рисование игрового поля
def draw_field(_canvas, _field, _cell_size=10):
    # _canvas.delete("all")
    for y in range(len(_field)):
        for x in range(len(_field[y])):
            if _field[y][x] is not None:

                if isinstance(_field[y][x], Tree):
                    _canvas.create_polygon( # Зелёные треугольники
                        x * _cell_size + _cell_size // 2,
                        y * _cell_size,
                        x * _cell_size,
                        y * _cell_size + _cell_size,
                        (x + 1) * _cell_size, y * _cell_size + _cell_size,
                        fill="green", outline=""
                    )
                elif isinstance(_field[y][x], Herbivore):
                    _canvas.create_oval(
                        x * _cell_size, y * _cell_size,
                        (x + 1) * _cell_size, (y + 1) * _cell_size,
                        fill="grey", outline=""
                    )
                elif isinstance(_field[y][x], Predator):
                    _canvas.create_oval(
                        x * _cell_size, y * _cell_size,
                        (x + 1) * _cell_size, (y + 1) * _cell_size,
                        fill="red", outline=""
                    )


field = [[None for _ in range(width)] for _ in range(height)]
# Шаг симуляции
def step():
    global field
    field = update_field(field)
    draw_field(canvas, field)

# Создаём начальное поле
def regenerate(_field, _canvas):
    initialize_field(_field)
    draw_field(_canvas, _field)

# Флаг для управления симуляцией
simulation_running = False

def toggle_simulation():
    global simulation_running
    if simulation_running:
        simulation_running = False  # Остановить симуляцию
        start_stop_button.config(text="Начать симуляцию")
    else:
        simulation_running = True  # Запустить симуляцию
        start_stop_button.config(text="Остановить симуляцию")
        threading.Thread(target=run_simulation, daemon=True).start()
        # threading.Thread(target=step, daemon=True).start()

def run_simulation():
    while simulation_running:
        global field
        field = update_field(field)
        draw_field(canvas, field)
        time.sleep(0.2)


# Инициализация интерфейса
root = tk.Tk()
root.title("Игра Жизнь")

canvas = tk.Canvas(root, width=width * cell_size/2, height=height * cell_size/2, bg="white")
canvas.pack()

button_frame = tk.Frame(root)
button_frame.pack()

step_button = tk.Button(button_frame, text="Шаг", command=step)
step_button.pack(side=tk.LEFT)


initialize_button = tk.Button(button_frame, text="Генерация", command=lambda: regenerate(field, canvas))
initialize_button.pack(side=tk.LEFT)

start_stop_button = tk.Button(button_frame, text="Начать симуляцию", command=toggle_simulation)
start_stop_button.pack(side=tk.LEFT)


# Генерация начального состояния и отрисовка
initialize_field(field)
draw_field(canvas, field)

root.mainloop()





















