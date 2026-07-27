const { JSDOM } = require('jsdom');
const fs = require('fs'), path = require('path');
const RAIZ = '/home/claude/elearning';

let fallas = 0;
const t = (n, c) => { console.log((c ? '  ok   ' : '  FALLA ') + n); if (!c) fallas++; };

function abrir(rel, estadoPrevio) {
  const file = path.join(RAIZ, rel.split('?')[0]);
  let html = fs.readFileSync(file, 'utf8');
  // resolver los <script src> relativos e incrustarlos
  html = html.replace(/<script src="([^"]+)"><\/script>/g, (m, src) => {
    const p = path.resolve(path.dirname(file), src);
    return '<script>' + fs.readFileSync(p, 'utf8') + '</script>';
  });
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/' + rel, pretendToBeVisual: true,
    beforeParse(w) {
      if (estadoPrevio) w.localStorage.setItem('auditcaats.programa.v1', estadoPrevio);
    }
  });
  return dom;
}

// ---------- 1. Portal sin inscripción ----------
let dom = abrir('index.html');
let d = dom.window.document;
t('portal muestra el formulario de inscripción', d.querySelector('#bloque-registro').hidden === false);
t('portal oculta la ruta sin participante', d.querySelector('#bloque-ruta').hidden === true);

// ---------- 2. Inscripción con datos inválidos ----------
d.querySelector('#f-nombre').value = 'Jorge';
d.querySelector('#btn-inscribir').click();
t('rechaza nombre sin apellido', d.querySelector('#f-nombre').closest('.ac-campo').classList.contains('invalido'));
t('sigue sin participante tras dato inválido', dom.window.AC.Participante.obtener() === null);

// ---------- 3. Inscripción válida ----------
const llenar = (doc) => {
  doc.querySelector('#f-nombre').value = 'Jorge Amaya';
  doc.querySelector('#f-doc').value = '12345678-9';
  doc.querySelector('#f-mail').value = 'jamaya@auditcaats.com';
  doc.querySelector('#f-cargo').value = 'Auditor externo';
  doc.querySelector('#f-org').value = "AuditCaat's";
  doc.querySelector('#btn-inscribir').click();
};
llenar(d);
t('inscribe con datos válidos', dom.window.AC.Participante.obtener().nombre === 'Jorge Amaya');
t('portal muestra la ruta tras inscribir', d.querySelector('#bloque-ruta').hidden === false);

const filas = d.querySelectorAll('#ruta .ac-fila');
t('el índice lista los ocho módulos', filas.length === 8);
t('M01 queda habilitado (es enlace)', filas[0].tagName === 'A');
t('M02 queda bloqueado hasta aprobar M01', filas[1].getAttribute('aria-disabled') === 'true');

// El estado del portal vive en localStorage; jsdom lo aísla por documento,
// así que se traspasa a mano al abrir el módulo.
const estado = dom.window.localStorage.getItem('auditcaats.programa.v1');

// ---------- 4. Recorrido del Módulo I ----------
const dm = abrir('modulos/m01.html', estado);
const dd = dm.window.document;

t('el módulo declara sus cédulas', dd.querySelectorAll('[data-cedula]').length === 7);
t('el módulo incluye laboratorio en Python', !!dd.querySelector('.ac-codigo'));
t('calificar arranca deshabilitado', dd.querySelector('#btn-calificar').disabled === true);

dd.querySelectorAll('[data-marcar]').forEach(b => b.click());
t('calificar se habilita al marcar todas las cédulas', dd.querySelector('#btn-calificar').disabled === false);
t('la marca de auditoría queda estampada',
  dd.querySelector('[data-marca-de="A-1"]').textContent === '✓');

// responder todo correcto
dd.querySelectorAll('.ac-pregunta').forEach(p => {
  const ok = Array.from(p.querySelectorAll('input')).find(i => i.value === '1');
  ok.checked = true;
});
dd.querySelector('#btn-calificar').click();

const prog = dm.window.AC.Progreso.modulo('M01');
t('aprueba con 100/100', prog.puntaje === 100 && prog.maximo === 100 && prog.aprobado === true);
t('emite certificado al aprobar', !!prog.certificado && /^AC-2026-/.test(prog.certificado.codigo));
t('muestra las acciones de certificado', dd.querySelector('#acciones-cert').style.display === 'block');
t('marca las opciones correctas en la retroalimentación',
  dd.querySelectorAll('.ac-opcion.correcta').length === 10);
t('deshabilita las opciones tras calificar',
  Array.from(dd.querySelectorAll('.ac-opcion input')).every(i => i.disabled));

// ---------- 5. Reprobar y reintentar ----------
const dm2 = abrir('modulos/m02.html',
  dm.window.localStorage.getItem('auditcaats.programa.v1'));
const d2 = dm2.window.document;
d2.querySelectorAll('[data-marcar]').forEach(b => b.click());
// responder solo 4 correctas
d2.querySelectorAll('.ac-pregunta').forEach((p, i) => {
  const inputs = Array.from(p.querySelectorAll('input'));
  (i < 4 ? inputs.find(x => x.value === '1') : inputs.find(x => x.value === '0')).checked = true;
});
d2.querySelector('#btn-calificar').click();
t('reprueba con 40/100', dm2.window.AC.Progreso.modulo('M02').aprobado === false);
t('no emite certificado si reprueba', dm2.window.AC.Progreso.modulo('M02').certificado == null);
const rep = Array.from(d2.querySelectorAll('button')).find(b => b.textContent === 'Repetir evaluación');
t('ofrece repetir la evaluación', !!rep);
rep.click();
t('rehabilita calificar al repetir', d2.querySelector('#btn-calificar').disabled === false);
t('limpia las marcas de corrección al repetir', d2.querySelectorAll('.ac-opcion.correcta').length === 0);

// ---------- 6. Portal tras aprobar M01 ----------
const dom3 = abrir('index.html', dm.window.localStorage.getItem('auditcaats.programa.v1'));
const d3 = dom3.window.document;
const f3 = d3.querySelectorAll('#ruta .ac-fila');
t('M01 aparece aprobado en el índice', f3[0].textContent.includes('Aprobado'));
t('M02 se desbloquea tras aprobar M01', f3[1].tagName === 'A');
t('la marca del módulo aprobado se ve en el índice',
  f3[0].querySelector('.ac-marca-aud').classList.contains('puesta'));

// ---------- 7. Certificado ----------
const dcert = abrir('certificado.html?modulo=M01',
  dm.window.localStorage.getItem('auditcaats.programa.v1'));
const dq = dcert.window.document;
t('el certificado se renderiza', !!dq.querySelector('.ac-cert'));
t('el certificado lleva el nombre del participante',
  dq.querySelector('.ac-cert .nombre').textContent.trim() === 'Jorge Amaya');
t('el certificado muestra el código de verificación',
  /^AC-2026-/.test(dq.querySelector('.ac-cert .codigo').textContent.trim()));
t('el botón de LinkedIn apunta al perfil',
  dq.querySelector('#btn-li').href.startsWith('https://www.linkedin.com/profile/add'));

console.log('\n' + (fallas === 0 ? 'TODAS LAS PRUEBAS DE RECORRIDO PASAN' : fallas + ' FALLAS'));
process.exit(fallas ? 1 : 0);
