class ErrorEjecucion(Exception):
    def __init__(self, mensaje, linea=None):
        super().__init__(mensaje)
        self.linea = linea

class Interprete:
    def __init__(self, entradas=None):
        self.variables = {}
        self.tipos = {}
        self.salidas = []
        self.entradas = list(entradas or [])
        self.indice_entrada = 0

    def ejecutar(self, programa):
        for instruccion in programa.datos["instrucciones"]:
            self.ejecutar_instruccion(instruccion)
        return {"salidas": self.salidas, "variables": self.variables}

    def evaluar(self, nodo):
        d = nodo.datos
        if nodo.tipo == "literal":
            return d["valor"]
        if nodo.tipo == "variable":
            nombre = d["nombre"]
            if nombre not in self.variables:
                raise ErrorEjecucion(f"La variable '{nombre}' no está definida.", nodo.linea)
            return self.variables[nombre]
        if nodo.tipo == "unario":
            valor = self.evaluar(d["expresion"])
            if not isinstance(valor, (int, float)) or isinstance(valor, bool):
                raise ErrorEjecucion("El signo negativo solo se puede aplicar a números.", nodo.linea)
            return -valor
        if nodo.tipo == "binaria":
            a, b, op = self.evaluar(d["izquierda"]), self.evaluar(d["derecha"]), d["operador"]
            if op == "+" and (isinstance(a, str) or isinstance(b, str)):
                return str(a) + str(b)
            if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (a, b)):
                raise ErrorEjecucion("Las operaciones aritméticas requieren valores numéricos.", nodo.linea)
            if op == "+": return a + b
            if op == "-": return a - b
            if op == "*": return a * b
            if op == "/":
                if b == 0:
                    raise ErrorEjecucion("División entre cero: no se puede dividir entre 0.", nodo.linea)
                return a / b
        if nodo.tipo == "comparacion":
            a, b, op = self.evaluar(d["izquierda"]), self.evaluar(d["derecha"]), d["operador"]
            try:
                if op in ("=", "=="): return a == b
                if op in ("!=", "<>"): return a != b
                if op == "<": return a < b
                if op == ">": return a > b
                if op == "<=": return a <= b
                if op == ">=": return a >= b
            except TypeError:
                raise ErrorEjecucion("No se pueden comparar esos tipos de valores.", nodo.linea)
        raise ErrorEjecucion("Expresión no soportada.", nodo.linea)

    def ejecutar_instruccion(self, nodo):
        d = nodo.datos
        if nodo.tipo == "definir":
            nombre = d["nombre"]
            if nombre in self.variables:
                raise ErrorEjecucion(f"La variable '{nombre}' ya fue declarada.", nodo.linea)
            self.tipos[nombre] = d["tipo"]
            self.variables[nombre] = None
            return
        if nodo.tipo == "asignacion":
            nombre = d["nombre"]
            if nombre not in self.tipos:
                raise ErrorEjecucion(f"La variable '{nombre}' no está declarada. Use Definir primero.", nodo.linea)
            valor = self.evaluar(d["expresion"])
            tipo = self.tipos[nombre]
            if tipo == "entero":
                if not isinstance(valor, (int, float)) or isinstance(valor, bool) or int(valor) != valor:
                    raise ErrorEjecucion(f"La variable '{nombre}' requiere un número entero.", nodo.linea)
                valor = int(valor)
            elif tipo == "decimal":
                if not isinstance(valor, (int, float)) or isinstance(valor, bool):
                    raise ErrorEjecucion(f"La variable '{nombre}' requiere un número.", nodo.linea)
                valor = float(valor)
            elif tipo == "texto":
                if not isinstance(valor, str):
                    raise ErrorEjecucion(f"La variable '{nombre}' requiere texto entre comillas.", nodo.linea)
            self.variables[nombre] = valor
            return
        if nodo.tipo == "leer":
            nombre = d["nombre"]
            if nombre not in self.tipos:
                raise ErrorEjecucion(f"La variable '{nombre}' no está declarada. Use Definir primero.", nodo.linea)
            if self.indice_entrada >= len(self.entradas):
                raise ErrorEjecucion(f"Falta un dato de entrada para la variable '{nombre}'.", nodo.linea)
            bruto = self.entradas[self.indice_entrada]
            self.indice_entrada += 1
            try:
                if self.tipos[nombre] == "entero":
                    valor = int(bruto)
                elif self.tipos[nombre] == "decimal":
                    valor = float(bruto)
                else:
                    valor = str(bruto)
            except ValueError:
                raise ErrorEjecucion(f"El dato ingresado para '{nombre}' no coincide con el tipo {self.tipos[nombre]}.", nodo.linea)
            self.variables[nombre] = valor
            return
        if nodo.tipo == "escribir":
            valores = [self.evaluar(e) for e in d["expresiones"]]
            self.salidas.append(" ".join(str(v) for v in valores))
            return
        if nodo.tipo == "si":
            condicion = self.evaluar(d["condicion"])
            if not isinstance(condicion, bool):
                raise ErrorEjecucion("La condición de Si debe ser verdadera o falsa.", nodo.linea)
            bloque = d["verdadero"] if condicion else d["falso"]
            for instruccion in bloque:
                self.ejecutar_instruccion(instruccion)
