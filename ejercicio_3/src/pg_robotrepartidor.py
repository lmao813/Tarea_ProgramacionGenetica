import random
import numpy as np
import matplotlib.pyplot as plt
from deap import algorithms, base, creator, gp, tools

# ======================
# CONFIGURACIÓN DEL ENTORNO
# ======================

SALA_SIZE = 10  # Tamaño de la sala cuadrada (10x10)
INGENIEROS = [(2,5), (7,3), (4,8), (8,1)]  # Posiciones fijas de los ingenieros
POS_INICIAL = (0, 0)  # Punto de partida del robot
MAX_PASOS = 50  # Máximo número de movimientos por simulación
GALLETAS_INICIALES = 4  # Número inicial de galletas para repartir

# ======================
# DEFINICIÓN DEL ÁRBOL GP
# ======================

# Crear el conjunto de primitivas
pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(lambda a, b: a if random.random() < 0.5 else b, 2, name="if_random")
pset.addPrimitive(lambda a, b: (a, b), 2, name="progn2")
pset.addPrimitive(lambda a, b, c: (a, b, c), 3, name="progn3")

# Terminales (acciones básicas)
pset.addTerminal("avanzar_norte")
pset.addTerminal("avanzar_sur")
pset.addTerminal("avanzar_este")
pset.addTerminal("avanzar_oeste")
pset.addTerminal("entregar_galleta")
pset.addTerminal("girar_izquierda")
pset.addTerminal("girar_derecha")
pset.addTerminal("no_op")  # No hacer nada

# ======================
# CONFIGURACIÓN DE DEAP
# ======================

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# ======================
# FUNCIÓN DE EVALUACIÓN
# ======================

def evaluar_robot(individual):
    try:
        robot_program = toolbox.compile(expr=individual)
        
        # Estado inicial del robot
        x, y = POS_INICIAL
        direccion = (1, 0)  # Mirando al este (dx, dy)
        galletas = GALLETAS_INICIALES
        puntos = 0
        pasos = 0
        colisiones = 0
        entregas = []
        
        # Ejecutar el programa del robot
        while pasos < MAX_PASOS and galletas > 0:
            accion = robot_program()
            
            # Implementar acciones
            if accion == "avanzar_norte":
                if y + 1 < SALA_SIZE:
                    y += 1
                else:
                    colisiones += 1
            elif accion == "avanzar_sur":
                if y - 1 >= 0:
                    y -= 1
                else:
                    colisiones += 1
            elif accion == "avanzar_este":
                if x + 1 < SALA_SIZE:
                    x += 1
                else:
                    colisiones += 1
            elif accion == "avanzar_oeste":
                if x - 1 >= 0:
                    x -= 1
                else:
                    colisiones += 1
            elif accion == "girar_izquierda":
                direccion = (-direccion[1], direccion[0])  # Rotación 90° izquierda
            elif accion == "girar_derecha":
                direccion = (direccion[1], -direccion[0])  # Rotación 90° derecha
            elif accion == "entregar_galleta":
                if (x, y) in INGENIEROS and (x, y) not in entregas:
                    puntos += 10
                    galletas -= 1
                    entregas.append((x, y))
            
            pasos += 1
        
        # Calcular cobertura de entregas
        cobertura = len(set(entregas)) / len(INGENIEROS)
        
        # Función de aptitud compuesta
        aptitud = (puntos * 10) - (pasos * 0.1) - (colisiones * 5) + (cobertura * 20)
        
        return (aptitud,)
    except Exception as e:
        return (0,)  # En caso de error, aptitud mínima

# ======================
# OPERADORES GENÉTICOS
# ======================

toolbox.register("evaluate", evaluar_robot)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

# ======================
# VISUALIZACIÓN DE RUTAS
# ======================

def visualizar_ruta(individual):
    robot_program = toolbox.compile(expr=individual)
    
    x, y = POS_INICIAL
    direccion = (1, 0)
    galletas = GALLETAS_INICIALES
    pasos = 0
    ruta = [(x, y)]
    entregas = []
    
    while pasos < MAX_PASOS and galletas > 0:
        accion = robot_program()
        
        # Mismo código de movimiento que en evaluar_robot
        if accion == "avanzar_norte" and y + 1 < SALA_SIZE:
            y += 1
        elif accion == "avanzar_sur" and y - 1 >= 0:
            y -= 1
        elif accion == "avanzar_este" and x + 1 < SALA_SIZE:
            x += 1
        elif accion == "avanzar_oeste" and x - 1 >= 0:
            x -= 1
        elif accion == "entregar_galleta" and (x, y) in INGENIEROS and (x, y) not in entregas:
            entregas.append((x, y))
            galletas -= 1
        
        ruta.append((x, y))
        pasos += 1
    
    # Crear visualización
    plt.figure(figsize=(8, 8))
    
    # Dibujar sala
    plt.plot([0, SALA_SIZE, SALA_SIZE, 0, 0], [0, 0, SALA_SIZE, SALA_SIZE, 0], 'k-')
    
    # Dibujar ingenieros
    for ix, iy in INGENIEROS:
        plt.plot(ix, iy, 'ro', markersize=10, label='Ingeniero' if ix==INGENIEROS[0][0] else "")
    
    # Dibujar ruta
    rx, ry = zip(*ruta)
    plt.plot(rx, ry, 'b.-', alpha=0.5, label='Ruta')
    
    # Marcar entregas
    if entregas:
        ex, ey = zip(*entregas)
        plt.plot(ex, ey, 'go', markersize=12, label='Entrega')
    
    plt.title(f"Ruta del Robot (Entregas: {len(entregas)}/{len(INGENIEROS)}")
    plt.legend()
    plt.grid(True)
    plt.xlim(-1, SALA_SIZE+1)
    plt.ylim(-1, SALA_SIZE+1)
    plt.show()

# ======================
# ALGORITMO EVOLUTIVO
# ======================

def main():
    random.seed(42)
    
    # Crear población inicial
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    
    # Configurar estadísticas
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    # Ejecutar algoritmo evolutivo
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, 
                                  ngen=50, stats=stats, halloffame=hof, 
                                  verbose=True)
    
    # Mostrar resultados
    print("\nMejor individuo encontrado:")
    print(hof[0])
    
    print("\nFitness del mejor individuo:", hof[0].fitness.values[0])
    
    # Visualizar mejor ruta
    print("\nVisualizando la mejor ruta encontrada...")
    visualizar_ruta(hof[0])
    
    # Graficar evolución del fitness
    gen = log.select('gen')
    avg_fit = log.select('avg')
    max_fit = log.select('max')
    
    plt.figure()
    plt.plot(gen, avg_fit, 'b-', label="Fitness promedio")
    plt.plot(gen, max_fit, 'r-', label="Fitness máximo")
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Evolución del Fitness")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return pop, log, hof

if __name__ == "__main__":
    main()
