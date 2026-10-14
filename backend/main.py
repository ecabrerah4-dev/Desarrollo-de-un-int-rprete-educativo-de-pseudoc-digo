from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent.parent
FRONTEND = BASE / "frontend"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lexer import analizar_lexico, ErrorLexico
from parser import analizar_sintaxis, ErrorSintactico
from interpreter import Interprete, ErrorEjecucion

app = Flask(__name__)

@app.get("/")
def inicio():
    return send_from_directory(FRONTEND, "index.html")

@app.get("/<path:archivo>")
def archivos_frontend(archivo):
    if archivo.startswith("api/"):
        return jsonify({"error": "Ruta no encontrada"}), 404
    return send_from_directory(FRONTEND, archivo)

@app.post("/api/analizar")
def analizar():
    datos = request.get_json(silent=True) or {}
    codigo = datos.get("codigo", "")
    entradas = datos.get("entradas", [])
    if not isinstance(codigo, str) or not isinstance(entradas, list):
        return jsonify({"ok": False, "tipo": "solicitud", "mensaje": "Datos enviados con formato incorrecto."}), 400
    try:
        tokens, arbol = analizar_sintaxis(codigo)
        resultado = Interprete(entradas).ejecutar(arbol)
        return jsonify({
            "ok": True,
            "tokens": [{"tipo": t.tipo, "valor": t.valor, "linea": t.linea, "columna": t.columna}
                       for t in tokens if t.tipo != "EOF"],
            "salidas": resultado["salidas"],
            "variables": resultado["variables"],
            "mensaje": "Análisis correcto. Programa ejecutado."
        })
    except ErrorLexico as e:
        return jsonify({"ok": False, "tipo": "léxico", "mensaje": str(e),
                        "linea": e.linea, "columna": e.columna}), 400
    except ErrorSintactico as e:
        return jsonify({"ok": False, "tipo": "sintáctico", "mensaje": str(e),
                        "linea": e.linea, "columna": e.columna}), 400
    except ErrorEjecucion as e:
        return jsonify({"ok": False, "tipo": "ejecución", "mensaje": str(e),
                        "linea": e.linea}), 400
    except Exception:
        app.logger.exception("Error inesperado")
        return jsonify({"ok": False, "tipo": "interno",
                        "mensaje": "Ocurrió un error interno. Revise el código y vuelva a intentarlo."}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
