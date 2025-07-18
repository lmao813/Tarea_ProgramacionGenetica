# 📝 Codificador de 7 segmentos usando Programación Genética

## 📌 Descripción general
El objetivo fue encontrar una forma automática de diseñar las funciones lógicas necesarias para encender cada uno de los 7 segmentos de un display digital (de los que muestran los números del 0 al 9).
En lugar de escribir cada función a mano, usamos Programación Genética para que un algoritmo evolucione esas expresiones por sí solo.

## 💡 ¿Qué es un codificador de 7 segmentos?
Es un circuito que toma un número (en binario) y activa ciertos segmentos para formar ese número en una pantalla. Por ejemplo, para mostrar el número 3, se deben encender los segmentos a, b, c, d y g.

## 🔧 Configuración del problema
Para cada uno de los 7 segmentos (a a g), se usó un algoritmo evolutivo para encontrar la expresión lógica correcta.
- Terminales (entradas posibles): A, B, C, D (bits que representan el número en binario, de 0000 a 1001).
- Funciones disponibles (como compuertas lógicas): and, or, not, xor.
- Función de aptitud: Evalúa qué tan bien la función generada reproduce la salida esperada del segmento para los 10 dígitos (0 al 9).

## 🎲 Proceso del algoritmo genético
- Se inicia con funciones aleatorias para cada segmento.
- Se evalúa qué tan bien funcionan.
- Se cruzan y mutan las mejores funciones.
- Se repite el proceso por varias generaciones.
- Al final, se obtiene una función lógica para cada segmento.

## 📈 Resultados
- Evolucionando expresión para segmento 'a'...
  - Mejor expresión para a:
  - or_(xor(and_(not_(xor(and_(B, A), 1)), B), or_(C, and_(B, A))), xor(not_(B), and_(D, or_(C, not_(not_(xor(A, D)))))))

- Evolucionando expresión para segmento 'b'...}
  - Mejor expresión para b:
  - or_(xor(not_(B), and_(and_(xor(or_(C, or_(D, D)), 0), D), xor(C, A))), xor(and_(D, or_(D, D)), not_(or_(and_(A, A), C))))

- Evolucionando expresión para segmento 'c'...
  - Mejor expresión para c:
  - or_(or_(not_(C), and_(and_(1, C), and_(A, D))), or_(xor(D, B), xor(D, A)))

- Evolucionando expresión para segmento 'd'...
  - Mejor expresión para d:
  - or_(C, or_(or_(xor(D, xor(or_(1, A), B)), A), xor(not_(and_(not_(D), and_(0, C))), xor(or_(D, or_(or_(C, B), or_(D, B))), C))))

- Evolucionando expresión para segmento 'e'...
  - Mejor expresión para e:
  - xor(not_(not_(xor(D, 0))), or_(and_(1, not_(not_(xor(or_(not_(not_(C)), xor(and_(C, C), not_(B))), 0)))), xor(A, and_(1, or_(D, and_(A, not_(D)))))))

- Evolucionando expresión para segmento 'f'...
  - Mejor expresión para f:
  - or_(not_(C), and_(or_(and_(not_(B), 0), and_(or_(B, B), not_(D))), or_(xor(and_(C, C), not_(and_(or_(B, C), or_(0, B)))), C)))

- Evolucionando expresión para segmento 'g'...
  - Mejor expresión para g:
  - or_(and_(xor(0, C), and_(C, xor(C, xor(0, or_(A, B))))), xor(or_(or_(0, A), B), and_(C, D)))


* Cada segmento evolucionó de forma independiente. El algoritmo no garantiza la solución más corta, pero sí una que cumple correctamente la función para cada número del 0 al 9.
