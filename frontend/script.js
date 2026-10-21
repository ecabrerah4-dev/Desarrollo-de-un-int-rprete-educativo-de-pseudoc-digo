const codigo = document.getElementById("codigo");
const estado = document.getElementById("estado");
const salida = document.getElementById("salida");
const variables = document.getElementById("variables");
const tokens = document.getElementById("tokens");
const ejecutarBtn = document.getElementById("ejecutarBtn");

document.getElementById("ejecutarBtn").addEventListener("click", ejecutar);
document.getElementById("limpiarBtn").addEventListener("click", limpiar);
codigo.addEventListener("keydown", manejarTabulacion);
codigo.addEventListener("keydown", manejarEnter);
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
  estado.className = "estado neutral";
  estado.textContent = "Ejemplo cargado. Pulsa Analizar y ejecutar para ingresar los valores.";
});

function manejarTabulacion(evento) {
  if (evento.key !== "Tab") return;
  evento.preventDefault();

  const inicio = codigo.selectionStart;
  const fin = codigo.selectionEnd;
  if (evento.shiftKey) {
    const inicioLinea = codigo.value.lastIndexOf("\n", inicio - 1) + 1;
    const espacios = codigo.value.slice(inicioLinea).match(/^ {1,4}/)?.[0] ?? "";
    if (!espacios) return;
    codigo.setRangeText("", inicioLinea, inicioLinea + espacios.length, "start");
    const nuevaPosicion = Math.max(inicioLinea, inicio - espacios.length);
    codigo.setSelectionRange(nuevaPosicion, Math.max(nuevaPosicion, fin - espacios.length));
    return;
  }

  codigo.setRangeText("    ", inicio, fin, "end");
}

function manejarEnter(evento) {
  if (evento.key !== "Enter" || evento.shiftKey || evento.ctrlKey || evento.altKey) return;
  evento.preventDefault();

  const posicion = codigo.selectionStart;
  const inicioLinea = codigo.value.lastIndexOf("\n", posicion - 1) + 1;
  const textoLinea = codigo.value.slice(inicioLinea, posicion);
  const sangria = textoLinea.match(/^[ \t]*/)?.[0] ?? "";
  const contenido = textoLinea.trim();

  if (/^(?:SiNo|Sino)\b/i.test(contenido)) {
    const sangriaCondicional = reducirSangria(sangria);
    const textoSinSangria = textoLinea.slice(sangria.length);
    const nuevaLinea = `${sangriaCondicional}${textoSinSangria}\n${sangriaCondicional}    `;
    codigo.setRangeText(nuevaLinea, inicioLinea, codigo.selectionEnd, "end");
    return;
  }

  let siguienteSangria = sangria;

  if (/^FinSi\b|^FinAlgoritmo\b|^Fin\b/i.test(contenido)) {
    siguienteSangria = reducirSangria(sangria);
  } else if (/^Si\b.*\bEntonces\s*;?$/i.test(contenido)) {
    siguienteSangria = sangria + "    ";
  }

  codigo.setRangeText(`\n${siguienteSangria}`, posicion, codigo.selectionEnd, "end");
}

function reducirSangria(sangria) {
  if (sangria.endsWith("\t")) return sangria.slice(0, -1);
  if (sangria.endsWith("    ")) return sangria.slice(0, -4);
  return sangria.replace(/ +$/, "");
}

