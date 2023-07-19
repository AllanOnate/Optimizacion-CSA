import random

class Problem:
    def __init__(self):
        self.dimension = 5

    def checkConstraint(self, x, y):
        # Verificar restricciones del problema
        x1, x2, x3, x4, x5 = x
        y1, y2, y3, y4, y5 = y
        if (x1 <= 15 and x2 <= 10 and x3 <= 25 and x4 <= 4 and x5 <= 30 and
                1000 * x1 + 2000 * x2 + 1500 * x3 + 2500 * x4 + 300 * x5 <= 50000 and
                150 * x1 + 300 * x2 <= 1800 and
                x1 + x2 <= 20 and
                x3 == x3 - x2 and y2 != y3 and
                x1 >= 0 and x2 >= 0 and x3 >= 0 and x4 >= 0 and x5 >= 0 and
                y1 >= 0 and y2 >= 0 and y3 >= 0 and y4 >= 0 and y5 >= 0 and
                x1 >= y1 and x2 >= y2 and x3 >= y3 and x4 >= y4 and x5 >= y5 and
                15 * y1 >=x1 and 6 * y2 >= x2 and 25*y3 >= x3 and 4*y4 >= x4 and 30*y5 >= x5):
            return True
        return False

    def eval(self, x, y):
        # Evaluar la función objetivo
        x1, x2, x3, x4, x5 = x
        y1, y2, y3, y4, y5 = y
        return (1000 * x1 + 2000 * x2 + 1500 * x3 + 2500 * x4 + 300 * x5 -
                150 * y1 - 300 * y2 - 40 * y3 - 100 * y4 - 10 * y5)

class Chameleon(Problem):
    def __init__(self):
        self.p = Problem()
        self.x = [random.randint(0, 15),
                  random.randint(0, 6),
                  random.randint(0, 25),
                  random.randint(0, 4),
                  random.randint(0, 30)]
        self.y = [random.randint(0, 1),
                  random.randint(0, 1),
                  random.randint(0, 1),
                  random.randint(0, 1),
                  random.randint(0, 1)]

    def isFeasible(self):
        return self.p.checkConstraint(self.x, self.y)

    def isBetterThan(self, g):
        return self.resultado() > g.resultado()

    def resultado(self):
        return self.p.eval(self.x, self.y)

    def busquedaPresa(self, g):
        for i in range(self.p.dimension):
            self.x[i] += random.randint(-1, 1) * (g.x[i] - self.x[i])
            self.y[i] += random.randint(-1, 1) * (g.y[i] - self.y[i])

            # Restringir los valores dentro de los dominios específicos
            if i == 0:
                self.x[i] = max(0, min(self.x[i], 15))
                self.y[i] = max(0, min(self.y[i], 1))
            elif i == 1:
                self.x[i] = max(0, min(self.x[i], 6))
                self.y[i] = max(0, min(self.y[i], 1))
            elif i == 2:
                self.x[i] = max(0, min(self.x[i], 25))
                self.y[i] = max(0, min(self.y[i], 1))
            elif i == 3:
                self.x[i] = max(0, min(self.x[i], 4))
                self.y[i] = max(0, min(self.y[i], 1))
            elif i == 4:
                self.x[i] = max(0, min(self.x[i], 30))
                self.y[i] = max(0, min(self.y[i], 1))

    def __str__(self) -> str:
        return f"resultado: {self.resultado()} x: {self.x} y: {self.y} "

    def copy(self, a):
        self.x = a.x.copy()
        self.y = a.y.copy()

class Swarm:
    def __init__(self):
        self.maxIter = 30
        self.nChameleons = 15
        self.swarm = []
        self.g = Chameleon()

    def solve(self):
        self.initRand()
        self.evolve()

    def initRand(self):
        print("  -->  initRand  <-- ")
        for i in range(self.nChameleons):
            while True:
                a = Chameleon()
                if a.isFeasible():
                    break
            self.swarm.append(a)

        self.g.copy(self.swarm[0])
        for i in range(1, self.nChameleons):
            if self.swarm[i].isBetterThan(self.g):
                self.g.copy(self.swarm[i])

        self.swarmToConsole()
        self.bestToConsole()

    def evolve(self):
        print("  -->  evolve  <-- ")
        t = 1
        while t <= self.maxIter:
            for i in range(self.nChameleons):
                a = Chameleon()
                while True:
                    a.copy(self.swarm[i])
                    a.busquedaPresa(self.g)
                    if a.isFeasible():
                        break
                self.swarm[i].copy(a)

            for i in range(self.nChameleons):
                if self.swarm[i].isBetterThan(self.g):
                    self.g.copy(self.swarm[i])

            self.swarmToConsole()
            self.bestToConsole()
            t += 1

    def swarmToConsole(self):
        print(" -- Swarm --")
        for i in range(self.nChameleons):
            print(f"{self.swarm[i]}")

    def bestToConsole(self):
        print(" -- Best --")
        print(f"{self.g}")

try:
    Swarm().solve()
except Exception as e:
    print(f"{e} \nCaused by {e.__cause__}")
