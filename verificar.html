/**
 * AuditCaat's — Registro y verificacion de certificados
 * Programa MRC-2026
 *
 * Reemplaza al 1_Codigo.gs del Modulo I. Mantiene la misma hoja de
 * calculo y el mismo formato de codigo, de modo que los certificados
 * ya emitidos siguen verificando.
 *
 * IMPORTANTE AL PUBLICAR
 * Usar siempre "Implementar > Administrar implementaciones > Editar >
 * Version nueva" sobre la implementacion existente. Crear una
 * implementacion nueva cambia la URL y rompe la verificacion de los
 * certificados ya entregados.
 */

var HOJA_ID   = '';            // id de la planilla; vacio = crea una propia
var HOJA_NOM  = 'certificados';
var COLUMNAS  = ['fecha_registro','codigo','tipo','modulo','programa','nombre',
                 'documento','email','cargo','organizacion','puntaje','maximo','fecha_emision'];

/* ------------------------------------------------------------------ */
/* Hoja                                                                */
/* ------------------------------------------------------------------ */
function _hoja() {
  var libro = HOJA_ID ? SpreadsheetApp.openById(HOJA_ID) : SpreadsheetApp.getActiveSpreadsheet();
  if (!libro) {
    libro = SpreadsheetApp.create('AuditCaats - Certificados MRC-2026');
    PropertiesService.getScriptProperties().setProperty('HOJA_ID', libro.getId());
  }
  var h = libro.getSheetByName(HOJA_NOM);
  if (!h) {
    h = libro.insertSheet(HOJA_NOM);
    h.appendRow(COLUMNAS);
    h.setFrozenRows(1);
  }
  return h;
}

/* ------------------------------------------------------------------ */
/* Emision (POST desde el e-learning)                                  */
/* ------------------------------------------------------------------ */
function doPost(e) {
  var salida = { ok: false };
  try {
    var d = JSON.parse(e.postData.contents);
    if (d.accion !== 'emitir') throw new Error('accion no reconocida');

    var c = d.certificado || {};
    var p = d.participante || {};
    if (!c.codigo) throw new Error('certificado sin codigo');

    // Idempotente: si el codigo ya esta registrado no se duplica.
    if (!_buscar(c.codigo)) {
      _hoja().appendRow([
        new Date(), c.codigo, c.tipo || 'modulo', c.modulo || '', d.programa || '',
        p.nombre || '', p.documento || '', p.email || '', p.cargo || '', p.organizacion || '',
        c.puntaje || 0, c.maximo || 0, c.emision || ''
      ]);
    }
    salida = { ok: true, codigo: c.codigo };
  } catch (err) {
    salida = { ok: false, error: String(err) };
  }
  return ContentService.createTextOutput(JSON.stringify(salida))
                       .setMimeType(ContentService.MimeType.JSON);
}

function _buscar(codigo) {
  var datos = _hoja().getDataRange().getValues();
  for (var i = 1; i < datos.length; i++) {
    if (String(datos[i][1]).toUpperCase() === String(codigo).toUpperCase()) {
      var fila = {};
      COLUMNAS.forEach(function (col, k) { fila[col] = datos[i][k]; });
      return fila;
    }
  }
  return null;
}

/* Expuesta a la pagina mediante google.script.run.                     */
/* No se usa un formulario GET porque Apps Script sirve la pagina       */
/* dentro de un iframe y el envio se pierde.                            */
function verificarCodigo(codigo) {
  var r = _buscar(String(codigo || '').trim());
  if (!r) return { hallado: false };
  return {
    hallado: true,
    codigo: r.codigo,
    nombre: r.nombre,
    organizacion: r.organizacion,
    tipo: r.tipo,
    modulo: r.modulo,
    programa: r.programa,
    puntaje: r.puntaje,
    maximo: r.maximo,
    fecha: Utilities.formatDate(new Date(r.fecha_registro),
             Session.getScriptTimeZone(), 'dd-MM-yyyy')
  };
}

/* ------------------------------------------------------------------ */
/* Verificacion publica (GET)                                          */
/* ------------------------------------------------------------------ */
function doGet(e) {
  var t = HtmlService.createTemplateFromFile('verificar');
  t.codigoInicial = (e && e.parameter && e.parameter.verificar) ? e.parameter.verificar : '';
  return t.evaluate()
          .setTitle("Verificación de certificados · AuditCaat's")
          .addMetaTag('viewport', 'width=device-width, initial-scale=1')
          .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
