# Q-деревья
from random import randint
from typing import Tuple, List

import matplotlib.pyplot as plt

DOT_SEARCH_STATUS = 0

def drow_line(x1, y1, x2, y2):
   plt.plot([x1, x2], [y1, y2], color='b')

def drow_dot_blue(x,y):
    plt.scatter(x, y, s=7, c='b')

def drow_dot_red(x,y,annotation):
    plt.annotate(annotation, (x, y), xytext=(3, 3), textcoords='offset points', fontsize=8)
    plt.scatter(x, y, s=7, c='r')


def fill_yellow(x1, y1, x2, y2):
    plt.fill_between((x1, x2), y1, y2, color='y', alpha=0.2)

def fill_red(x1, y1, x2, y2):
    plt.fill_between((x1, x2), y1, y2, color='r', alpha=0.2)

class Dot:

    def __init__(self, x, y, id = -1):
        self.x = x
        self.y = y
        self.id = id

    def __repr__(self):
        return f"Dot(x={self.x!r},y={self.y!r})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Tree:
    def __init__(self, low_left_end: Dot, high_right_end: Dot):
        self.low_left_end = low_left_end
        self.high_right_end = high_right_end
        self._dot = None
        self.has_children = False

        self.children = None
        self.drow_borders()

    def add_dot(self, _dot: Dot):

        drow_dot_red(_dot.x,_dot.y,_dot.id)

        if self._dot is None and not self.has_children:
            self._dot = _dot
        elif self.has_children:
            for tree in self.children:
                if tree.contains_the_dot(_dot):
                    tree.add_dot(_dot)
        else:
            self.has_children = True
            self.children = self.create_children()
            for tree in self.children:
                if tree.contains_the_dot(_dot):
                    tree.add_dot(_dot)
                if tree.contains_the_dot(self._dot):
                    tree.add_dot(self._dot)
            self._dot = None

    def create_children(self):
        base_x = self.low_left_end.x
        base_y = self.low_left_end.y
        delta = (self.high_right_end.x - self.low_left_end.x) // 2
        t1 = Tree(Dot(base_x + delta, base_y + delta), Dot(base_x + delta + delta, base_y + delta + delta))
        t2 = Tree(Dot(base_x, base_y + delta), Dot(base_x + delta, base_y + delta + delta))
        t3 = Tree(Dot(base_x, base_y), Dot(base_x + delta, base_y + delta))
        t4 = Tree(Dot(base_x + delta, base_y), Dot(base_x + delta + delta, base_y + delta))
        return [t1, t2, t3, t4]

    def drow_borders(self):
        drow_line(self.low_left_end.x, self.low_left_end.y, self.high_right_end.x, self.low_left_end.y)
        drow_line(self.low_left_end.x, self.low_left_end.y, self.low_left_end.x, self.high_right_end.y)
        drow_line(self.high_right_end.x, self.high_right_end.y, self.high_right_end.x, self.low_left_end.y)
        drow_line(self.high_right_end.x, self.high_right_end.y, self.low_left_end.x, self.high_right_end.y)
        # plt.plot((10,20), (20,30))
        # plt.plot((self.high_right_end.x, self.high_right_end.y), (self.low_left_end.x, self.low_left_end.y))
        # plt.plot((self.high_right_end.x, self.high_right_end.y), (self.low_left_end.x, self.low_left_end.y))

    def contains_the_dot(self, _dot: Dot):
        if _dot == self.high_right_end:
            return True
        return (self.low_left_end.x < _dot.x <= self.high_right_end.x) and (
                    self.low_left_end.y < _dot.y <= self.high_right_end.y)

    def color_yellow(self):
        fill_yellow(self.low_left_end.x, self.low_left_end.y, self.high_right_end.x, self.high_right_end.y)

    def color_red(self):
        fill_red(self.low_left_end.x, self.low_left_end.y, self.high_right_end.x, self.high_right_end.y)

    def search(self, search_id):
        global DOT_SEARCH_STATUS
        if not self._dot is None and DOT_SEARCH_STATUS == 0:
            if self._dot.id == search_id:
                self.color_red()
                DOT_SEARCH_STATUS = 1

        if self.has_children and DOT_SEARCH_STATUS == 0:
            for x in self.children:
                x.search(search_id)

        if DOT_SEARCH_STATUS == 1:
            self.search_closest(search_id)

    def search_closest(self, search_id):
        global DOT_SEARCH_STATUS
        if not self._dot is None and DOT_SEARCH_STATUS == 1 and self._dot.id != search_id:
            self.color_yellow()
            DOT_SEARCH_STATUS = 2

        if self.has_children and DOT_SEARCH_STATUS == 1:
            for x in self.children:
                x.search_closest(search_id)


    def __repr__(self):
        return f"Tree({self.low_left_end!r},{self.high_right_end!r})"



size_max = 128
step = 8
dots = 30


plt.xticks(list(x for x in range(0, size_max + step, step)))
plt.yticks(list(x for x in range(0, size_max + step, step)))

plt.xlim(0, size_max)
plt.ylim(0, size_max)

main_tree = Tree(Dot(0, 0), Dot(size_max, size_max))

for i in range(dots):
    dot = Dot(randint(1,size_max),randint(1,size_max), id=i)
    main_tree.add_dot(dot)

plt.savefig('plots/plot1.png')
# plt.show()

dot_id = int(input("Введите ID точки, сеседей которой ищете: "))
main_tree.search(dot_id)
# main_tree.children[1].color_yellow()

plt.savefig('plots/plot2.png')

