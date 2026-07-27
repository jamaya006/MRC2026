# Programa MRC-2026 — Validación de modelos de riesgo de crédito

Ocho módulos para auditores y contadores. Enfoque aplicado en **Python**:
cada módulo cierra con un laboratorio ejecutable sobre la cartera del curso.

AuditCaat's Data Assurance.

## Estructura

```
elearning/
├── index.html              Portal: inscripción, índice de legajo, avance, diploma
├── certificado.html        Certificado de módulo y diploma (A4 vertical)
├── assets/
│   ├── ac_marca.css        Paleta, tipografía y logo. Único archivo de identidad
│   ├── ac_estilo.css       Componentes compartidos
│   ├── ac_programa.js      Catálogo de los ocho módulos y URL del backend
│   ├── ac_engine.js        Motor: almacenamiento, progreso, quiz, certificados
│   └── ac_modulo.js        Runtime de página de módulo
├── generar.py             Genera los HTML de los módulos desde el contenido
├── empaquetar.py          Produce dist/: sitio autocontenido y archivo único
├── contenido/
│   ├── m01.py … m08.py     Contenido y banco de preguntas de cada módulo
│   └── labs.py             Laboratorios en Python, uno por módulo
├── modulos/
│   ├── m01.html … m08.html Generados: no se editan a mano
│   └── _plantilla.html     Referencia de la estructura
└── backend/
    ├── 1_Codigo.gs         Apps Script: registro y verificación
    └── verificar.html      Página pública de verificación
```

Un defecto corregido en `assets/` queda corregido en los ocho módulos.

## Puesta en marcha

**1. Logo.** Ya viene incrustado en `assets/ac_marca.css`, en dos variantes:
`--ac-logo` en blanco para la cabecera oscura y `--ac-logo-tinta` para el
certificado sobre papel. Si el logo cambia, se reemplazan ambas cadenas base64.

**2. Empaquetar.** Los archivos de la raíz enlazan `assets/` por ruta relativa,
así que abrirlos con doble clic no carga estilos ni scripts. Para obtener
versiones que funcionen sin servidor:

```bash
python3 empaquetar.py
```

Eso genera `dist/` con dos formatos:

| Archivo | Para qué sirve |
|---|---|
| `dist/AuditCaats_MRC2026.html` | Programa completo en un solo archivo, con navegación interna. Se abre de un toque en el teléfono y se manda por correo |
| `dist/index.html` y `dist/modulos/` | Sitio para publicar. Cada página lleva su CSS y su JS incrustados |

Volver a ejecutar `empaquetar.py` después de cada cambio en contenido o
en `assets/`: `dist/` se regenera completo y no se edita a mano.

**3. Publicar el backend.** En el proyecto de Apps Script existente:
reemplazar `1_Codigo.gs`, agregar `verificar.html` y conservar `2_Logo.gs`.
Publicar con **Administrar implementaciones → Editar → Versión nueva**.

> Crear una implementación nueva genera otra URL y deja sin verificación los
> certificados ya entregados. Es el error que ya ocurrió tres veces en el Módulo I.

**4. Enlazar el backend.** Copiar la URL `/exec` en `assets/ac_programa.js`:

```js
const AC_BACKEND = "https://script.google.com/a/macros/auditcaats.com/s/XXXX/exec";
```

**5. Publicar el sitio.** Cualquier hosting estático sirve. El portal no requiere
servidor de aplicación: el avance vive en el navegador del participante y solo
las emisiones de certificado viajan al backend.

## Entorno de los laboratorios

Python 3.11 con `pandas`, `numpy`, `scikit-learn` y `matplotlib`. El código de
los laboratorios está en `contenido/labs.py` y se anexa como última cédula de
cada módulo al generar. Editarlo ahí, no en el HTML.

```bash
pip install pandas numpy scikit-learn matplotlib
```

## Editar el contenido de un módulo

Los HTML de `modulos/` son generados. Editarlos a mano se pierde en la
siguiente ejecución. El contenido vive en `contenido/mNN.py`:

```python
MODULO = {
  "ref": "C",                      # prefijo de las cédulas
  "titulo": "...",
  "proposito": "...",              # recuadro de apertura
  "cedulas": [
    {"ref": "C-1", "titulo": "...", "bloques": [
      ("p", "párrafo"),
      ("nota",   "título", "texto"),   # verde: procedimiento
      ("riesgo", "título", "texto"),   # ámbar: qué sale mal
      ("umbral", "título", "texto"),   # rojo: valor citable
      ("cita", "texto", "Clase 3, aprox. 01:50:24"),
      ("lista", ["...", "..."]),
      ("pasos", ["...", "..."]),
      ("tabla", [["encabezado"], ["fila"]]),
      ("codigo", "título del bloque", "código Python"),
    ]},
  ],
  "banco": [ ... ],
}
```

Después:

```bash
python3 generar.py         # todos
python3 generar.py M06     # solo uno
```

El generador valida que las cédulas usen el prefijo del módulo y que cada
pregunta tenga exactamente una opción correcta. Marcar la correcta con
`ok: True`; el orden en que se escriban las opciones no importa, porque el
motor baraja en cada intento.

Un módulo no aparece habilitado en el portal hasta que está publicado **y** el
módulo anterior está aprobado.

## Pruebas

```bash
cd ..                      # donde está node_modules
node elearning/pruebas/motor.js          # lógica: códigos, gating, diploma
node elearning/pruebas/recorrido.js      # recorrido completo en DOM (requiere jsdom)
node elearning/pruebas/archivo_unico.js  # navegación y flujo del archivo único
```

`recorrido.js` cubre inscripción, validación de campos, marcado de cédulas,
aprobación, reprobación con reintento, desbloqueo del módulo siguiente y
emisión del certificado.

## Decisiones que conviene conocer

**Almacenamiento.** El avance se guarda en `localStorage`. Si el navegador lo
bloquea, el motor sigue funcionando en memoria y el portal lo advierte: la
sesión sirve, pero no sobrevive al cierre.

**Cambio de equipo.** El avance no se sincroniza entre navegadores. Para eso
está la convalidación: se ingresa el código del certificado y el módulo se marca
como aprobado sin repetirlo. Es también la vía para reconocer el Módulo I a
quienes lo aprobaron antes del portal.

**Códigos.** Deterministas: el mismo participante y el mismo módulo producen
siempre el mismo código. Rehacer un módulo no genera un código distinto ni
duplica el registro en la planilla.

**Aprobación.** 70 % del puntaje del módulo. Se puede repetir; en cada intento
las opciones se rebarajan.
