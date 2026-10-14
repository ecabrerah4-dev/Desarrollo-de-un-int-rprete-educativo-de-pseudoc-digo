# Gramática del lenguaje educativo

## 1. Convenciones
- El programa comienza con `Algoritmo nombre` y termina con `FinAlgoritmo`.
- Las palabras reservadas no distinguen mayúsculas de minúsculas.
- Cada variable debe declararse antes de asignarle o leer su valor.
- Los tipos son `Entero`, `Decimal` y `Texto`.
- Se permiten comentarios de línea que comiencen con `#`.
- `Escribir` acepta una o varias expresiones separadas por comas.
- `Leer` lee un valor por instrucción; los datos se proporcionan en la interfaz, uno por línea.
- Para asignar se usa `=` o `:=`.
- Las cadenas se escriben entre comillas simples o dobles.
- Operadores relacionales: `=`, `==`, `!=`, `<>`, `<`, `>`, `<=`, `>=`.
- Operadores aritméticos: `+`, `-`, `*`, `/`. Multiplicación y división tienen precedencia sobre suma y resta.

## 2. Símbolos
**No terminales:** Programa, Bloque, Instruccion, Declaracion, Asignacion, Lectura, Escritura, Condicional, Condicion, Expresion, Termino, Unario, Primario, ListaExpresiones, Tipo, Identificador, Numero, Cadena, Relacional.

**Terminales:** `Algoritmo`, `FinAlgoritmo`, `Definir`, `Como`, `Entero`, `Decimal`, `Texto`, `Leer`, `Escribir`, `Si`, `Entonces`, `SiNo`, `FinSi`, `=`, `:=`, `+`, `-`, `*`, `/`, `(`, `)`, `,`, `;`, identificadores, números, cadenas y fin de entrada.

**Símbolo inicial:** Programa.

## 3. Producciones GIC (EBNF)
```ebnf
Programa          ::= ("Algoritmo" | "Inicio") Identificador [";"]
                      Bloque ("FinAlgoritmo" | "Fin") [";"] ;
Bloque            ::= { Instruccion [";"] } ;
Instruccion       ::= Declaracion | Asignacion | Lectura | Escritura | Condicional ;
Declaracion       ::= "Definir" Identificador "Como" Tipo ;
Tipo              ::= "Entero" | "Decimal" | "Texto" ;
Asignacion        ::= Identificador ("=" | ":=") Expresion ;
Lectura           ::= "Leer" Identificador ;
Escritura         ::= "Escribir" ListaExpresiones ;
ListaExpresiones  ::= Expresion { "," Expresion } ;
Condicional       ::= "Si" Condicion "Entonces" Bloque
                      ["SiNo" Bloque] "FinSi" ;
Condicion         ::= Expresion Relacional Expresion ;
Relacional        ::= "=" | "==" | "!=" | "<>" | "<" | ">" | "<=" | ">=" ;
Expresion         ::= Termino { ("+" | "-") Termino } ;
Termino           ::= Unario { ("*" | "/") Unario } ;
Unario            ::= "-" Unario | Primario ;
Primario          ::= Numero | Cadena | Identificador | "Verdadero" | "Falso"
                      | "(" Expresion ")" ;
Identificador     ::= letra { letra | dígito | "_" } ;
Numero            ::= dígito { dígito } ["." dígito { dígito }] ;
Cadena            ::= '"' { carácter } '"' | "'" { carácter } "'" ;
```
La implementación usa un analizador descendente recursivo para las producciones y bucles de repetición para los operadores de cada nivel de precedencia.

## 4. Ejemplos válidos
1. `Algoritmo hola / Escribir "Hola" / FinAlgoritmo` (cada `/` aquí representa un salto de línea, no el operador del programa).
2. Declarar un entero, asignarle `8` y escribirlo.
3. Declarar dos decimales, leerlos y escribir `a + b`.
4. Si `nota >= 60 Entonces` escribir `"Aprobado"`; `SiNo` escribir `"Reprobado"`; `FinSi`.
5. Calcular `resultado = (2 + 3) * 4`.

## 5. Ejemplos inválidos
1. `Algoritmo / Escribir "Hola" / FinAlgoritmo`: falta el identificador del algoritmo.
2. `Algoritmo prueba / Definir Como Entero / FinAlgoritmo`: falta el nombre de variable.
3. `Algoritmo prueba / Si x > Entonces / FinSi / FinAlgoritmo`: falta el operando derecho.
4. `Algoritmo prueba / x = 3 / FinAlgoritmo`: puede pasar sintaxis, pero falla en ejecución porque `x` no fue declarada.
5. `Algoritmo prueba / Escribir @ / FinAlgoritmo`: error léxico por símbolo no reconocido.

En los ejemplos anteriores, `/` se usa solo como separador visual de líneas en este documento.
