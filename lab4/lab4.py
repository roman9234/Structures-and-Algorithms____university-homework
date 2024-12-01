import math
import threading
import time
import tkinter as tk
from random import randint, random, shuffle
from Predator import Predator
from Herbivore import Herbivore
from Tree import Tree

# Правила мира
tree_on_death = True

# типы
TREE_TYPE = 1
HERBIVORE_TYPE = 2
PREDATOR_TYPE = 3

TREE_SURROUNDED_STATUS = 2


TREE_SURROUNDED_STATUS_FALSE = 0
TREE_SURROUNDED_STATUS_TRUE = 1

# поля животных
AMOUNT_OF_STATUSES = 6

TYPE = 0
ENERGY = 1
STATUS_ACTION = 2
STATUS_DIRECTION = 3
CHOSEN_DIRECTION = 4
CHOSEN_DIRECTION_MOVES_LEFT = 5

# STATUS_ACTION
STATUS_ACTION_READY = 0
STATUS_ACTION_COMPLETED_ACTION = 1

# STATUS_DIRECTION
STATUS_DIRECTION_NO_DIRECTION = 0
STATUS_DIRECTION_CHOSEN_DIRECTION = 1

# CHOSEN_DIRECTION
CHOSEN_DIRECTION_UP = 1
CHOSEN_DIRECTION_RIGHT = 2
CHOSEN_DIRECTION_DOWN = 3
CHOSEN_DIRECTION_LEFT = 4


# Размеры поля
cell_size = 20
# width, height = 100, 80
# width, height = 50, 40
width, height = 25, 20
# width, height = 15, 15
# width, height = 10, 10
# width, height = 4, 4
# width, height = 3, 3

# generation
tree_probability = 0.2
herbivore_probability = 0.02
predator_probability = 0.005

# Tree
tree_starting_energy = 5
tree_min_breeding_energy = 20
tree_breed_size = 2
tree_energy_per_tick = 2
tree_energy_for_breeding = 10

# Herbivore
herbivore_starting_energy = 10
# herbivore_starting_energy = 100
herbivore_min_breeding_energy = 20
# herbivore_min_breeding_energy = 400

herbivore_breeding_cost = 10

herbivore_energy_for_eating_a_tree = 5

herbivore_energy_per_tick = -1

herbivore_min_movement_distance = 4
herbivore_max_movement_distance = 15

# Predator
predator_starting_energy = 100
predator_min_breeding_energy = 200

predator_breeding_cost = 100
predator_breed_size = 1

predator_energy_for_eating_a_herbivore = 7

predator_energy_per_tick = -1

predator_min_movement_distance = 10
predator_max_movement_distance = 20


# системные переменные (нужны для симуляции)
new_amount_of_trees = 0
old_amount_of_trees = 0


