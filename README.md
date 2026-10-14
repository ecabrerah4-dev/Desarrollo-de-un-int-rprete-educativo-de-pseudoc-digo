# Intérprete educativo de pseudocódigo

Aplicación web académica para practicar conceptos de Autómatas y Lenguajes Formales.

## Requisitos
- Python 3.10 o superior.
- Navegador moderno.
- Conexión a Internet solo para instalar Flask la primera vez.

## Instalación en Windows
1. Descomprime la carpeta `interprete_pseudocodigo`.
2. Abre PowerShell dentro de la carpeta del proyecto.
3. Ejecuta:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   py -m pip install -r backend\requirements.txt
   py backend\main.py
   ```
   Si PowerShell bloquea la activación, puedes omitir los dos comandos de activación y ejecutar:
   ```powershell
   py -m pip install -r backend\requirements.txt
   py backend\main.py
   ```
4. Abre `http://127.0.0.1:8000` en el navegador.
5. Para detener el servidor, vuelve a la terminal y pulsa `Ctrl+C`.

## Sintaxis de ejemplo
```text
Algoritmo suma
Definir a Como Entero
Definir b Como Entero
Definir total Como Entero
Leer a
Leer b
total = a + b
Escribir "Total:", total
FinAlgoritmo
```
En el cuadro de entradas escribe un valor por línea, por ejemplo `4` y `6`.

## Archivos
- `backend/lexer.py`: expresiones regulares y generación de tokens.
- `backend/parser.py`: analizador sintáctico descendente recursivo y árbol sintáctico.
- `backend/interpreter.py`: ejecución controlada de instrucciones.
- `backend/main.py`: servidor Flask y API local.
- `frontend/`: editor y resultados.
- `gramatica.md`: GIC, terminales/no terminales y ejemplos.
- `pruebas.md`: diez casos mínimos de prueba.

## Alcance y limitaciones
Es un lenguaje educativo deliberadamente pequeño. Las variables deben declararse antes de usarse. Los errores léxicos, sintácticos y de ejecución se informan sin ejecutar el programa cuando el análisis falla. `Leer` toma datos del panel de entradas, uno por línea. El lenguaje no incluye ciclos, funciones, arreglos ni operaciones booleanas compuestas. El programa solo interpreta su propio conjunto limitado de instrucciones; no ejecuta comandos del sistema operativo.
