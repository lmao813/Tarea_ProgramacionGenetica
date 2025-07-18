!pip install deap
import numpy as np
import random
import operator
import matplotlib.pyplot as plt
from deap import base, creator, gp, tools, algorithms

# --- Tipos personalizados ---
class Action: pass
class Number(int): pass
class Boolean: pass  # No hereda de bool para evitar errores

# --- Configuración de la sala ---
GRID_SIZE = 10
NUM_ENGINEERS = 10
MAX_STEPS = 50

def generar_ingenieros():
    posiciones = set()
    while len(posiciones) < NUM_ENGINEERS:
        posiciones.add((random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)))
    return list(posiciones)

# --- Acciones de movimiento ---
def move_up(pos):
    return (max(pos[0]-1, 0), pos[1])

def move_down(pos):
    return (min(pos[0]+1, GRID_SIZE-1), pos[1])

def move_left(pos):
    return (pos[0], max(pos[1]-1, 0))

def move_right(pos):
    return (pos[0], min(pos[1]+1, GRID_SIZE-1))

def if_then_else(condition, out1, out2):
    return out1 if condition else out2

# --- Visualización de ruta ---
def visualizar_ruta(trayectoria, ingenieros):
    grid = np.zeros((GRID_SIZE, GRID_SIZE))

    for x, y in ingenieros:
        grid[x, y] = 2  # Ingenieros (valor 2)

    for x, y in trayectoria:
        if grid[x, y] != 2:
            grid[x, y] = 1  # Ruta (valor 1)

    plt.figure(figsize=(6, 6))
    cmap = plt.cm.get_cmap("viridis", 3)
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)
    plt.colorbar(ticks=[0, 1, 2], label='Leyenda')
    plt.title("Ruta del robot (0: vacío, 1: ruta, 2: ingeniero)")
    plt.grid(False)
    plt.xticks(range(GRID_SIZE))
    plt.yticks(range(GRID_SIZE))
    plt.gca().invert_yaxis()
    plt.show()

# --- DEAP Setup ---
pset = gp.PrimitiveSetTyped("MAIN", [], Action)

# Primitivos condicionales y operadores
pset.addPrimitive(if_then_else, [Boolean, Action, Action], Action)
pset.addPrimitive(operator.gt, [Number, Number], Boolean)
pset.addPrimitive(operator.lt, [Number, Number], Boolean)
pset.addPrimitive(operator.eq, [Number, Number], Boolean)
pset.addPrimitive(operator.add, [Number, Number], Number)
pset.addPrimitive(operator.sub, [Number, Number], Number)
pset.addPrimitive(lambda a, b: a if b != 0 else 0, [Number, Number], Number, name="safe_mod")

# Terminales de movimiento (envueltos en lambdas únicos)
pset.addTerminal(lambda: move_up, Action, name="move_up")
pset.addTerminal(lambda: move_down, Action, name="move_down")
pset.addTerminal(lambda: move_left, Action, name="move_left")
pset.addTerminal(lambda: move_right, Action, name="move_right")

# Terminales numéricos
for i in range(1, 11):
    pset.addTerminal(Number(i), Number)

# Terminales booleanos necesarios
pset.addTerminal(True, Boolean, name="TRUE")
pset.addTerminal(False, Boolean, name="FALSE")


# --- Estructuras genéticas ---
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# --- Evaluación de aptitud con visualización ---
def eval_robot(ind):
    func = toolbox.compile(expr=ind)
    robot_pos = (0, 0)
    visited = set()
    trayectoria = [robot_pos]
    engineers = generar_ingenieros()

    for _ in range(MAX_STEPS):
        try:
            move = func()
            robot_pos = move(robot_pos)
        except:
            return 0,

        trayectoria.append(robot_pos)
        if robot_pos in engineers:
            visited.add(robot_pos)

    if len(visited) >= 4:
        print(f"\nVisitó {len(visited)} ingenieros")
        visualizar_ruta(trayectoria, engineers)

    return len(visited),

toolbox.register("evaluate", eval_robot)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr, pset=pset)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=7))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=7))

# --- Ejecución principal ---
def main():
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.7, 0.3, 50, stats=stats, halloffame=hof, verbose=True)

    print("\nMejor solución encontrada:")
    print(hof[0])

if __name__ == "__main__":
    main()