async function ejecutar() {
  ejecutarBtn.disabled = true;
  estado.className = "estado neutral";
  estado.textContent = "Analizando código...";
  salida.textContent = "";
  variables.textContent = "Procesando...";
  tokens.innerHTML = "";
  const listaEntradas = [];
  try {
    while (true) {
      const respuesta = await fetch("/api/analizar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({codigo: codigo.value, entradas: listaEntradas})
      });
      const data = await respuesta.json();
      const entradaRequerida = obtenerEntradaRequerida(data);
      if (entradaRequerida) {
        const valor = await solicitarEntrada(entradaRequerida);
        if (valor === null) {
          estado.className = "estado neutral";
          estado.textContent = "Ejecución cancelada.";
          salida.textContent = "El programa no se ejecutó hasta el final.";
          variables.textContent = "No disponibles.";
          return;
        }
        listaEntradas.push(valor);
        estado.textContent = `Dato recibido para '${entradaRequerida.nombre}'. Continuando ejecución...`;
        continue;
      }
      if (!data.ok) {
        estado.className = "estado error";
        const mensajeError = `Error ${data.tipo}${data.linea ? ` en línea ${data.linea}` : ""}${data.columna ? `, columna ${data.columna}` : ""}: ${data.mensaje}`;
        estado.textContent = mensajeError;
        salida.textContent = "El programa no se ejecutó correctamente.";
        variables.textContent = "No disponibles.";
        await Swal.fire({
          icon: "error",
          title: "Respuesta incorrecta",
          text: mensajeError,
          confirmButtonText: "Entendido",
          confirmButtonColor: "#8b3de8"
        });
        return;
      }
      await mostrarResultado(data);
      return;
    }
  } catch (error) {
    estado.className = "estado error";
    estado.textContent = "No se pudo conectar con el servidor o mostrar una ventana. Comprueba la conexión e inténtalo de nuevo.";
    salida.textContent = String(error);
    variables.textContent = "No disponibles.";
    if (typeof Swal !== "undefined") {
      await Swal.fire({
        icon: "error",
        title: "No se pudo ejecutar",
        text: estado.textContent,
        confirmButtonText: "Entendido",
        confirmButtonColor: "#8b3de8"
      });
    }
  } finally {
    ejecutarBtn.disabled = false;
  }
}

function obtenerEntradaRequerida(data) {
  if (data.entrada_requerida) return data.entrada_requerida;
  if (data.tipo !== "ejecución") return null;

  const coincidencia = data.mensaje.match(/Falta un dato de entrada para la variable ['"]?([A-Za-z_]\w*)/i);
  if (!coincidencia) return null;

  for (const declaracion of codigo.value.matchAll(/\bDefinir\s+([A-Za-z_]\w*)\s+Como\s+(Entero|Decimal|Texto)\b/gi)) {
    if (declaracion[1].toLowerCase() === coincidencia[1].toLowerCase()) {
      return {nombre: declaracion[1], tipo: declaracion[2].toLowerCase()};
    }
  }
  return null;
}

async function solicitarEntrada(entrada) {
  const {nombre, tipo} = entrada;
  const respuesta = await Swal.fire({
    title: `Ingresa un valor para "${nombre}"`,
    text: `Tipo de dato: ${tipo}`,
    input: "text",
    inputPlaceholder: tipo === "texto" ? "Escribe un texto" : "Escribe un número",
    showCancelButton: true,
    confirmButtonText: "Continuar",
    cancelButtonText: "Cancelar",
    confirmButtonColor: "#8b3de8",
    cancelButtonColor: "#353744",
    inputValidator: valor => {
      const texto = valor.trim();
      if (!texto) return "Ingresa un valor para continuar.";
      if (tipo === "entero" && !/^[+-]?\d+$/.test(texto)) {
        return "Ingresa un número entero válido.";
      }
      if (tipo === "decimal" && !Number.isFinite(Number(texto))) {
        return "Ingresa un número decimal válido.";
      }
    }
  });
  return respuesta.isConfirmed ? respuesta.value.trim() : null;
}

async function mostrarResultado(data) {
  estado.className = "estado correcto";
  estado.textContent = data.mensaje;
  salida.textContent = data.salidas.length ? data.salidas.join("\n") : "(El programa no produjo salida.)";
  await Swal.fire({
    icon: "success",
    title: "¡Respuesta correcta!",
    text: data.salidas.length
      ? `Resultado: ${data.salidas.join("\n")}`
      : "El programa terminó correctamente, pero no produjo salida.",
    confirmButtonText: "Aceptar",
    confirmButtonColor: "#8b3de8"
  });
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
}

function limpiar() {
  estado.className = "estado neutral";
  estado.textContent = "Resultados limpiados.";
  salida.textContent = "Los resultados aparecerán aquí.";
  variables.textContent = "Todavía no hay variables.";
  tokens.innerHTML = '<tr><td colspan="4">Ejecuta un programa para ver sus tokens.</td></tr>';
}
