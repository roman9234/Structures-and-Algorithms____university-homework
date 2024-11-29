from Predator import Predator
from Herbivore import Herbivore
from Tree import Tree


q = Predator()

if isinstance(q, Tree):
    print("Tree")
if isinstance(q, Herbivore):
    print("Herbivore")
if isinstance(q, Predator):
    print("Predator")
