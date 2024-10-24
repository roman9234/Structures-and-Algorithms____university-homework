from random import randint, random

from being import Being
from methods import breed, print_beings

children_amont = 2
genes_amount = 10
population = 10
iterations_amount = 20

mutation_probability = 0.2

beings = []

for i in range(population):
    beings.append(Being([randint(0, 1) for x in range(genes_amount)]))

i = 0
while beings[0].get_guality() != genes_amount:
    beings = sorted(beings, key=lambda x: x.get_guality(), reverse=True)
    for q in range(0, population, 2):
        being1 = beings[q]
        being2 = beings[q + 1]

        child1, child2 = breed(being1, being2, random_mutation_probability=0.01)
        i += 1
        beings[q] = child1
        beings[q + 1] = child2
    print_beings(beings)

print_beings(beings)
print(f"на выведение идеального Being ушло {i} итераций")
