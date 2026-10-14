import re
from dataclasses import dataclass

@dataclass
class Token:
    tipo: str
    valor: str
    linea: int
    columna: int

PATRONES = [
    ("ESPACIO", r"[ \t\r]+"),
    ("COMENTARIO", r"\#[^\n]*"),
    ("CADENA", r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
    ("NUMERO", r"\d+(?:\.\d+)?"),
    ("OPERADOR", r"<=|>=|==|!=|<>|:=|[+\-*/=<>]"),
    ("PARENTESIS", r"[()]"),
    ("COMA", r","),
    ("PUNTO_COMA", r";"),
    ("IDENTIFICADOR", r"[A-Za-z_áéíóúÁÉÍÓÚñÑ][A-Za-z0-9_áéíóúÁÉÍÓÚñÑ]*"),
]
RESERVADAS = {
    "algoritmo", "finalgoritmo", "inicio", "fin", "definir", "como",
    "entero", "decimal", "texto", "leer", "escribir", "si", "entonces",
    "sino", "finsi", "verdadero", "falso", "y", "o", "no"
}
MASTER = re.compile("|".join(f"(?P<{n}>{p})" for n, p in PATRONES), re.IGNORECASE)

class ErrorLexico(Exception):
    def __init__(self, mensaje, linea, columna):
        super().__init__(mensaje)
        self.linea, self.columna = linea, columna

def analizar_lexico(codigo):
    tokens = []
    linea = columna = 1
    pos = 0
    while pos < len(codigo):
        if codigo[pos] == "\n":
            linea += 1
            columna = 1
            pos += 1
            continue
        m = MASTER.match(codigo, pos)
        if not m:
            raise ErrorLexico(f"Símbolo no reconocido: {codigo[pos]!r}", linea, columna)
        tipo = m.lastgroup
        valor = m.group()
        if tipo not in ("ESPACIO", "COMENTARIO"):
            if tipo == "IDENTIFICADOR" and valor.lower() in RESERVADAS:
                tipo = "RESERVADA"
            tokens.append(Token(tipo, valor, linea, columna))
        columna += len(valor)
        pos = m.end()
    tokens.append(Token("EOF", "", linea, columna))
    return tokens
