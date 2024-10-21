from random import randint, random
from being import Being


def print_beings(_list):
    print(" ".join([str(x) for x in _list]))
    print()


def breed(being1, being2, genes_amount=10, random_mutation_probability=0.2) -> list:
    def random_mutation(_list, probability=0.2) -> list:
        for i in range(len(_list)):
            if random() < probability:
                if _list[i] == 0:
                    _list[i] = 1
                else:
                    _list[i] = 0
        return _list

    _slice_point = randint(1, genes_amount - 2)
    _being1_slice1 = random_mutation(being1.genes[0:_slice_point], probability=random_mutation_probability)
    _being1_slice2 = random_mutation(being1.genes[_slice_point:], probability=random_mutation_probability)
    _being2_slice1 = random_mutation(being2.genes[_slice_point:], probability=random_mutation_probability)
    _being2_slice2 = random_mutation(being2.genes[0:_slice_point], probability=random_mutation_probability)
    _child1 = Being(_being1_slice1 + _being2_slice1)
    _child2 = Being(_being1_slice2 + _being2_slice2)
    return [_child1, _child2]


# Демонстрация
if __name__ == "__main__":
    genes_amount = 10
    being1 = Being([1 for x in range(genes_amount)])
    being2 = Being([0 for x in range(genes_amount)])
    print(being1, being2)

    child1, child2 = breed(being1, being2)
    print(child1, child2)