# Генерация начального состояния
def initialize_field(_field):
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
                    res = [TREE_TYPE, randint(0,20)]
                elif q <= 1 - predator_probability:
                    new_being = [0] * AMOUNT_OF_STATUSES
                    new_being[TYPE] = HERBIVORE_TYPE
                    new_being[ENERGY] = herbivore_starting_energy
                    new_being[STATUS_ACTION] = STATUS_ACTION_READY
                    new_being[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                    res = new_being
                else:
                    new_being = [0] * AMOUNT_OF_STATUSES
                    new_being[TYPE] = PREDATOR_TYPE
                    new_being[ENERGY] = predator_starting_energy
                    new_being[STATUS_ACTION] = STATUS_ACTION_READY
                    new_being[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                    res = new_being
            _field[y][x] = res


# [тип, кол-во энергии]


# Обновление поля
def update_field(_field):
    print(_field)
    _height = len(_field)
    _width = len(_field[0])
    _new_field = [[0 for _ in range(width)] for _ in range(height)]
    # new_field = [[None for _ in range(_width)] for _ in range(_height)]


    for y in range(len(_field)):
        for x in range(len(_field[y])):
            if _field[y][x] is not None:
                if _field[y][x] != 0:

                    if _field[y][x][TYPE] == TREE_TYPE:
                        _field[y][x][ENERGY] += tree_energy_per_tick
                        _new_field[y][x] = _field[y][x].copy()
                        if _field[y][x][ENERGY] >= tree_min_breeding_energy:
                            breeded = False
                            breed = tree_breed_size
                            # up
                            if breed != 0:
                                if y > 0:
                                    if _field[y-1][x] == 0:
                                        _new_field[y-1][x] = [TREE_TYPE, tree_starting_energy]
                                        breeded = True
                                        breed -= 1
                            # right
                            if breed != 0:
                                if x < width-1:
                                    if _field[y][x+1] == 0:
                                        _new_field[y][x+1] = [TREE_TYPE, tree_starting_energy]
                                        breeded = True
                                        breed -= 1
                            # down
                            if breed != 0:
                                if y < height - 1:
                                    if _field[y+1][x] == 0:
                                        _new_field[y+1][x] = [TREE_TYPE, tree_starting_energy]
                                        breeded = True
                                        breed -= 1
                            # left
                            if breed != 0:
                                if x > 0:
                                    if _field[y][x-1] == 0:
                                        _new_field[y][x-1] = [TREE_TYPE, tree_starting_energy]
                                        breeded = True
                                        breed -= 1
                            if breeded:
                                _new_field[y][x][ENERGY] -= tree_energy_for_breeding


                    # [тип, энергия, состояие, направление]
                    # состояния:
                    # 0 - готов к действию
                    # 1 - размножился
                    # 2 - поел
                    # 3 - выбрано направление

                    # направления:
                    # 1 верх
                    # 2 право
                    # 3 низ
                    # 4 лево

                    elif _field[y][x][TYPE] == HERBIVORE_TYPE:

                        _field[y][x][ENERGY] += herbivore_energy_per_tick
                        # проверка на энергию, смерть от голода
                        if _field[y][x][ENERGY] <0:
                            if tree_on_death:
                                _field[y][x] = 0
                                _new_field[y][x] = [TREE_TYPE, tree_starting_energy]
                            else:
                                _field[y][x] = 0
                                _new_field[y][x] = 0
                        else:

                            moved = False
                            can_breed = False
                            breed_cost_paid = False
                            if _field[y][x][ENERGY] >= herbivore_min_breeding_energy:
                                can_breed = True

                            # размножение или охота на деревья или передвижение от хищника
                            random_directions = [i for i in range(CHOSEN_DIRECTION_UP, CHOSEN_DIRECTION_LEFT+1)]
                            shuffle(random_directions)
                            for direction in random_directions:
                                # up
                                if direction == CHOSEN_DIRECTION_UP:
                                    if not moved:
                                        if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                            if y > 0:
                                                if _field[y - 1][x] == 0:
                                                    if can_breed:
                                                        new_pred = [0]*AMOUNT_OF_STATUSES
                                                        new_pred[TYPE] = HERBIVORE_TYPE
                                                        new_pred[ENERGY] = predator_starting_energy
                                                        new_pred[STATUS_ACTION] = STATUS_ACTION_READY
                                                        new_pred[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                        _field[y - 1][x] = new_pred
                                                        _new_field[y - 1][x] = new_pred
                                                        _field[y - 1][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION

                                                        if not breed_cost_paid:
                                                            _field[y][x][ENERGY] -= predator_breeding_cost
                                                            breed_cost_paid = True
                                                        can_breed = False

                                                        _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        break


                                                elif _field[y-1][x][TYPE] == TREE_TYPE:
                                                    # удаляем дерево
                                                    _field[y - 1][x] = 0
                                                    _new_field[y-1][x] = 0

                                                    # добавляем энергию за дерево травоядному, перемещаем его на бывшую клетку дерева
                                                    _field[y][x][ENERGY] += herbivore_energy_for_eating_a_tree
                                                    _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                    _new_field[y - 1][x] = _field[y][x].copy()
                                                    _field[y - 1][x] = _field[y][x].copy()
                                                    _new_field[y - 1][x][STATUS_ACTION] = STATUS_ACTION_READY
                                                    moved = True

                                                    _field[y][x] = 0

                                                    break

                                                elif _field[y - 1][x][TYPE] == PREDATOR_TYPE:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_CHOSEN_DIRECTION
                                                    _field[y][x][CHOSEN_DIRECTION] = CHOSEN_DIRECTION_DOWN
                                                    _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] = randint(herbivore_min_movement_distance, herbivore_max_movement_distance)
                                                    break
                                # right
                                if direction == CHOSEN_DIRECTION_RIGHT:
                                    if not moved:
                                        if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                            # right
                                            if x < width-1:
                                                if _field[y][x + 1] == 0:
                                                    if can_breed:
                                                        new_being = [0]*AMOUNT_OF_STATUSES
                                                        new_being[TYPE] = HERBIVORE_TYPE
                                                        new_being[ENERGY] = herbivore_starting_energy
                                                        new_being[STATUS_ACTION] = STATUS_ACTION_READY
                                                        new_being[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                        _field[y][x + 1] = new_being
                                                        _field[y][x + 1][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _new_field[y][x + 1] = new_being

                                                        if not breed_cost_paid:
                                                            _field[y][x][ENERGY] -= herbivore_breeding_cost
                                                            breed_cost_paid = True
                                                        can_breed = False

                                                        _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        break


                                                elif _field[y][x + 1][TYPE] == TREE_TYPE:
                                                    # удаляем дерево
                                                    _field[y][x + 1] = 0
                                                    _new_field[y][x + 1] = 0

                                                    # добавляем энергию за дерево травоядному, перемещаем его на бывшую клетку дерева
                                                    _field[y][x][ENERGY] += herbivore_energy_for_eating_a_tree
                                                    _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                    _new_field[y][x + 1] = _field[y][x].copy()
                                                    _field[y][x + 1] = _field[y][x].copy()
                                                    _new_field[y][x + 1][STATUS_ACTION] = STATUS_ACTION_READY
                                                    moved = True

                                                    _field[y][x] = 0

                                                    break

                                                elif _field[y][x + 1][TYPE] == PREDATOR_TYPE:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_CHOSEN_DIRECTION
                                                    _field[y][x][CHOSEN_DIRECTION] = CHOSEN_DIRECTION_LEFT
                                                    _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] = randint(
                                                        herbivore_min_movement_distance, herbivore_max_movement_distance)
                                                    break


                                # down
                                if direction == CHOSEN_DIRECTION_DOWN:
                                    if not moved:
                                        if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                            if y < height - 1:
                                                if _field[y + 1][x] == 0:
                                                    if can_breed:
                                                        new_being = [0] * AMOUNT_OF_STATUSES
                                                        new_being[TYPE] = HERBIVORE_TYPE
                                                        new_being[ENERGY] = herbivore_starting_energy
                                                        new_being[STATUS_ACTION] = STATUS_ACTION_READY
                                                        new_being[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                        _field[y + 1][x] = new_being
                                                        _field[y + 1][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _new_field[y + 1][x] = new_being

                                                        if not breed_cost_paid:
                                                            _field[y][x][ENERGY] -= herbivore_breeding_cost
                                                            breed_cost_paid = True
                                                        can_breed = False
                                                        _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        break

                                                elif _field[y + 1][x][TYPE] == TREE_TYPE:
                                                    # удаляем дерево
                                                    _field[y + 1][x] = 0
                                                    _new_field[y + 1][x] = 0

                                                    # добавляем энергию за дерево травоядному, перемещаем его на бывшую клетку дерева
                                                    _field[y][x][ENERGY] += herbivore_energy_for_eating_a_tree
                                                    _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                    _new_field[y + 1][x] = _field[y][x].copy()
                                                    _field[y + 1][x] = _field[y][x].copy()
                                                    _new_field[y + 1][x][STATUS_ACTION] = STATUS_ACTION_READY

                                                    _field[y][x] = 0

                                                    moved = True
                                                    break

                                                elif _field[y + 1][x][TYPE] == PREDATOR_TYPE:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_CHOSEN_DIRECTION
                                                    _field[y][x][CHOSEN_DIRECTION] = CHOSEN_DIRECTION_UP
                                                    _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] = randint(
                                                        herbivore_min_movement_distance, herbivore_max_movement_distance)
                                                    break


                                # left
                                if direction == CHOSEN_DIRECTION_LEFT:
                                    if not moved:
                                        if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                            if x > 0:
                                                if _field[y][x - 1] == 0:
                                                    if can_breed:
                                                        new_being = [0] * AMOUNT_OF_STATUSES
                                                        new_being[TYPE] = HERBIVORE_TYPE
                                                        new_being[ENERGY] = herbivore_starting_energy
                                                        new_being[STATUS_ACTION] = STATUS_ACTION_READY
                                                        new_being[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                        _field[y][x - 1] = new_being
                                                        _field[y][x - 1][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _new_field[y][x - 1] = new_being


                                                        if not breed_cost_paid:
                                                            _field[y][x][ENERGY] -= herbivore_breeding_cost
                                                            breed_cost_paid = True
                                                        can_breed = False
                                                        _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        break


                                                elif _field[y][x - 1][TYPE] == TREE_TYPE:
                                                    # удаляем дерево
                                                    _field[y][x - 1] = 0
                                                    _new_field[y][x - 1] = 0

                                                    # добавляем энергию за дерево травоядному, перемещаем его на бывшую клетку дерева
                                                    _field[y][x][ENERGY] += herbivore_energy_for_eating_a_tree
                                                    _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                    _new_field[y][x - 1] = _field[y][x].copy()
                                                    _field[y][x - 1] = _field[y][x].copy()
                                                    _new_field[y][x - 1][STATUS_ACTION] = STATUS_ACTION_READY

                                                    moved = True

                                                    _field[y][x] = 0

                                                    break

                                                elif _field[y][x - 1][TYPE] == PREDATOR_TYPE:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_CHOSEN_DIRECTION
                                                    _field[y][x][CHOSEN_DIRECTION] = CHOSEN_DIRECTION_RIGHT
                                                    _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] = randint(
                                                        herbivore_min_movement_distance, herbivore_max_movement_distance)
                                                    break




                                # перемещение если нет ничего вокруг
                            if not moved:
                                if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                    if _field[y][x][STATUS_DIRECTION] == STATUS_DIRECTION_NO_DIRECTION:
                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_CHOSEN_DIRECTION
                                        _field[y][x][CHOSEN_DIRECTION] = randint(CHOSEN_DIRECTION_UP, CHOSEN_DIRECTION_LEFT)
                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] = randint(herbivore_min_movement_distance, herbivore_max_movement_distance)

                                    if _field[y][x][STATUS_DIRECTION] == STATUS_DIRECTION_CHOSEN_DIRECTION:
                                        if _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] <= 0:
                                            _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                        else:
                                            if _field[y][x][CHOSEN_DIRECTION] == CHOSEN_DIRECTION_UP:
                                                if y > 0:
                                                    if _field[y - 1][x] == 0:
                                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] -= 1
                                                        _new_field[y - 1][x] = _field[y][x].copy()
                                                        _field[y - 1][x] = _field[y][x].copy()
                                                        _field[y - 1][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _field[y][x] = 0
                                                        moved = True
                                                    else:
                                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                                else:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                            elif _field[y][x][CHOSEN_DIRECTION] == CHOSEN_DIRECTION_RIGHT:
                                                if x < width - 1:
                                                    if _field[y][x + 1] == 0:
                                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] -= 1
                                                        _new_field[y][x + 1] = _field[y][x].copy()
                                                        _field[y][x + 1] = _field[y][x].copy()
                                                        _field[y][x + 1][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _field[y][x] = 0
                                                        moved = True
                                                    else:
                                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                                else:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                            elif _field[y][x][CHOSEN_DIRECTION] == CHOSEN_DIRECTION_DOWN:
                                                if y < height - 1:
                                                    if _field[y + 1][x] == 0:
                                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] -= 1
                                                        _new_field[y + 1][x] = _field[y][x].copy()
                                                        _field[y + 1][x] = _field[y][x].copy()
                                                        _field[y + 1][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _field[y][x] = 0
                                                        moved = True
                                                    else:
                                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                                else:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                            elif _field[y][x][CHOSEN_DIRECTION] == CHOSEN_DIRECTION_LEFT:
                                                if x > 0:
                                                    if _field[y][x - 1] == 0:
                                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] -= 1
                                                        _new_field[y][x - 1] = _field[y][x].copy()
                                                        _field[y][x - 1] = _field[y][x].copy()
                                                        _field[y][x - 1][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _field[y][x] = 0
                                                        moved = True
                                                    else:
                                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                                else:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                if not moved:
                                    _new_field[y][x] = _field[y][x].copy()
                                    _new_field[y][x][STATUS_ACTION] = STATUS_ACTION_READY








                    elif _field[y][x][0] == PREDATOR_TYPE:
                        _field[y][x][ENERGY] += predator_energy_per_tick
                        # проверка на энергию, смерть от голода
                        if _field[y][x][ENERGY] <0:
                            if tree_on_death:
                                _field[y][x] = 0
                                _new_field[y][x] = [TREE_TYPE, tree_starting_energy]
                            else:
                                _field[y][x] = 0
                                _new_field[y][x] = 0
                        else:

                            moved = False
                            can_breed = False
                            breed_cost_paid = False
                            if _field[y][x][ENERGY] >= predator_min_breeding_energy:
                                can_breed = True

                            # размножение или охота на деревья или передвижение от хищника
                            random_directions = [i for i in range(CHOSEN_DIRECTION_UP, CHOSEN_DIRECTION_LEFT+1)]
                            shuffle(random_directions)
                            for direction in random_directions:
                                # up
                                if direction == CHOSEN_DIRECTION_UP:
                                    if not moved:
                                        if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                            if y > 0:
                                                if _field[y - 1][x] == 0:
                                                    if can_breed:
                                                        new_being = [0]*AMOUNT_OF_STATUSES
                                                        new_being[TYPE] = PREDATOR_TYPE
                                                        new_being[ENERGY] = predator_starting_energy
                                                        new_being[STATUS_ACTION] = STATUS_ACTION_READY
                                                        new_being[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                        _field[y - 1][x] = new_being
                                                        _new_field[y - 1][x] = new_being
                                                        _field[y - 1][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION

                                                        if not breed_cost_paid:
                                                            _field[y][x][ENERGY] -= predator_breeding_cost
                                                            breed_cost_paid = True
                                                        can_breed = False

                                                        _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        break


                                                elif _field[y-1][x][TYPE] == HERBIVORE_TYPE:
                                                    # удаляем дерево
                                                    _field[y - 1][x] = 0
                                                    _new_field[y-1][x] = 0

                                                    # добавляем энергию за дерево травоядному, перемещаем его на бывшую клетку дерева
                                                    _field[y][x][ENERGY] += predator_energy_for_eating_a_herbivore
                                                    _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                    _new_field[y - 1][x] = _field[y][x].copy()
                                                    _field[y - 1][x] = _field[y][x].copy()
                                                    _new_field[y - 1][x][STATUS_ACTION] = STATUS_ACTION_READY
                                                    moved = True

                                                    _field[y][x] = 0

                                                    break

                                # right
                                if direction == CHOSEN_DIRECTION_RIGHT:
                                    if not moved:
                                        if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                            # right
                                            if x < width-1:
                                                if _field[y][x + 1] == 0:
                                                    if can_breed:
                                                        new_being = [0]*AMOUNT_OF_STATUSES
                                                        new_being[TYPE] = PREDATOR_TYPE
                                                        new_being[ENERGY] = predator_starting_energy
                                                        new_being[STATUS_ACTION] = STATUS_ACTION_READY
                                                        new_being[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                        _field[y][x + 1] = new_being
                                                        _field[y][x + 1][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _new_field[y][x + 1] = new_being

                                                        if not breed_cost_paid:
                                                            _field[y][x][ENERGY] -= predator_breeding_cost
                                                            breed_cost_paid = True
                                                        can_breed = False

                                                        _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        break


                                                elif _field[y][x + 1][TYPE] == HERBIVORE_TYPE:
                                                    # удаляем дерево
                                                    _field[y][x + 1] = 0
                                                    _new_field[y][x + 1] = 0

                                                    # добавляем энергию за дерево травоядному, перемещаем его на бывшую клетку дерева
                                                    _field[y][x][ENERGY] += predator_energy_for_eating_a_herbivore
                                                    _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                    _new_field[y][x + 1] = _field[y][x].copy()
                                                    _field[y][x + 1] = _field[y][x].copy()
                                                    _new_field[y][x + 1][STATUS_ACTION] = STATUS_ACTION_READY
                                                    moved = True

                                                    _field[y][x] = 0

                                                    break



                                # down
                                if direction == CHOSEN_DIRECTION_DOWN:
                                    if not moved:
                                        if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                            if y < height - 1:
                                                if _field[y + 1][x] == 0:
                                                    if can_breed:
                                                        new_being = [0] * AMOUNT_OF_STATUSES
                                                        new_being[TYPE] = PREDATOR_TYPE
                                                        new_being[ENERGY] = predator_starting_energy
                                                        new_being[STATUS_ACTION] = STATUS_ACTION_READY
                                                        new_being[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                        _field[y + 1][x] = new_being
                                                        _field[y + 1][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _new_field[y + 1][x] = new_being

                                                        if not breed_cost_paid:
                                                            _field[y][x][ENERGY] -= predator_breeding_cost
                                                            breed_cost_paid = True
                                                        can_breed = False
                                                        _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        break

                                                elif _field[y + 1][x][TYPE] == HERBIVORE_TYPE:
                                                    # удаляем дерево
                                                    _field[y + 1][x] = 0
                                                    _new_field[y + 1][x] = 0

                                                    # добавляем энергию за дерево травоядному, перемещаем его на бывшую клетку дерева
                                                    _field[y][x][ENERGY] += predator_energy_for_eating_a_herbivore
                                                    _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                    _new_field[y + 1][x] = _field[y][x].copy()
                                                    _field[y + 1][x] = _field[y][x].copy()
                                                    _new_field[y + 1][x][STATUS_ACTION] = STATUS_ACTION_READY

                                                    _field[y][x] = 0

                                                    moved = True
                                                    break



                                # left
                                if direction == CHOSEN_DIRECTION_LEFT:
                                    if not moved:
                                        if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                            if x > 0:
                                                if _field[y][x - 1] == 0:
                                                    if can_breed:
                                                        new_being = [0] * AMOUNT_OF_STATUSES
                                                        new_being[TYPE] = PREDATOR_TYPE
                                                        new_being[ENERGY] = predator_starting_energy
                                                        new_being[STATUS_ACTION] = STATUS_ACTION_READY
                                                        new_being[STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                        _field[y][x - 1] = new_being
                                                        _field[y][x - 1][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _new_field[y][x - 1] = new_being


                                                        if not breed_cost_paid:
                                                            _field[y][x][ENERGY] -= predator_breeding_cost
                                                            breed_cost_paid = True
                                                        can_breed = False
                                                        _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        break


                                                elif _field[y][x - 1][TYPE] == HERBIVORE_TYPE:
                                                    # удаляем дерево
                                                    _field[y][x - 1] = 0
                                                    _new_field[y][x - 1] = 0

                                                    # добавляем энергию за дерево травоядному, перемещаем его на бывшую клетку дерева
                                                    _field[y][x][ENERGY] += predator_energy_for_eating_a_herbivore
                                                    _field[y][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                                    _new_field[y][x - 1] = _field[y][x].copy()
                                                    _field[y][x - 1] = _field[y][x].copy()
                                                    _new_field[y][x - 1][STATUS_ACTION] = STATUS_ACTION_READY

                                                    moved = True

                                                    _field[y][x] = 0

                                                    break





                                # перемещение если нет ничего вокруг
                            if not moved:
                                if _field[y][x][STATUS_ACTION] == STATUS_ACTION_READY:
                                    if _field[y][x][STATUS_DIRECTION] == STATUS_DIRECTION_NO_DIRECTION:
                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_CHOSEN_DIRECTION
                                        _field[y][x][CHOSEN_DIRECTION] = randint(CHOSEN_DIRECTION_UP, CHOSEN_DIRECTION_LEFT)
                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] = randint(predator_min_movement_distance, predator_max_movement_distance)

                                    if _field[y][x][STATUS_DIRECTION] == STATUS_DIRECTION_CHOSEN_DIRECTION:
                                        if _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] <= 0:
                                            _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION

                                        else:
                                            if _field[y][x][CHOSEN_DIRECTION] == CHOSEN_DIRECTION_UP:
                                                if y > 0:
                                                    if _field[y - 1][x] == 0:
                                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] -= 1
                                                        _new_field[y - 1][x] = _field[y][x].copy()
                                                        _field[y - 1][x] = _field[y][x].copy()
                                                        _field[y - 1][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _field[y][x] = 0
                                                        moved = True
                                                    else:
                                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                                else:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                            elif _field[y][x][CHOSEN_DIRECTION] == CHOSEN_DIRECTION_RIGHT:
                                                if x < width - 1:
                                                    if _field[y][x + 1] == 0:
                                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] -= 1
                                                        _new_field[y][x + 1] = _field[y][x].copy()
                                                        _field[y][x + 1] = _field[y][x].copy()
                                                        _field[y][x + 1][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _field[y][x] = 0
                                                        moved = True
                                                    else:
                                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                                else:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                            elif _field[y][x][CHOSEN_DIRECTION] == CHOSEN_DIRECTION_DOWN:
                                                if y < height - 1:
                                                    if _field[y + 1][x] == 0:
                                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] -= 1
                                                        _new_field[y + 1][x] = _field[y][x].copy()
                                                        _field[y + 1][x] = _field[y][x].copy()
                                                        _field[y + 1][x][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _field[y][x] = 0
                                                        moved = True
                                                    else:
                                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                                else:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                            elif _field[y][x][CHOSEN_DIRECTION] == CHOSEN_DIRECTION_LEFT:
                                                if x > 0:
                                                    if _field[y][x - 1] == 0:
                                                        _field[y][x][CHOSEN_DIRECTION_MOVES_LEFT] -= 1
                                                        _new_field[y][x - 1] = _field[y][x].copy()
                                                        _field[y][x - 1] = _field[y][x].copy()
                                                        _field[y][x - 1][STATUS_ACTION] = STATUS_ACTION_COMPLETED_ACTION
                                                        _field[y][x] = 0
                                                        moved = True
                                                    else:
                                                        _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                                else:
                                                    _field[y][x][STATUS_DIRECTION] = STATUS_DIRECTION_NO_DIRECTION
                                if not moved:
                                    _new_field[y][x] = _field[y][x].copy()
                                    _new_field[y][x][STATUS_ACTION] = STATUS_ACTION_READY



    return _new_field


# Рисование игрового поля
def draw_field(_canvas, _field, _cell_size=10):
    _canvas.delete("all")
    for y in range(len(_field)):
        for x in range(len(_field[y])):
            if _field[y][x] is not None:
                if _field[y][x] != 0:

                    if _field[y][x][0] == TREE_TYPE:
                        _canvas.create_polygon( # Зелёные треугольники
                            x * _cell_size + _cell_size // 2,
                            y * _cell_size,
                            x * _cell_size,
                            y * _cell_size + _cell_size,
                            (x + 1) * _cell_size, y * _cell_size + _cell_size,
                            fill="green", outline=""
                        )
                    elif _field[y][x][0] == HERBIVORE_TYPE:
                        _canvas.create_oval(
                            x * _cell_size, y * _cell_size,
                            (x + 1) * _cell_size, (y + 1) * _cell_size,
                            fill="grey", outline=""
                        )
                    elif _field[y][x][0] == PREDATOR_TYPE:
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
        time.sleep(0.05)


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





















