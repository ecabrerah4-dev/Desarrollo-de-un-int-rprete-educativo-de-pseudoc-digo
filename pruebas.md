# Plan de pruebas

Los casos se deben ejecutar en la aplicación y el resultado obtenido se debe completar con lo observado en el equipo.

| ID | Tipo | Código o preparación | Entrada | Resultado esperado | Estado |
|---|---|---|---|---|---|
| P01 | Aritmética | `Algoritmo p` / `Definir x Como Entero` / `x = 4 + 3 * 2` / `Escribir x` / `FinAlgoritmo` | Ninguna | Muestra `10`; precedencia correcta | Pendiente de ejecución |
| P02 | Aritmética | `Algoritmo p` / `Definir x Como Decimal` / `x = (8 - 2) / 3` / `Escribir x` / `FinAlgoritmo` | Ninguna | Muestra `2.0` | Pendiente de ejecución |
| P03 | Entrada/salida | Definir `nombre` como Texto, `Leer nombre`, `Escribir "Hola", nombre` | `Ana` | Muestra `Hola Ana` | Pendiente de ejecución |
| P04 | Entrada/salida | Definir `n` como Entero, `Leer n`, `Escribir n + 5` | `7` | Muestra `12` | Pendiente de ejecución |
| P05 | Condición verdadera | Definir `edad` como Entero, `edad = 20`, Si `edad >= 18` escribir `Adulto`, SiNo escribir `Menor`, FinSi | Ninguna | Muestra `Adulto` | Pendiente de ejecución |
| P06 | Condición falsa | Definir `n` como Entero, `n = 3`, Si `n > 10` escribir `Mayor`, SiNo escribir `No mayor`, FinSi | Ninguna | Muestra `No mayor` | Pendiente de ejecución |
| P07 | Error léxico | `Algoritmo p` / `Escribir @` / `FinAlgoritmo` | Ninguna | Error léxico, línea 2; no ejecuta | Pendiente de ejecución |
| P08 | Error sintáctico | `Algoritmo p` / `Si 2 > Entonces` / `FinSi` / `FinAlgoritmo` | Ninguna | Error sintáctico con línea y columna | Pendiente de ejecución |
| P09 | Error de ejecución | Definir `x` como Entero, `x = 5 / 0`, `Escribir x` | Ninguna | Informa división entre cero | Pendiente de ejecución |
| P10 | Límite | Definir `x` como Entero, `x = 2.5`, `Escribir x` | Ninguna | Error: se requiere entero | Pendiente de ejecución |

## Registro de resultados reales
Después de probar cada caso, anotar el resultado obtenido y cambiar el estado a **Aprobada** o **Fallida**. No marcar las pruebas como aprobadas sin ejecutarlas.
