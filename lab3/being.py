class Being:

    def __init__(self, genes):
        self.genes = genes

    def get_guality(self):
        return sum(self.genes)

    def __str__(self):
        return "".join(str(x) for x in self.genes)
