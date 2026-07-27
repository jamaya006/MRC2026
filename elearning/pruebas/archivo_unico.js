/* Prueba del empaquetado de archivo unico: navegacion por hash y flujo completo. */
const { JSDOM } = require('jsdom');
const fs = require('fs');
const ARCHIVO = '/home/claude/elearning/dist/AuditCaats_MRC2026.html';

let fallas = 0;
const t = (n, c) => { console.log((c ? '  ok   ' : '  FALLA ') + n); if (!c) fallas++; };

const dom = new JSDOM(fs.readFileSync(ARCHIVO, 'utf8'),
  { runScripts: 'dangerously', url: 'https://x.test/AuditCaats_MRC2026.html', pretendToBeVisual: true });
const w = dom.window, d = w.document;

t('el archivo abre en el portal', !!d.querySelector('#bloque-registro'));
t('no hay recursos externos de assets', !/src="assets|href="assets/.test(fs.readFileSync(ARCHIVO, 'utf8')));

d.querySelector('#f-nombre').value = 'Jorge Amaya';
d.querySelector('#f-doc').value = '12345678-9';
d.querySelector('#f-mail').value = 'jamaya@auditcaats.com';
d.querySelector('#f-cargo').value = 'Auditor externo';
d.querySelector('#f-org').value = "AuditCaat's";
d.querySelector('#btn-inscribir').click();
t('inscribe desde el archivo único', w.AC.Participante.obtener().nombre === 'Jorge Amaya');

const filas = d.querySelectorAll('#ruta .ac-fila');
t('el índice lista los ocho módulos', filas.length === 8);
t('los enlaces son de navegación interna', filas[0].getAttribute('href') === '#/m/M01');

// navegar al módulo I
w.location.hash = '#/m/M01';
w.dispatchEvent(new w.HashChangeEvent('hashchange'));
t('entra al Módulo I', d.querySelectorAll('[data-cedula]').length === 7);
t('el laboratorio en Python se renderiza', !!d.querySelector('.ac-codigo pre code'));
t('el encabezado cambia al módulo',
  d.querySelector('#cab-titulo').textContent.indexOf('Por qué un contador') === 0);

d.querySelectorAll('[data-marcar]').forEach(b => b.click());
d.querySelectorAll('.ac-pregunta').forEach(p => {
  Array.from(p.querySelectorAll('input')).find(i => i.value === '1').checked = true;
});
d.querySelector('#btn-calificar').click();
t('aprueba dentro del archivo único', w.AC.Progreso.modulo('M01').aprobado === true);
t('el enlace al certificado usa hash',
  d.querySelector('#btn-cert').getAttribute('href') === '#/cert/M01');
t('el botón de volver al índice se resuelve a hash',
  d.querySelector('#btn-indice').getAttribute('href') === '#/');

// certificado
w.location.hash = '#/cert/M01';
w.dispatchEvent(new w.HashChangeEvent('hashchange'));
t('renderiza el certificado', !!d.querySelector('.ac-cert'));
t('el certificado lleva el nombre',
  d.querySelector('.ac-cert .nombre').textContent.trim() === 'Jorge Amaya');

// volver y comprobar desbloqueo
w.location.hash = '#/';
w.dispatchEvent(new w.HashChangeEvent('hashchange'));
const f2 = d.querySelectorAll('#ruta .ac-fila');
t('el portal recuerda el avance al volver', f2[0].textContent.includes('Aprobado'));
t('M02 queda desbloqueado', f2[1].getAttribute('href') === '#/m/M02');

// módulo II debe montar limpio, sin restos del I
w.location.hash = '#/m/M02';
w.dispatchEvent(new w.HashChangeEvent('hashchange'));
t('el Módulo II monta con sus propias cédulas',
  d.querySelector('[data-cedula]').dataset.cedula === 'B-1');
t('no quedan cédulas del módulo anterior en el DOM',
  d.querySelectorAll('[data-cedula^="A-"]').length === 0);

console.log('\n' + (fallas === 0 ? 'ARCHIVO ÚNICO: TODAS LAS PRUEBAS PASAN' : fallas + ' FALLAS'));
process.exit(fallas ? 1 : 0);
