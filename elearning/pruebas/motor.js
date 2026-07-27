// Stub minimo de navegador para probar la logica del motor sin DOM real
global.localStorage = (function(){ const m={}; return {
  getItem:k=>k in m?m[k]:null, setItem:(k,v)=>{m[k]=String(v)}, removeItem:k=>{delete m[k]} };})();
global.window = global;
global.document = { querySelector:()=>null, querySelectorAll:()=>[] };
const fs=require('fs'), path=require('path');
const A=n=>path.join(__dirname,'..','assets',n);
eval(fs.readFileSync(A('ac_programa.js'),'utf8').replace(/^const /gm,'global.'));
eval(fs.readFileSync(A('ac_engine.js'),'utf8'));

let fallas=0;
const t=(n,c)=>{ if(c) console.log('  ok   '+n); else {console.log('  FALLA '+n); fallas++;} };

console.log('Persistencia disponible:', AC.Store.persistente());

AC.Participante.registrar({nombre:'Jorge Amaya', documento:'12.345.678-9',
  email:'JAmaya@AuditCaats.com', cargo:'Auditor externo', organizacion:"AuditCaat's"});
t('participante registrado', AC.Participante.obtener().nombre==='Jorge Amaya');
t('email normalizado', AC.Participante.obtener().email==='jamaya@auditcaats.com');

t('M01 disponible al inicio', AC.Progreso.disponible('M01')===true);
t('M02 bloqueado sin aprobar M01', AC.Progreso.disponible('M02')===false);

// codigo determinista y con formato valido
const c1=AC.util.generarCodigo(AC.Participante.obtener(),'M01');
const c2=AC.util.generarCodigo(AC.Participante.obtener(),'M01');
const c3=AC.util.generarCodigo(AC.Participante.obtener(),'M02');
t('codigo determinista', c1===c2);
t('codigo distinto por modulo', c1!==c3);
t('formato de codigo '+c1, /^AC-2026-[A-Z0-9]{5}-[A-Z0-9]{4}$/.test(c1));

// convalidacion
t('convalidacion rechaza formato malo', AC.Progreso.convalidar('M01','XX-1')===false);
t('convalidacion acepta codigo valido', AC.Progreso.convalidar('M01','AC-2026-V8MKT-1DQ9')===true);
t('M02 se abre tras convalidar M01', AC.Progreso.disponible('M02')===true);
t('M01 marcado como convalidado', AC.Progreso.modulo('M01').convalidado===true);

// calificacion sin DOM: se prueba solo el barajado
const ops=[{txt:'a',ok:true},{txt:'b'},{txt:'c'},{txt:'d'}];
let posiciones=new Set();
for(let i=0;i<200;i++) posiciones.add(AC.util.barajar(ops).findIndex(o=>o.ok));
t('barajado distribuye la correcta en 4 posiciones', posiciones.size===4);

// diploma solo con todo aprobado
t('diploma bloqueado con programa incompleto', AC.Certificado.emitirDiploma()===null);
AC_PROGRAMA.modulos.forEach(m=>AC.Progreso.guardar(m.id,{aprobado:true,puntaje:90,maximo:100}));
t('programa completo con los ocho aprobados y publicados', AC.Progreso.programaCompleto()===true);
AC_PROGRAMA.modulos[3].estadoPublicacion='pendiente';
t('programa incompleto si un modulo se despublica', AC.Progreso.programaCompleto()===false);
AC_PROGRAMA.modulos[3].estadoPublicacion='publicado';
const d=AC.Certificado.emitirDiploma();
t('diploma emitido', d && /^AC-2026-/.test(d.codigo));
t('diploma suma puntajes', d.maximo===800);

// persistencia entre "recargas"
const crudo=JSON.parse(localStorage.getItem('auditcaats.programa.v1'));
t('estado persistido en disco', crudo.participante.nombre==='Jorge Amaya');

console.log(fallas===0?'\nTODAS LAS PRUEBAS PASAN':'\n'+fallas+' FALLAS');
process.exit(fallas?1:0);
