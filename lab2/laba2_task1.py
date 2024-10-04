# no и yes - меньше/больше.
# дерево элементов. В нём и ищем.
# работает только с отсортированными массивами
import random
from typing import List


class Teacher:
    def __init__(self, characteristics: List, name: str):
        self.characteristics = characteristics
        self.name = name

    def __repr__(self):
        return f"Teacher({self.characteristics!r},{self.name!r}"
        # return f"Teacher({self.name!r}"


t_abs = Teacher([
    "мужчина",
    "молодой",
    "ведёт IT-предмет",
    "ведёт физику",
    "ведёт электронику",
    "ведёт электротехнику",
    "ведёт проектный практикум",
    "ведёт физкультуру",
    "ведёт высшую математику",
    "ведёт ИТИП",
    "ведёт теорию вероятностей",
    "ведёт дисркетную математику",
    "ведёт и лекции и лабораторные",
    "ведёт только лекции",
    "ведёт только лабораторные/практики"
], "имя препода")

t1 = Teacher([
    "мужчина",
    "ведёт физику",
    "ведёт только лекции"
], "Вальковский Сергей Николаевич. Физика - лекции")
t2 = Teacher([
    "мужчина",
    "ведёт физику",
    "ведёт только лабораторные/практики"
], "Полищук Юрий Владимирович. Физика - практика")
t3 = Teacher([
    "мужчина",
    "ведёт электронику",
    "ведёт только лекции"
], "Власов Вячеслав Петрович. Электионика - лекции")
t4 = Teacher([
    "женщина",
    "ведёт электротехнику",
    "ведёт и лекции и лабораторные",
    "вызывает страх у студентов"
], "Семёнова Татьяна Николаевна. Электротехника")
t5 = Teacher([
    "женщина",
    "молодой",
    "ведёт IT-предмет",
    "ведёт ИТИП",
    "ведёт только лабораторные/практики"
], "Мосева Марина Сергеевна. ИТИП - практики")
t6 = Teacher([
    "мужчина",
    "молодой",
    "ведёт IT-предмет",
    "ведёт ИТИП",
    "рассказывал вам про процессор",
    "ведёт только лекции",
], "Симонов Сергей Евгеньевич. ИТИП - лекции")
t7 = Teacher([
    "женщина",
    "ведёт теорию вероятностей",
    "ведёт и лекции и лабораторные"
], "Скородумова Елена Александровна. Вероятности")
t8 = Teacher([
    "женщина",
    "ведёт проектный практикум",
], "Петросян Вера Рафаэловна. Проектный практикум")
t9 = Teacher([
    "молодой",
    "женщина",
    "ведёт дисркетную математику",
], "Изотова Анастасия Андреевна. дисркетная математика")
t10 = Teacher([
    "женщина",
    "ведёт физкультуру",
], "Королева Светлана Анатольевна. Физкультура")
t11 = Teacher([
    "женщина",
    "ведёт высшую математику",
], "Шаймарданова Лилия Кимматовна. высшая математика")

teachers = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]


class AkinatorController:

    def __init__(self, _teachers: List, debug=False):

        self._debug = debug

        self.searchable_techers = None  # меняющийся по мере поиска список учителей
        self.false_chars = None
        self.true_chars = None
        self.to_be_asked_chars = None
        self.possible_chars = None

        self._teachers = _teachers
        # print(self.possible_chars)

    def start(self):
        self.possible_chars = self.get_all_chars(self._teachers)

        self.searchable_techers = self._teachers.copy()
        self.to_be_asked_chars = self.possible_chars.copy()
        self.true_chars = []
        self.false_chars = []

        random.shuffle(self.to_be_asked_chars)
        while True:
            if len(self.searchable_techers) == 0:
                print("преподаватель не найден")
                self.add_teacher_script()
                return
            elif len(self.searchable_techers) == 1:
                answer = self.get_answer(f"Ваш преподаватель - {self.searchable_techers[0].name}?")
                if answer:
                    print("Отлично! Акинатор угадал!")
                    answer = self.get_answer("Попробовать заново?")
                    if answer:
                        self.start()
                        return
                    return
                else:
                    # TODO сделать нормальный контроллер приложения
                    answer = self.get_answer("Попробовать заново?")
                    if answer:
                        self.start()
                        return
                    self.add_teacher_script()
                    return
            else:
                if len(self.to_be_asked_chars) != 0:
                    asked_char = self.to_be_asked_chars.pop(0)
                    answer = self.get_answer(f"Ваш преподаватель - {asked_char}?")
                    if answer:
                        self.true_chars.append(asked_char)
                        self.remove_teachers_without_this_char(asked_char)
                    else:
                        self.false_chars.append(asked_char)
                        self.remove_trachers_with_this_char(asked_char)

                    self.to_be_asked_chars = self.get_all_chars(self.searchable_techers)
                    for x in self.true_chars:
                        if x in self.to_be_asked_chars:
                            self.to_be_asked_chars.remove(x)

                    if self._debug:
                        self.print_debug_data()

    def print_debug_data(self):
        print(self.to_be_asked_chars)
        print(self.true_chars)
        print(self.false_chars)
        print(self.searchable_techers)

    def remove_teachers_without_this_char(self, char: str):
        self.searchable_techers = list(
            filter(lambda _teacher: char in _teacher.characteristics, self.searchable_techers))

    def remove_trachers_with_this_char(self, char: str):
        self.searchable_techers = list(
            filter(lambda _teacher: char not in _teacher.characteristics, self.searchable_techers))

    def add_teacher_script(self):
        answer = self.get_answer("добавить нового преподавателя?")
        if answer:
            res = str(input("Введите имя нового преподавателя: "))
            new_teacher = Teacher(self.true_chars, res)
            while True:
                print("\nВот характеристики вашего нового преподавателя:")
                print(new_teacher.characteristics)
                print("Вот все уже существующие характеристики:")
                print(self.get_all_chars(self._teachers))
                res = str(input(
                    "Введите характеристику, которая будет у нового преподавателя. Она может быть из спика выше, или совершенно новой \n(либо введите 0 чтобы закончить создание): ")).strip()
                if res == "0":
                    print(f"Вы создали и добавили нового преподавателя: {new_teacher!r}")
                    self._teachers.append(new_teacher)
                    return
                elif res in self.true_chars:
                    print("У вашего учителя уже есть эта характеристика")
                else:
                    print(f"Вашему преподавателю добавлена новая характеристика: {res}")
                    new_teacher.characteristics.append(res)
                    print(f"Текущие параметры преподавателя: {new_teacher!r}")
        else:
            return

    @staticmethod
    def get_answer(question: str) -> bool:
        print("\n")
        print(question)
        i = 0
        while True:
            answer = input("Введите да/нет или 1/0 для ответа: ").strip().lower()
            if answer == "да" or answer == "1":
                return True
            elif answer == "yes" or answer == "0":
                return False
            else:
                i += 1
                print("неправильный формат ответа")
                if i == 5:
                    i = 0
                    print(question)

    @staticmethod
    def get_all_chars(_teachers: List) -> List:
        result = set()
        for teacher in _teachers:
            for x in teacher.characteristics:
                result.add(x)
        return list(result)


controller = AkinatorController(teachers)
while True:
    controller.start()
