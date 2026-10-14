const codigo = document.getElementById("codigo");
const entradas = document.getElementById("entradas");
const estado = document.getElementById("estado");
const salida = document.getElementById("salida");
const variables = document.getElementById("variables");
const tokens = document.getElementById("tokens");
const ejecutarBtn = document.getElementById("ejecutarBtn");

document.getElementById("ejecutarBtn").addEventListener("click", ejecutar);
document.getElementById("limpiarBtn").addEventListener("click", limpiar);
document.getElementById("ejemploBtn").addEventListener("click", () => {
  codigo.value = `Algoritmo suma
Definir a Como Decimal
Definir b Como Decimal
Definir resultado Como Decimal
Leer a
Leer b
resultado = a + b * 2
Escribir "Resultado:", resultado
FinAlgoritmo`;
  entradas.value = "a: 5\nb: 3";
  estado.className = "estado neutral";
  estado.textContent = "Ejemplo cargado. Pulsa Analizar y ejecutar.";
});

async function ejecutar() {
  ejecutarBtn.disabled = true;
  estado.className = "estado neutral";
  estado.textContent = "Analizando código...";
  salida.textContent = "";
  variables.textContent = "Procesando...";
  tokens.innerHTML = "";
  const listaEntradas = entradas.value
    .split(/\r?\n/)
    .filter((x, i, a) => x !== "" || a.length > 1)
    .map(x => x.replace(/^\s*[A-Za-z_]\w*\s*:\s*/, "").trim());
  try {
    const respuesta = await fetch("/api/analizar", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({codigo: codigo.value, entradas: listaEntradas})
    });
    const data = await respuesta.json();
    if (!data.ok) {
      estado.className = "estado error";
      estado.textContent = `Error ${data.tipo}${data.linea ? ` en línea ${data.linea}` : ""}${data.columna ? `, columna ${data.columna}` : ""}: ${data.mensaje}`;
      salida.textContent = "El programa no se ejecutó correctamente.";
      variables.textContent = "No disponibles.";
      return;
    }
    estado.className = "estado correcto";
    estado.textContent = data.mensaje;
    salida.textContent = data.salidas.length ? data.salidas.join("\n") : "(El programa no produjo salida.)";
    const nombres = Object.keys(data.variables);
    if (!nombres.length) {
      variables.textContent = "El programa no declaró variables.";
    } else {
      const tabla = document.createElement("table");
      tabla.innerHTML = "<thead><tr><th>Variable</th><th>Valor final</th></tr></thead>";
      const cuerpo = document.createElement("tbody");
      for (const nombre of nombres) {
        const fila = document.createElement("tr");
        const celdaNombre = document.createElement("td");
        const celdaValor = document.createElement("td");
        celdaNombre.textContent = nombre;
        celdaValor.textContent = data.variables[nombre] === null ? "(sin valor)" : String(data.variables[nombre]);
        fila.append(celdaNombre, celdaValor);
        cuerpo.appendChild(fila);
      }
      tabla.appendChild(cuerpo);
      variables.replaceChildren(tabla);
    }
    for (const token of data.tokens) {
      const fila = document.createElement("tr");
      [token.tipo, token.valor || "(vacío)", token.linea, token.columna].forEach(valor => {
        const celda = document.createElement("td");
        celda.textContent = valor;
        fila.appendChild(celda);
      });
      tokens.appendChild(fila);
    }
    if (!data.tokens.length) tokens.innerHTML = '<tr><td colspan="4">No se encontraron tokens.</td></tr>';
  } catch (error) {
    estado.className = "estado error";
    estado.textContent = "No se pudo conectar con el servidor. Comprueba que main.py esté ejecutándose.";
    salida.textContent = String(error);
    variables.textContent = "No disponibles.";
  } finally {
    ejecutarBtn.disabled = false;
  }
}

function limpiar() {
  estado.className = "estado neutral";
  estado.textContent = "Resultados limpiados.";
  salida.textContent = "Los resultados aparecerán aquí.";
  variables.textContent = "Todavía no hay variables.";
  tokens.innerHTML = '<tr><td colspan="4">Ejecuta un programa para ver sus tokens.</td></tr>';
}
