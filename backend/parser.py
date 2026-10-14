from dataclasses import dataclass
from lexer import analizar_lexico, ErrorLexico

class ErrorSintactico(Exception):
    def __init__(self, mensaje, linea, columna):
        super().__init__(mensaje)
        self.linea, self.columna = linea, columna

@dataclass
class Nodo:
    tipo: str
    datos: dict
    linea: int

class Parser:
    def __init__(self, tokens):
        self.t = tokens
        self.i = 0

    def actual(self):
        return self.t[self.i]

    def avanzar(self):
        tok = self.actual()
        if tok.tipo != "EOF":
            self.i += 1
        return tok

    def es(self, *valores):
        tok = self.actual()
        return tok.valor.lower() in [v.lower() for v in valores]

    def aceptar(self, *valores):
        if self.es(*valores):
            return self.avanzar()
        return None

    def exigir(self, *valores):
        tok = self.actual()
        if not self.es(*valores):
            esperado = " o ".join(valores)
            recibido = tok.valor if tok.valor else "fin del programa"
            raise ErrorSintactico(
                f"Se esperaba {esperado}, pero se encontró {recibido!r}.",
                tok.linea, tok.columna
            )
        return self.avanzar()

    def exigir_tipo(self, tipo, descripcion):
        tok = self.actual()
        if tok.tipo != tipo:
            recibido = tok.valor if tok.valor else "fin del programa"
            raise ErrorSintactico(f"Se esperaba {descripcion}, pero se encontró {recibido!r}.",
                                  tok.linea, tok.columna)
        return self.avanzar()

    def parsear(self):
        inicio = self.exigir("Algoritmo", "Inicio")
        nombre = self.exigir_tipo("IDENTIFICADOR", "nombre del algoritmo")
        self.aceptar(";")
        instrucciones = self.bloque({"FinAlgoritmo", "Fin"})
        self.exigir("FinAlgoritmo", "Fin")
        self.aceptar(";")
        if self.actual().tipo != "EOF":
            tok = self.actual()
            raise ErrorSintactico("Hay contenido después de FinAlgoritmo.", tok.linea, tok.columna)
        return Nodo("programa", {"nombre": nombre.valor, "instrucciones": instrucciones}, inicio.linea)

    def bloque(self, cierres):
        instrucciones = []
        while self.actual().tipo != "EOF" and not self.es(*cierres):
            if self.aceptar(";"):
                continue
            instrucciones.append(self.instruccion())
            self.aceptar(";")
        return instrucciones

    def instruccion(self):
        tok = self.actual()
        if self.aceptar("Definir"):
            nombre = self.exigir_tipo("IDENTIFICADOR", "nombre de variable")
            self.exigir("Como")
            tipo = self.exigir("Entero", "Decimal", "Texto")
            self.aceptar(";")
            return Nodo("definir", {"nombre": nombre.valor, "tipo": tipo.valor.lower()}, tok.linea)
        if self.aceptar("Leer"):
            nombre = self.exigir_tipo("IDENTIFICADOR", "nombre de variable")
            return Nodo("leer", {"nombre": nombre.valor}, tok.linea)
        if self.aceptar("Escribir"):
            exprs = [self.expresion()]
            while self.aceptar(","):
                exprs.append(self.expresion())
            return Nodo("escribir", {"expresiones": exprs}, tok.linea)
        if self.aceptar("Si"):
            condicion = self.condicion()
            self.exigir("Entonces")
            verdadero = self.bloque({"Sino", "FinSi"})
            falso = []
            if self.aceptar("Sino"):
                falso = self.bloque({"FinSi"})
            self.exigir("FinSi")
            return Nodo("si", {"condicion": condicion, "verdadero": verdadero, "falso": falso}, tok.linea)
        if tok.tipo == "IDENTIFICADOR":
            nombre = self.avanzar()
            self.exigir("=", ":=")
            expr = self.expresion()
            return Nodo("asignacion", {"nombre": nombre.valor, "expresion": expr}, tok.linea)
        recibido = tok.valor if tok.valor else "fin del programa"
        raise ErrorSintactico(f"Instrucción no válida: {recibido!r}.", tok.linea, tok.columna)

    def condicion(self):
        izquierda = self.expresion()
        tok = self.actual()
        if tok.valor not in ("=", "==", "!=", "<>", "<", ">", "<=", ">="):
            raise ErrorSintactico("La condición necesita un operador relacional (=, !=, <, >, <= o >=).",
                                  tok.linea, tok.columna)
        op = self.avanzar().valor
        derecha = self.expresion()
        return Nodo("comparacion", {"izquierda": izquierda, "operador": op, "derecha": derecha}, tok.linea)

    def expresion(self):
        nodo = self.termino()
        while self.es("+", "-"):
            op = self.avanzar()
            nodo = Nodo("binaria", {"izquierda": nodo, "operador": op.valor,
                                    "derecha": self.termino()}, op.linea)
        return nodo

    def termino(self):
        nodo = self.unario()
        while self.es("*", "/"):
            op = self.avanzar()
            nodo = Nodo("binaria", {"izquierda": nodo, "operador": op.valor,
                                    "derecha": self.unario()}, op.linea)
        return nodo

    def unario(self):
        if self.aceptar("-"):
            tok = self.t[self.i - 1]
            return Nodo("unario", {"operador": "-", "expresion": self.unario()}, tok.linea)
        if self.aceptar("("):
            expr = self.expresion()
            self.exigir(")")
            return expr
        tok = self.actual()
        if tok.tipo == "NUMERO":
            self.avanzar()
            val = float(tok.valor) if "." in tok.valor else int(tok.valor)
            return Nodo("literal", {"valor": val}, tok.linea)
        if tok.tipo == "CADENA":
            self.avanzar()
            return Nodo("literal", {"valor": tok.valor[1:-1]}, tok.linea)
        if tok.tipo == "RESERVADA" and tok.valor.lower() in ("verdadero", "falso"):
            self.avanzar()
            return Nodo("literal", {"valor": tok.valor.lower() == "verdadero"}, tok.linea)
        if tok.tipo == "IDENTIFICADOR":
            self.avanzar()
            return Nodo("variable", {"nombre": tok.valor}, tok.linea)
        raise ErrorSintactico("Se esperaba un número, texto, variable o expresión entre paréntesis.",
                              tok.linea, tok.columna)

def analizar_sintaxis(codigo):
    tokens = analizar_lexico(codigo)
    arbol = Parser(tokens).parsear()
    return tokens, arbol
