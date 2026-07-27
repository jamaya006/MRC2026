#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AuditCaat's — Empaquetador del programa MRC-2026

Produce dos formatos a partir de la misma fuente:

  dist/                        Sitio para publicar. Cada pagina lleva su CSS y
                               su JS incrustados, asi que tambien funciona
                               abriendo el archivo directamente, sin servidor.

  dist/AuditCaats_MRC2026.html Un solo archivo con el programa completo y
                               navegacion interna. Es el que se manda por
                               correo o se abre en el telefono.

Uso:
    python3 empaquetar.py
"""

import re
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DIST = RAIZ / "dist"

ASSET = re.compile(r'<link rel="stylesheet" href="([^"]+)">|<script src="([^"]+)"></script>')


def leer(rel):
    return (RAIZ / rel).read_text(encoding="utf-8")


def incrustar(html, base):
    """Reemplaza cada <link> y <script src> por su contenido."""
    def sub(m):
        css, js = m.group(1), m.group(2)
        ruta = (base / (css or js)).resolve()
        cuerpo = ruta.read_text(encoding="utf-8")
        if css:
            return "<style>\n" + cuerpo + "\n</style>"
        return "<script>\n" + cuerpo + "\n</script>"
    return ASSET.sub(sub, html)


# ------------------------------------------------------------------
# 1. Sitio con paginas autocontenidas
# ------------------------------------------------------------------
def construir_sitio():
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "modulos").mkdir(parents=True)

    paginas = [Path("index.html"), Path("certificado.html")]
    paginas += sorted(Path(p.relative_to(RAIZ)) for p in (RAIZ / "modulos").glob("m0*.html"))

    for rel in paginas:
        html = incrustar(leer(rel), (RAIZ / rel).parent)
        (DIST / rel).write_text(html, encoding="utf-8")
        print(f"  dist/{rel}  {len(html)//1024} KB")

    shutil.copytree(RAIZ / "backend", DIST / "backend")

    # GitHub Pages ignora las carpetas que empiezan con guion bajo sin este archivo
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / "LEEME_DESPLIEGUE.md").write_text(DESPLIEGUE, encoding="utf-8")


# ------------------------------------------------------------------
# 2. Archivo unico navegable
# ------------------------------------------------------------------
def extraer_main(html):
    i = html.index("<main")
    i = html.index(">", i) + 1
    return html[i:html.index("</main>")]


def extraer_banco(html):
    i = html.index("const BANCO = ")
    j = html.index("\nACModulo.iniciar")
    return html[i + len("const BANCO = "):j].rstrip().rstrip(";")


def cuerpo_del_script(html):
    """Devuelve el interior del IIFE del script inline de una pagina."""
    bloque = re.findall(r"<script>\s*\(function \(\) \{(.*?)\}\)\(\);\s*</script>", html, re.S)
    return bloque[0]


def construir_unico():
    modulos = sorted((RAIZ / "modulos").glob("m0*.html"))
    piezas_html, piezas_banco = [], []
    for f in modulos:
        mid = f.stem.upper()
        h = f.read_text(encoding="utf-8")
        piezas_html.append(f'  "{mid}": {escapar_js(extraer_main(h))}')
        piezas_banco.append(f'  "{mid}": {extraer_banco(h)}')

    index = leer("index.html")
    portal_main = extraer_main(index)
    portal_js = cuerpo_del_script(index)

    css = leer("assets/ac_marca.css") + "\n" + leer("assets/ac_estilo.css")
    js_base = "\n".join(leer(f"assets/{n}") for n in
                        ("ac_programa.js", "ac_engine.js", "ac_modulo.js", "ac_cert.js"))

    doc = PLANTILLA_UNICO.format(
        css=css,
        js_base=js_base,
        modulos_html="{\n" + ",\n".join(piezas_html) + "\n}",
        bancos="{\n" + ",\n".join(piezas_banco) + "\n}",
        portal_main=escapar_js(portal_main),
        portal_js=portal_js,
    )
    destino = DIST / "AuditCaats_MRC2026.html"
    destino.write_text(doc, encoding="utf-8")
    print(f"  dist/{destino.name}  {len(doc)//1024} KB")


def escapar_js(texto):
    """Convierte HTML en un literal de plantilla seguro."""
    t = texto.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    return "`" + t + "`"


DESPLIEGUE = """# Publicación del programa MRC-2026

Esta carpeta es el sitio listo para subir. No requiere servidor de
aplicación, base de datos ni proceso de compilación: son archivos estáticos.

## Qué subir

Todo el contenido de esta carpeta a la raíz del sitio o a un subdirectorio,
respetando la estructura:

    index.html
    certificado.html
    modulos/m01.html … m08.html
    .nojekyll
    AuditCaats_MRC2026.html   (opcional: copia del programa en un solo archivo)

La carpeta `backend/` NO se sube al sitio web: su contenido va al proyecto de
Google Apps Script.

## Opciones de alojamiento

Cualquiera sirve. En orden de simplicidad:

- Netlify o Cloudflare Pages: arrastrar la carpeta sobre el panel.
- GitHub Pages: subir al repositorio y activar Pages. El archivo `.nojekyll`
  ya viene incluido.
