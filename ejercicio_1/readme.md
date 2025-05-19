# Análisis de Cancer1 con MEPX

## Descripción
Implementación del ejemplo Cancer1 usando Multi Expression Programming X (MEPX) para clasificación binaria.

## Archivos importantes
- `mepx_2025_05_19_00_52_13.py`: Código generado por MEPX
- `mepx_errors_*.csv`: Resultados de clasificación
- `mepx_stats_*.csv`: Estadísticas de entrenamiento

## Análisis
El análisis se realizó utilizando Multi Expression Programming X (MEPX) en el conjunto de datos "Cancer1" para un problema de clasificación binaria. El sistema evolucionó durante 26 generaciones, generando un programa de clasificación automática mediante programación genética.  

- Análisis de Errores  
   - Total de muestras evaluadas: 350  
   - Predicciones correctas: 346 (98.86%)  
   - Errores de clasificación: 4 (1.14%)  
   - Falsos positivos: 3 casos (0.86%)  
   - Falsos negativos: 1 caso (0.29%)  

- Evolución del Modelo
  - Evolución del Error: La gráfica muestra cómo el error disminuyó consistentemente durante las generaciones:
    - Error inicial (Gen 1): 2.8571% (validación).
    - Mejor error (Gen 13 y 25): 1.7143% (validación).
    - Estabilización alrededor de la generación 20.

- Estructura del Programa Generado  
El código generado (mepx_2025_05_19_00_52_13.py) implementa un clasificador mediante:
  - Variables Relevantes: Variables más utilizadas:
    - x[0]: Aparece 6 veces.
    - x[1]: Aparece 6 veces.
    - x[5]: Aparece 8 veces.
    - x[6]: Aparece 5 veces.  

  - Variables menos relevantes:
    - x[8]: Solo aparece 2 veces.

- Operaciones Clave
python  
prg[7] = math.sqrt(prg[5])  
prg[11] = math.log(prg[2])  
prg[22] = prg[11] - prg[7]  # Combinación log-sqrt  
prg[30] = prg[29] / prg[24]  # Operación decisiva final  

- Regla de Decisión Final
python  
if prg[30] <= 30.027582:  
    outputs[0] = 0  # No cáncer  
else:  
    outputs[0] = 1  # Cáncer  
- Matriz de Confusión  
Predicción 0	Predicción 1  
Real 0	173	3  
Real 1	1	173  
Precisión global: 98.86%  

Sensibilidad (Recall): 99.43%  

Especificidad: 98.30%  

- Análisis de los Errores: Los 4 casos mal clasificados muestran:
  - Falsos positivos (3 casos):
    - Ocurren cuando prg[30] está ligeramente por encima del umbral (30.027582)
    - Posiblemente corresponden a casos límite en el espacio de características

  - Falso negativo (1 caso):
    - Valor atípico donde las características no siguen el patrón general
    - x[5] tenía un valor extremadamente bajo en este caso

- Conclusiones:
  - El modelo desarrollado con MEPX demostró:
    - Alta precisión: 98.86% de clasificación correcta
    - Buena generalización: Error similar en entrenamiento/validación/test
    - Interpretabilidad: Se puede analizar la lógica de decisión
    - Eficiencia: Tiempo de entrenamiento razonable (~43s/generación)
  - El enfoque de Programación Genética resultó efectivo para este problema de clasificación binaria, generando un modelo competitivo con buenas propiedades de generalización.

