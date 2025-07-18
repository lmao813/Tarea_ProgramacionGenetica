!pip install deap
import operator
import numpy as np
from deap import base, creator, tools, gp, algorithms
import random
import matplotlib.pyplot as plt
import functools

# -------------------------------
# 1. Tabla de verdad (0-9)
# -------------------------------
# Entradas binarias (A B C D) de 0 a 9
inputs = [list(map(int, f"{i:04b}")) for i in range(10)]

# Salidas por segmento (a-g)
outputs = {
    'a': [1,0,1,1,0,1,1,1,1,1],
    'b': [1,1,1,1,1,0,0,1,1,1],
    'c': [1,1,0,1,1,1,1,1,1,1],
    'd': [1,0,1,1,0,1,1,0,1,1],
    'e': [1,0,1,0,0,0,1,0,1,0],
    'f': [1,0,0,0,1,1,1,0,1,1],
    'g': [0,0,1,1,1,1,1,0,1,1],
}

# -------------------------------
# 2. Definir el entorno GP
# -------------------------------
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 4)  # 4 entradas: A, B, C, D
pset.renameArguments(ARG0='A', ARG1='B', ARG2='C', ARG3='D')

pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.xor, 2)
pset.addPrimitive(operator.not_, 1)

pset.addEphemeralConstant("randBool", lambda: random.randint(0,1))

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# -------------------------------
# 3. Evaluar un segmento (por nombre)
# -------------------------------
def make_fitness_evaluator(segment):
    def eval_func(individual):
        func = toolbox.compile(expr=individual)
        predictions = [int(func(*inp)) for inp in inputs]
        score = sum([1 for p, t in zip(predictions, outputs[segment]) if p == t])
        return score / len(inputs),  # Normalizado entre 0 y 1
    return eval_func

# -------------------------------
# 4. Algoritmo GP por segmento
# -------------------------------
def evolve_segment(segment, ngen=40):
    toolbox.register("evaluate", make_fitness_evaluator(segment))
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr, pset=pset)

    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, ngen, stats=stats, halloffame=hof, verbose=False)

    best_expr = hof[0]
    return best_expr

# -------------------------------
# 5. Ejecutar para todos los segmentos
# -------------------------------
if __name__ == '__main__':
    resultados = {}
    for seg in outputs.keys():
        print(f"Evolucionando expresión para segmento '{seg}'...")
        expr = evolve_segment(seg)
        resultados[seg] = expr
        print(f"  Mejor expresión para {seg}:\n    {expr}\n")
