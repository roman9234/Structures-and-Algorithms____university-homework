from random import randint
from typing import List
import matplotlib.pyplot as plt


class Hotel:
    _basic_price = 10

    def __init__(self):
        # оценка отеля от 0 до 10, равна половине звёздности, например 7 = 3.5 звезды, 10 = 5 звёзд, 3 = 1.5 звёзд
        self.star_points = randint(0, 10)
        self.price_per_star_point = randint(5, 15)
        # self.price_per_star_point = 10
        self.price = self.star_points * self.price_per_star_point + self._basic_price

    def __str__(self):
        return f"Отель {self.star_points / 2} звёзд, цена {self.price}, цена за звезду {self.price_per_star_point / 2}"


class Algorithms:

    # s - число, после которого
    @staticmethod
    def algorithm_37(amount_of_steps=100, s=37, debug=False):
        current_best = Hotel()
        for i in range(1, amount_of_steps):
            new_hotel = Hotel()
            if debug: new_hotel.__str__()
            if debug: print(i)
            if i <= round(amount_of_steps * (s / 100)):
                if Algorithms.check_if_new_hotel_is_better(new_hotel, current_best):
                    current_best = new_hotel
                    if debug: print(f"Взят как новый лучший")
            else:
                if Algorithms.check_if_new_hotel_is_better(new_hotel, current_best):
                    if debug: new_hotel.__str__()
                    if debug: print("Выбран")
                    return new_hotel
        return None

    @staticmethod
    def check_if_new_hotel_is_better(new_hotel: Hotel, old_hotel: Hotel):
        return new_hotel.star_points >= old_hotel.star_points and new_hotel.price_per_star_point >= old_hotel.price_per_star_point


class AlgorithmEvaluator:
    @staticmethod
    def statistics_of_algoritm(amount_of_steps=100, s=37, amount_of_iterations=100):
        chosen_values = []
        for _i in range(amount_of_iterations):
            _result_hotel = Algorithms.algorithm_37(amount_of_steps=amount_of_steps, s=s)
            chosen_values.append(_result_hotel)
        _result = AlgorithmEvaluator.average_hotel_values_estimator(chosen_values)
        # print(AlgorithmEvaluator.results_as_str(result), f"число итераций = {amount_of_iterations}, число s = {s}")
        return _result

    # Получает на вход список выбранный алгоритмами отелей и оцениквает параметры этого спика
    @staticmethod
    def average_hotel_values_estimator(_lst: List):
        _result_values = {"average_star_points": None, "average_price_per_star_point": None, "good_results": 0,
                          "none_results": 0, "res_percent": 0}
        _star_pints = []
        _prices_per_start_point = []
        for hotel in _lst:
            if hotel is None:
                _result_values["none_results"] += 1
            else:
                _result_values["good_results"] += 1
                _star_pints.append(hotel.star_points)
                _prices_per_start_point.append(hotel.price_per_star_point)
        _result_values["average_star_points"] = sum(_star_pints) / len(_star_pints)
        _result_values["average_price_per_star_point"] = sum(_prices_per_start_point) / len(_prices_per_start_point)
        _result_values["res_percent"] = (
                _result_values["good_results"] / (_result_values["good_results"] + _result_values["none_results"]))
        return _result_values

    @staticmethod
    def results_as_str(result_values):
        return f" среднее число звёзд: {round(result_values["average_star_points"] / 2, 2)}, средняя цена за звезду:{round(result_values["average_price_per_star_point"] / 2, 2)} \n получен результат в {round((result_values["good_results"] / (result_values["good_results"] + result_values["none_results"])) * 100, 2)} % случаев"

# -----


# q = Algorithms.algorithm_37(amount_of_steps=100, s=37)
# if q is not None:
#     print(q)
# else:
#     print("отель не найден")


# ----- ----- ----- -----


result = AlgorithmEvaluator.statistics_of_algoritm(s=37, amount_of_iterations=200, amount_of_steps=100)
print(AlgorithmEvaluator.results_as_str(result))

# ----- ----- ----- -----


# x_values = []
# y_values_1 = []
# y_values_2 = []
# y_values_3 = []
# for s in range(10, 90):
#     x_values.append(s)
#     result = AlgorithmEvaluator.statistics_of_algoritm(s=s, amount_of_iterations=200, amount_of_steps=100)
#     average_star_points = result["average_star_points"]
#     y_values_1.append(average_star_points)
#     average_price_per_star_point = result["average_price_per_star_point"]
#     y_values_2.append(average_price_per_star_point)
#     # star_points = result["good_results"]
#     # star_points = result["none_results"]
#     res_percent = result["res_percent"]
#     y_values_3.append(res_percent)
#
# plt.plot(x_values, y_values_1)
# plt.show()
# plt.plot(x_values, y_values_2)
# plt.show()
# plt.plot(x_values, y_values_3)
# plt.show()








