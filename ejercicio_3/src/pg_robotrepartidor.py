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
# DEFINICIÓN DE ACCIONES BÁSICAS (TERMINALES)
# ======================

def avanzar_norte(): return "avanzar_norte"
def avanzar_sur(): return "avanzar_sur"
def avanzar_este(): return "avanzar_este"
def avanzar_oeste(): return "avanzar_oeste"
def entregar_galleta(): return "entregar_galleta"
def girar_izquierda(): return "girar_izquierda"
def girar_derecha(): return "girar_derecha"
def no_op(): return "no_op"

# ======================
# DEFINICIÓN DE PRIMITIVAS
# ======================

def progn2(a, b):
    """Ejecuta dos acciones secuencialmente"""
    def _exec():
        a()
        return b()
    return _exec

def progn3(a, b, c):
    """Ejecuta tres acciones secuencialmente"""
    def _exec():
        a()
        b()
        return c()
    return _exec

def if_tiene_galletas(then_action, else_action):
    """Ejecuta condicionalmente basado en galletas disponibles"""
    def _exec():
        return then_action() if GALLETAS_INICIALES > 0 else else_action()
    return _exec

# ======================
# CONFIGURACIÓN DE DEAP
# ======================

# Creación de tipos
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

# Configuración del toolbox
toolbox = base.Toolbox()
pset = gp.PrimitiveSet("MAIN", 0)

# Agregar primitivas
pset.addPrimitive(progn2, 2, name="progn2")
pset.addPrimitive(progn3, 3, name="progn3")
pset.addPrimitive(if_tiene_galletas, 2, name="if_tiene_galletas")

# Agregar terminales (acciones)
pset.addTerminal(avanzar_norte, name="avanzar_norte")
pset.addTerminal(avanzar_sur, name="avanzar_sur")
pset.addTerminal(avanzar_este, name="avanzar_este")
pset.addTerminal(avanzar_oeste, name="avanzar_oeste")
pset.addTerminal(entregar_galleta, name="entregar_galleta")
pset.addTerminal(girar_izquierda, name="girar_izquierda")
pset.addTerminal(girar_derecha, name="girar_derecha")
pset.addTerminal(no_op, name="no_op")

# Configurar toolbox
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
        
        if not callable(robot_program):
            return (0.1,)  # Valor mínimo para permitir evolución
        
        # Estado inicial
        x, y = POS_INICIAL
        direccion = (1, 0)  # Mirando al este
        galletas = GALLETAS_INICIALES
        puntos = 0
        pasos = 0
        colisiones = 0
        entregas = []
        
        # Ejecutar el programa
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
                direccion = (-direccion[1], direccion[0])
            elif accion == "girar_derecha":
                direccion = (direccion[1], -direccion[0])
            elif accion == "entregar_galleta":
                if (x, y) in INGENIEROS and (x, y) not in entregas and galletas > 0:
                    puntos += 10
                    galletas -= 1
                    entregas.append((x, y))
            
            pasos += 1
        
        # Calcular cobertura
        cobertura = len(set(entregas)) / len(INGENIEROS)
        
        # Función de aptitud compuesta
        aptitud = (puntos * 10) - (pasos * 0.1) - (colisiones * 5) + (cobertura * 20)
        
        return (max(aptitud, 0.1),)  # Nunca devolver menos de 0.1
    
    except Exception as e:
        print(f"Error en evaluación: {str(e)}")
        return (0.1,)

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
    try:
        robot_program = toolbox.compile(expr=individual)
        
        if not callable(robot_program):
            print("Error: Programa no ejecutable")
            return
        
        # Estado inicial
        x, y = POS_INICIAL
        direccion = (1, 0)
        galletas = GALLETAS_INICIALES
        pasos = 0
        ruta = [(x, y)]
        entregas = []
        
        # Ejecutar programa
        while pasos < MAX_PASOS and galletas > 0:
            accion = robot_program()
            
            # Implementar acciones
            if accion == "avanzar_norte":
                y = min(y + 1, SALA_SIZE - 1)
            elif accion == "avanzar_sur":
                y = max(y - 1, 0)
            elif accion == "avanzar_este":
                x = min(x + 1, SALA_SIZE - 1)
            elif accion == "avanzar_oeste":
                x = max(x - 1, 0)
            elif accion == "entregar_galleta":
                if (x, y) in INGENIEROS and (x, y) not in entregas and galletas > 0:
                    entregas.append((x, y))
                    galletas -= 1
            
            ruta.append((x, y))
            pasos += 1
        
        # Crear visualización
        plt.figure(figsize=(10, 10))
        
        # Dibujar sala
        plt.plot([0, SALA_SIZE, SALA_SIZE, 0, 0], [0, 0, SALA_SIZE, SALA_SIZE, 0], 'k-', linewidth=2)
        
        # Dibujar ingenieros
        for i, (ix, iy) in enumerate(INGENIEROS):
            color = 'green' if (ix, iy) in entregas else 'red'
            plt.plot(ix, iy, 'o', markersize=15, color=color, label=f'Ingeniero {i+1}')
        
        # Dibujar ruta
        rx, ry = zip(*ruta)
        plt.plot(rx, ry, 'b.-', alpha=0.5, linewidth=1, label='Ruta')
        
        # Marcar inicio/fin
        plt.plot(POS_INICIAL[0], POS_INICIAL[1], 'gs', markersize=10, label='Inicio')
        plt.plot(x, y, 'bs', markersize=10, label='Final')
        
        # Configuración del gráfico
        plt.title(f"Ruta del Robot\nEntregas: {len(entregas)}/{len(INGENIEROS)} | Galletas restantes: {galletas}")
        plt.legend()
        plt.grid(True)
        plt.xlim(-1, SALA_SIZE + 1)
        plt.ylim(-1, SALA_SIZE + 1)
        plt.xticks(range(SALA_SIZE + 1))
        plt.yticks(range(SALA_SIZE + 1))
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
    
    except Exception as e:
        print(f"Error en visualización: {str(e)}")

# ======================
# ALGORITMO EVOLUTIVO
# ======================

def main():
    random.seed(42)
    
    # Crear población inicial
    pop = toolbox.population(n=200)  # Población más grande
    
    # Configurar estadísticas
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    # Hall of Fame para los mejores individuos
    hof = tools.HallOfFame(5)
    
    # Ejecutar algoritmo evolutivo
    pop, log = algorithms.eaSimple(
        pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=100,  # Más generaciones
        stats=stats, halloffame=hof, verbose=True
    )
    
    # Mostrar resultados
    print("\n=== Mejores individuos encontrados ===")
    for i, ind in enumerate(hof):
        print(f"\nIndividuo #{i+1} (Fitness: {ind.fitness.values[0]:.2f}):")
        print(ind)
    
    # Visualizar rutas de los mejores individuos
    for i, ind in enumerate(hof):
        print(f"\nVisualizando ruta del individuo #{i+1}...")
        visualizar_ruta(ind)
    
    # Graficar evolución del fitness
    gen = log.select('gen')
    avg_fit = log.select('avg')
    max_fit = log.select('max')
    
    plt.figure(figsize=(10, 6))
    plt.plot(gen, avg_fit, 'b-', label="Fitness promedio")
    plt.plot(gen, max_fit, 'r-', label="Fitness máximo")
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Evolución del Fitness durante las Generaciones")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return pop, log, hof

if __name__ == "__main__":
    main()