- Hosting propio: copiar por FTP al directorio público.

## Después de publicar

1. Abrir el sitio y comprobar que el logo aparece en la cabecera.
2. Inscribirse con datos de prueba y completar un módulo entero.
3. Verificar que el certificado imprime bien en A4 vertical.
4. Confirmar que el código del certificado se registra en la planilla del
   backend.

## Backend de certificación

En el proyecto de Apps Script existente: reemplazar `1_Codigo.gs`, agregar
`verificar.html` y publicar con **Administrar implementaciones → Editar →
Versión nueva**. Crear una implementación nueva cambia la URL y deja sin
verificación los certificados ya emitidos.

La URL `/exec` debe quedar cargada en `assets/ac_programa.js` **antes** de
ejecutar `empaquetar.py`.
"""


PLANTILLA_UNICO = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Programa MRC-2026 · AuditCaat's Data Assurance</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;500;600;700&family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>

<header class="ac-cabecera ac-no-imprimir">
  <div class="ac-envoltura ac-cabecera-fila">
    <div class="ac-logo" id="logo"><span>AC</span></div>
    <div class="ac-cabecera-txt">
      <strong id="cab-titulo">AuditCaat's Data Assurance</strong>
      <small id="cab-ref">Programa de formación interna</small>
    </div>
    <div class="ac-cabecera-fin" id="cab-participante"></div>
  </div>
</header>

<main id="app"></main>

<script>
{js_base}
</script>

<script>
/* ===================================================================
   Navegacion del archivo unico.
   Solo un modulo esta en el DOM a la vez, para que el runtime
   compartido siga usando selectores simples.
   =================================================================== */
(function () {{
  const $ = AC.util.$;
  const app = document.getElementById("app");

  const MODULOS_HTML = {modulos_html};
  const BANCOS = {bancos};
  const PORTAL_HTML = {portal_main};

  // Las rutas pasan a ser de hash: no hay archivos separados.
  AC.Rutas.cert = id => "#/cert/" + id;
  AC.Rutas.diploma = () => "#/diploma";
  AC.Rutas.indice = () => "#/";
  AC.programa.modulos.forEach(m => {{ m.url = "#/m/" + m.id; }});

  if (getComputedStyle(document.documentElement).getPropertyValue("--ac-logo").trim() !== "none") {{
    $("#logo").classList.add("tiene-imagen");
  }}

  function encabezado(titulo, sub) {{
    $("#cab-titulo").textContent = titulo;
    $("#cab-ref").textContent = sub;
  }}

  function montarPortal() {{
    app.className = "";
    app.innerHTML = PORTAL_HTML;
    encabezado("AuditCaat's Data Assurance", "Programa de formación interna");
    portalJS();
  }}

  function portalJS() {{
{portal_js}
  }}

  function montarModulo(id) {{
    if (!MODULOS_HTML[id]) return montarPortal();
    if (!AC.Participante.obtener()) {{ location.hash = "#/"; return; }}
    const mod = AC.moduloPorId(id);
    app.className = "ac-angosto";
    app.style.paddingTop = "var(--e-7)";
    app.style.paddingBottom = "var(--e-8)";
    app.innerHTML = '<p class="ac-no-imprimir" style="margin-bottom:var(--e-5)">' +
                    '<a href="#/">Volver al índice</a></p>' + MODULOS_HTML[id];
    encabezado(mod.titulo, "Referencia " + mod.ref);
    ACModulo.iniciar(id, BANCOS[id]);
  }}

  function montarCertificado(id) {{
    if (!AC.Participante.obtener()) {{ location.hash = "#/"; return; }}
    app.className = "";
    app.style.padding = "0";
    app.innerHTML =
      '<div class="ac-envoltura ac-no-imprimir" style="padding-top:var(--e-5);' +
      'display:flex;gap:var(--e-3);flex-wrap:wrap">' +
      '<button class="ac-btn ac-btn-primario" id="btn-imprimir">Imprimir o guardar en PDF</button>' +
      '<a class="ac-btn ac-btn-secundario" id="btn-li" target="_blank" rel="noopener">Agregar a LinkedIn</a>' +
      '<button class="ac-btn ac-btn-secundario" id="btn-json">Descargar constancia</button>' +
      '<a class="ac-btn ac-btn-secundario" href="#/">Volver al índice</a></div><div id="hoja"></div>';
    const r = ACCert.render("#hoja", id === "__programa__"
      ? {{ tipo: "programa" }} : {{ tipo: "modulo", moduloId: id }});
    if (r) ACCert.enlazarAcciones(r.certificado, r.titulo);
    encabezado("Certificado", "AuditCaat's Data Assurance");
  }}

  function enrutar() {{
    const h = location.hash || "#/";
    if (h.indexOf("#/m/") === 0) montarModulo(h.slice(4));
    else if (h === "#/diploma") montarCertificado("__programa__");
    else if (h.indexOf("#/cert/") === 0) montarCertificado(h.slice(7));
    else montarPortal();
    if (window.scrollTo) window.scrollTo(0, 0);
  }}

  window.addEventListener("hashchange", enrutar);
  enrutar();
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    print("Empaquetando:")
    construir_sitio()
    construir_unico()
    print("Listo. Todo en dist/")
