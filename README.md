# 🧬 Tarea de Programación Genética
**Curso:** Inteligencia Artificial y Mini-Robots  
**Autor:** David Camilo Guzmán Guerrero  
**Fecha de Entrega:** Julio 2025  
**Repositorio:** [Enlace a GitHub](https://github.com/lmao813/Tarea_ProgramacionGenetica) 

## 📚 Contenido

- **Ejercicio 2:** Diseño evolutivo de un codificador de 7 segmentos  
Se implementó un sistema basado en programación genética para encontrar las expresiones booleanas que activan correctamente los segmentos de un display de 7 segmentos.
Para cada segmento (a-g), se evoluciona una expresión lógica que decide cuándo debe estar encendido, usando combinaciones de las entradas binarias A, B, C y D (que representan los números del 0 al 9).

  - Conjunto de terminales: A, B, C, D, constantes 0 y 1
  - Conjunto de funciones: and, or, not, xor
  - Función de aptitud: número de salidas correctas respecto al valor esperado del segmento

  - * Nota: Se usó la librería DEAP para construir árboles sintácticos que representan las expresiones booleanas, y se obtuvo una expresión optimizada para cada segmento.

- **Ejercicio 3:** Robot repartidor de galletas  
Se simuló un entorno 10x10 con ingenieros ubicados aleatoriamente y un robot encargado de repartir galletas. El objetivo es que el robot visite el mayor número posible de ingenieros en 50 pasos, aprendiendo su comportamiento mediante programación genética.

  - Conjunto de terminales: acciones arriba, abajo, izquierda, derecha
  - Conjunto de funciones: if_then_else, operadores aritméticos y condicionales
  - Función de aptitud: número de ingenieros visitados durante el recorrido

  - * Nota: Se visualizó la trayectoria del robot en una matriz con colores distintos para ingenieros, posiciones visitadas y celdas libres. El mejor individuo fue capaz de alcanzar hasta 5 ingenieros.
