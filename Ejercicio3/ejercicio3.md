# 📝 Recorrido del robot repartidor de galletas usando Programación Genética
## 🤖 Descripción del problema
Se desea programar el comportamiento de un robot que entrega galletas a un grupo de ingenieros ubicados aleatoriamente en una sala cuadrada de 10x10. Cada vez que el robot visita la celda de un ingeniero, este gana puntos. El robot parte desde la esquina superior izquierda (posición (0, 0)) y tiene 50 pasos para intentar repartir la mayor cantidad posible de galletas.
El comportamiento del robot es generado automáticamente mediante Programación Genética (PG). Cada individuo de la población representa una estrategia de recorrido, expresada como una combinación de funciones condicionales, comparaciones y movimientos.

## ⚙️ Detalles de la implementación
- Lenguaje: Python
- Librería utilizada: DEAP (Distributed Evolutionary Algorithms in Python)
- Tamaño de la sala: 10x10
- Cantidad de ingenieros: 10
- Pasos máximos del robot: 50
- Población inicial: 100 estrategias
- Generaciones: 50

## 🧠 Conjunto de terminales y funciones:
- Terminales (acciones): move_up(pos), move_down(pos), move_left(pos), move_right(pos)
- Constantes numéricas: 0 a 9
- Comparaciones: lt, gt, eq
- Aritmética: add, sub, safe_mod (versión segura de módulo para evitar división por cero)
- Control de flujo: if_then_else

## 🧪 Función de aptitud
La función de aptitud mide cuántos ingenieros logra visitar el robot durante su recorrido. Cada vez que pisa una celda ocupada por un ingeniero, suma un punto. El objetivo es maximizar esta cantidad.

## 🖥️ Código en Python
https://colab.research.google.com/drive/1q219rMhsAGKjZw4eKIzzYc5Rr4JYS0It#scrollTo=mB7U57yNywDP

## ✅ Resultados
- Durante las 50 generaciones, el algoritmo fue refinando las expresiones de control.
- El robot alcanzó una máxima puntuación de 5 ingenieros visitados en una ejecución.
- En múltiples generaciones, logró consistentemente visitar entre 3 y 4 ingenieros.
- La expresión ganadora fue una combinación anidada de condicionales, que resultó efectiva dentro de las restricciones.
- Visualización: Se utilizó un mapa de calor para mostrar las celdas visitadas por el robot y cuántas de ellas correspondían a ingenieros.

* Este ejercicio muestra cómo la Programación Genética puede generar comportamientos útiles y adaptativos en entornos desconocidos. A través de operadores evolutivos como cruce y mutación, el sistema descubrió una estrategia eficaz para maximizar la cobertura del robot repartidor, sin intervención directa en el diseño del algoritmo de recorrido.
