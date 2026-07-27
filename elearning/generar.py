#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AuditCaat's — Generador de modulos del programa MRC-2026

El contenido de cada modulo vive en contenido/mNN.py como estructura de
datos. Este script lo convierte en el HTML final, que solo declara
contenido: toda la mecanica esta en assets/ac_engine.js y ac_modulo.js.

Uso:
    python3 generar.py            genera todos los modulos declarados
    python3 generar.py M02 M06    genera solo los indicados
"""

import html
import importlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SALIDA = RAIZ / "modulos"

MODULOS = ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08"]


def esc(t):
    return html.escape(str(t), quote=False)


def render_bloque(b):
    """Cada bloque es una tupla (tipo, contenido)."""
    tipo = b[0]

    if tipo == "p":
        return f"<p>{esc(b[1])}</p>"

    if tipo in ("nota", "riesgo", "umbral"):
        titulo, cuerpo = b[1], b[2]
        return (f'<div class="ac-{tipo}"><strong>{esc(titulo)}</strong>{esc(cuerpo)}</div>')

    if tipo == "cita":
        texto, fuente = b[1], b[2]
        return (f'<blockquote class="ac-cita">{esc(texto)}'
                f"<cite>{esc(fuente)}</cite></blockquote>")

    if tipo == "lista":
        items = "".join(f"<li>{esc(i)}</li>" for i in b[1])
        return f"<ul>{items}</ul>"

    if tipo == "pasos":
        items = "".join(f"<li>{esc(i)}</li>" for i in b[1])
        return f"<ol>{items}</ol>"

    if tipo == "codigo":
        titulo, cuerpo = b[1], b[2]
        return ('<div class="ac-codigo"><div class="ac-codigo-encab">'
                f'<span>Python</span><em>{esc(titulo)}</em></div>'
                f"<pre><code>{esc(cuerpo)}</code></pre></div>")

    if tipo == "tabla":
        filas = b[1]
        cab = "".join(f"<th>{esc(c)}</th>" for c in filas[0])
        cuerpo = ""
        for f in filas[1:]:
            celdas = ""
            for c in f:
                clase = ' class="num"' if isinstance(c, (int, float)) or (
                    isinstance(c, str) and c.replace(",", "").replace(".", "")
                    .replace("%", "").replace("-", "").replace(" ", "").isdigit()) else ""
                celdas += f"<td{clase}>{esc(c)}</td>"
            cuerpo += f"<tr>{celdas}</tr>"
        return (f'<table class="ac-tabla"><thead><tr>{cab}</tr></thead>'
                f"<tbody>{cuerpo}</tbody></table>")

    raise ValueError(f"Tipo de bloque no reconocido: {tipo}")


def render_cedula(c):
    bloques = "\n      ".join(render_bloque(b) for b in c["bloques"])
    return f"""
  <section class="ac-cedula" data-cedula="{c['ref']}">
    <div class="ac-cedula-encab">
      <span class="ref">{c['ref']}</span>
      <h3>{esc(c['titulo'])}</h3>
    </div>
    <div class="ac-cedula-cuerpo">
      {bloques}
    </div>
    <div class="ac-cedula-pie">
      <button class="ac-btn ac-btn-secundario" data-marcar="{c['ref']}">Marcar cédula revisada</button>
      <span class="ac-marca-aud" data-marca-de="{c['ref']}"></span>
    </div>
  </section>"""


PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} · AuditCaat's</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;500;600;700&family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/ac_marca.css">
<link rel="stylesheet" href="../assets/ac_estilo.css">
</head>
<body>

<header class="ac-cabecera">
  <div class="ac-envoltura ac-cabecera-fila">
    <div class="ac-logo" id="logo"><span>AC</span></div>
    <div class="ac-cabecera-txt">
      <strong id="cab-titulo">{titulo}</strong>
      <small id="cab-ref">Referencia</small>
    </div>
    <div class="ac-cabecera-fin"><a href="../index.html" style="color:#fff">Volver al índice</a></div>
  </div>
</header>

<main class="ac-angosto" style="padding-top:var(--e-7);padding-bottom:var(--e-8)">

  <div class="ac-avance">
    <div class="ac-avance-riel"><div class="ac-avance-lleno" id="ac-avance-lleno"></div></div>
    <small id="ac-avance-txt"></small>
  </div>

  <div class="ac-nota" style="margin-bottom:var(--e-6)">
    <strong>Qué se lleva de este módulo</strong>{proposito}
  </div>
{cedulas}

  <section class="ac-cedula" id="bloque-eval">
    <div class="ac-cedula-encab">
      <span class="ref">EVAL</span>
      <h3>Evaluación del módulo</h3>
    </div>
    <div class="ac-cedula-cuerpo">
      <p id="eval-aviso">Completa las cédulas para habilitar la evaluación.</p>
      <div id="quiz"></div>
      <div style="margin-top:var(--e-5);display:flex;gap:var(--e-3);align-items:center;flex-wrap:wrap">
        <button class="ac-btn ac-btn-primario" id="btn-calificar" disabled>Calificar</button>
        <span id="resultado" style="font-family:var(--ac-dato);font-size:var(--t-sm)"></span>
      </div>
      <div id="acciones-cert" style="margin-top:var(--e-4);display:none">
        <a class="ac-btn ac-btn-primario" id="btn-cert">Ver certificado del módulo</a>
        <a class="ac-btn ac-btn-secundario" id="btn-indice" href="../index.html">Volver al índice</a>
      </div>
    </div>
  </section>

</main>

<script src="../assets/ac_programa.js"></script>
<script src="../assets/ac_engine.js"></script>
<script src="../assets/ac_modulo.js"></script>
<script>
const BANCO = {banco};
ACModulo.iniciar("{mid}", BANCO);
</script>
</body>
</html>
"""


def generar(mid):
    mod = importlib.import_module(f"contenido.{mid.lower()}")
    datos = mod.MODULO

    # El laboratorio en Python se declara aparte y se anexa como ultima cedula.
    from contenido.labs import LABS
    if mid in LABS and not any(c["ref"] == LABS[mid]["ref"] for c in datos["cedulas"]):
        datos["cedulas"] = datos["cedulas"] + [LABS[mid]]

    for c in datos["cedulas"]:
        if not c["ref"].startswith(datos["ref"] + "-"):
            raise ValueError(f"{mid}: la cédula {c['ref']} no usa el prefijo {datos['ref']}-")

    banco = json.dumps(datos["banco"], ensure_ascii=False, indent=2)
    doc = PLANTILLA.format(
        titulo=esc(datos["titulo"]),
        proposito=esc(datos["proposito"]),
        cedulas="\n".join(render_cedula(c) for c in datos["cedulas"]),
        banco=banco,
        mid=mid,
    )

    destino = SALIDA / f"{mid.lower()}.html"
    destino.write_text(doc, encoding="utf-8")

    puntaje = sum(p.get("puntaje", 10) for p in datos["banco"])
    correctas = [sum(1 for o in p["opciones"] if o.get("ok")) for p in datos["banco"]]
    if set(correctas) != {1}:
        raise ValueError(f"{mid}: hay preguntas sin exactamente una opción correcta")

    print(f"  {mid}  {destino.name:<12} {len(datos['cedulas'])} cédulas  "
          f"{len(datos['banco'])} preguntas  {puntaje} puntos  "
          f"{destino.stat().st_size // 1024} KB")


if __name__ == "__main__":
    sys.path.insert(0, str(RAIZ))
    pedidos = [a.upper() for a in sys.argv[1:]] or MODULOS
    print("Generando módulos:")
    for m in pedidos:
        generar(m)
    print("Listo.")
