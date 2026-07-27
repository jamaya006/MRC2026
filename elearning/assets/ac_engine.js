/* ===================================================================
   AuditCaat's — Motor del programa  (ac_engine.js)
   Requiere: ac_programa.js cargado antes que este archivo.

   Responsabilidades
     1. Guardar y recuperar al participante y su avance
     2. Renderizar el indice de legajo del portal
     3. Gestionar cedulas y estampado de marcas dentro de un modulo
     4. Renderizar y calificar la evaluacion (con barajado de opciones)
     5. Emitir certificado por modulo y diploma de programa
     6. Sincronizar con el backend de Apps Script

   Corregir un defecto aqui lo corrige en los ocho modulos.
   =================================================================== */

(function (global) {
  "use strict";

  /* ---------------------------------------------------------------
     1. Almacenamiento tolerante a fallos
     localStorage puede no estar disponible (modo privado, iframe con
     restricciones, visor de archivos). En ese caso se degrada a
     memoria: la sesion funciona igual, pero no persiste al cerrar.
     --------------------------------------------------------------- */
  const Store = (function () {
    const CLAVE = "auditcaats.programa.v1";
    let memoria = null;
    let hayDisco = false;
    try {
      const p = "__ac_probe__";
      localStorage.setItem(p, "1");
      localStorage.removeItem(p);
      hayDisco = true;
    } catch (e) { hayDisco = false; }

    function leer() {
      if (memoria) return memoria;
      if (hayDisco) {
        try {
          const crudo = localStorage.getItem(CLAVE);
          memoria = crudo ? JSON.parse(crudo) : estadoInicial();
        } catch (e) { memoria = estadoInicial(); }
      } else {
        memoria = estadoInicial();
      }
      return memoria;
    }
    function escribir(estado) {
      memoria = estado;
      if (!hayDisco) return false;
      try { localStorage.setItem(CLAVE, JSON.stringify(estado)); return true; }
      catch (e) { return false; }
    }
    function estadoInicial() {
      return { participante: null, modulos: {}, diploma: null, version: 1 };
    }
    return { leer, escribir, persistente: () => hayDisco, reiniciar: () => escribir(estadoInicial()) };
  })();

  /* ---------------------------------------------------------------
     2. Utilidades
     --------------------------------------------------------------- */

  // Hash determinista (FNV-1a de 32 bits). Mismo participante y mismo
  // modulo producen siempre el mismo codigo de verificacion.
  function hash32(txt) {
    let h = 0x811c9dc5;
    for (let i = 0; i < txt.length; i++) {
      h ^= txt.charCodeAt(i);
      h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
    }
    return h >>> 0;
  }
  function base32(n, largo) {
    const A = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"; // sin I, L, O, 0, 1
    let s = "";
    for (let i = 0; i < largo; i++) { s = A[n % A.length] + s; n = Math.floor(n / A.length); }
    return s;
  }
  // Formato AC-2026-XXXXX-XXXX, compatible con los certificados ya emitidos
  function generarCodigo(participante, moduloId) {
    const semilla = [participante.documento, participante.nombre, moduloId, AC_PROGRAMA.codigo]
      .join("|").toUpperCase().replace(/\s+/g, " ").trim();
    const a = hash32(semilla);
    const b = hash32(semilla + "#2");
    return "AC-" + AC_PROGRAMA.anio + "-" + base32(a, 5) + "-" + base32(b, 4);
  }

  // Fisher-Yates. Sin esto, todas las respuestas correctas terminan
  // en la misma posicion y el participante aprueba por patron.
  function barajar(arr) {
    const c = arr.slice();
    for (let i = c.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [c[i], c[j]] = [c[j], c[i]];
    }
    return c;
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, m =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
  }
  function hoy() {
    return new Date().toLocaleDateString("es-CL", { day: "2-digit", month: "long", year: "numeric" });
  }
  const $ = (sel, raiz) => (raiz || document).querySelector(sel);
  const $$ = (sel, raiz) => Array.prototype.slice.call((raiz || document).querySelectorAll(sel));

  /* ---------------------------------------------------------------
     3. Participante
     --------------------------------------------------------------- */
  const Participante = {
    obtener() { return Store.leer().participante; },
    registrar(datos) {
      const e = Store.leer();
      e.participante = {
        nombre: datos.nombre.trim(),
        documento: datos.documento.trim().toUpperCase(),
        email: datos.email.trim().toLowerCase(),
        cargo: datos.cargo,
        organizacion: datos.organizacion.trim(),
        alta: new Date().toISOString()
      };
      Store.escribir(e);
      return e.participante;
    },
    salir() { Store.reiniciar(); }
  };

  /* ---------------------------------------------------------------
     4. Progreso
     Estructura por modulo:
       { cedulas: {A1:true,...}, puntaje: 0, maximo: 0, aprobado: false,
         certificado: {codigo, fecha}, convalidado: false }
     --------------------------------------------------------------- */
  const Progreso = {
    modulo(id) {
      const e = Store.leer();
      if (!e.modulos[id]) {
        e.modulos[id] = { cedulas: {}, puntaje: 0, maximo: 0, aprobado: false, certificado: null };
        Store.escribir(e);
      }
      return e.modulos[id];
    },
    guardar(id, parcial) {
      const e = Store.leer();
      e.modulos[id] = Object.assign(this.modulo(id), parcial);
      Store.escribir(e);
      return e.modulos[id];
    },
    marcarCedula(moduloId, cedulaId) {
      const m = this.modulo(moduloId);
      m.cedulas[cedulaId] = true;
      this.guardar(moduloId, m);
      return m;
    },
    // Un modulo se abre si el anterior esta aprobado. El primero siempre abierto.
    disponible(moduloId) {
      const idx = AC_PROGRAMA.modulos.findIndex(m => m.id === moduloId);
      if (idx <= 0) return true;
      const previo = AC_PROGRAMA.modulos[idx - 1];
      return !!this.modulo(previo.id).aprobado;
    },
    aprobados() {
      return AC_PROGRAMA.modulos.filter(m => this.modulo(m.id).aprobado).length;
    },
    programaCompleto() {
      const publicados = AC_PROGRAMA.modulos.filter(m => m.estadoPublicacion === "publicado");
      return publicados.length === AC_PROGRAMA.modulos.length &&
             this.aprobados() === AC_PROGRAMA.modulos.length;
    },
    // Convalida el Modulo I a quien ya tiene certificado emitido, sin
    // obligarlo a repetir el curso.
    convalidar(moduloId, codigo) {
      if (!/^AC-\d{4}-[A-Z0-9]{5}-[A-Z0-9]{4}$/.test(codigo.trim().toUpperCase())) return false;
      const p = Participante.obtener();
      if (!p) return false;
      this.guardar(moduloId, {
        aprobado: true, convalidado: true,
        certificado: { codigo: codigo.trim().toUpperCase(), fecha: hoy(), convalidado: true }
      });
      return true;
    }
  };

  /* ---------------------------------------------------------------
     5. Evaluacion
     Banco esperado:
       [{ id:"q1", texto:"...", puntaje:10,
          opciones:[{txt:"...", ok:true}, ...],
          retro:"por que la correcta es la correcta" }]
     --------------------------------------------------------------- */
  const Quiz = {
    render(contenedor, banco) {
      const nodo = typeof contenedor === "string" ? $(contenedor) : contenedor;
      if (!nodo) return;
      nodo.innerHTML = banco.map((p, i) => {
        const ops = barajar(p.opciones.map((o, k) => Object.assign({ _k: k }, o)));
        return '<div class="ac-pregunta" data-q="' + esc(p.id) + '">' +
          '<div class="ac-pregunta-num">Pregunta ' + (i + 1) + ' de ' + banco.length +
          '  ·  ' + (p.puntaje || 10) + ' puntos</div>' +
          '<div class="ac-pregunta-txt">' + esc(p.texto) + '</div>' +
          ops.map(o =>
            '<label class="ac-opcion">' +
            '<input type="radio" name="' + esc(p.id) + '" value="' + (o.ok ? "1" : "0") + '">' +
            '<span>' + esc(o.txt) + '</span></label>').join("") +
          '<div class="ac-retro">' + esc(p.retro || "") + '</div>' +
          '</div>';
      }).join("");
      nodo.dataset.banco = "listo";
    },

    calificar(contenedor, banco) {
      const nodo = typeof contenedor === "string" ? $(contenedor) : contenedor;
      let puntaje = 0, maximo = 0, sinResponder = 0;

      banco.forEach(p => {
        const val = p.puntaje || 10;
        maximo += val;
        const bloque = $('[data-q="' + p.id + '"]', nodo);
        const marcado = $('input[name="' + p.id + '"]:checked', bloque);
        if (!marcado) { sinResponder++; }
        else if (marcado.value === "1") { puntaje += val; }

        $$(".ac-opcion", bloque).forEach(op => {
          const inp = $("input", op);
          if (inp.value === "1") op.classList.add("correcta");
          else if (inp.checked) op.classList.add("incorrecta");
          inp.disabled = true;
        });
        $(".ac-retro", bloque).classList.add("visible");
      });

      return { puntaje, maximo, sinResponder, razon: maximo ? puntaje / maximo : 0 };
    }
  };

  /* ---------------------------------------------------------------
     6. Certificacion
     --------------------------------------------------------------- */
  const Certificado = {
    emitirModulo(moduloId) {
      const p = Participante.obtener();
      if (!p) return null;
      const m = Progreso.modulo(moduloId);
      if (!m.aprobado) return null;
      if (m.certificado) return m.certificado;

      const cert = {
        tipo: "modulo",
        modulo: moduloId,
        codigo: generarCodigo(p, moduloId),
        fecha: hoy(),
        emision: new Date().toISOString(),
        puntaje: m.puntaje,
        maximo: m.maximo
      };
      Progreso.guardar(moduloId, { certificado: cert });
      Backend.registrar(cert, p);
      return cert;
    },

    emitirDiploma() {
      const p = Participante.obtener();
      if (!p || !Progreso.programaCompleto()) return null;
      const e = Store.leer();
      if (e.diploma) return e.diploma;

      const total = AC_PROGRAMA.modulos.reduce((a, m) => {
        const r = Progreso.modulo(m.id);
        return { p: a.p + (r.puntaje || 0), x: a.x + (r.maximo || 0) };
      }, { p: 0, x: 0 });

      e.diploma = {
        tipo: "programa",
        modulo: AC_PROGRAMA.codigo,
        codigo: generarCodigo(p, AC_PROGRAMA.codigo),
        fecha: hoy(),
        emision: new Date().toISOString(),
        puntaje: total.p, maximo: total.x,
        horas: AC_PROGRAMA.horasTotales
      };
      Store.escribir(e);
      Backend.registrar(e.diploma, p);
      return e.diploma;
    },

    urlLinkedIn(cert, tituloModulo) {
      const q = new URLSearchParams({
        startTask: "CERTIFICATION_NAME",
        name: tituloModulo,
        organizationName: AC_PROGRAMA.emisor,
        issueYear: String(new Date().getFullYear()),
        issueMonth: String(new Date().getMonth() + 1),
        certId: cert.codigo
      });
      if (AC_BACKEND) q.set("certUrl", AC_BACKEND + "?verificar=" + cert.codigo);
      return "https://www.linkedin.com/profile/add?" + q.toString();
    },

    descargarConstancia(cert) {
      const p = Participante.obtener();
      const blob = new Blob([JSON.stringify({ programa: AC_PROGRAMA.codigo, participante: p, certificado: cert }, null, 2)],
        { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "constancia_" + cert.codigo + ".json";
      a.click();
      URL.revokeObjectURL(a.href);
    }
  };

  /* ---------------------------------------------------------------
     7. Backend
     Envio sin CORS: Apps Script no responde encabezados CORS a fetch
     con JSON. Se envia como texto plano en modo no-cors; la respuesta
     no se lee, por eso el registro local manda y el backend solo
     acumula para verificacion publica.
     --------------------------------------------------------------- */
  const Backend = {
    registrar(cert, participante) {
      if (!AC_BACKEND) return Promise.resolve({ ok: false, motivo: "sin backend configurado" });
      const carga = {
        accion: "emitir",
        programa: AC_PROGRAMA.codigo,
        certificado: cert,
        participante: {
          nombre: participante.nombre, documento: participante.documento,
          email: participante.email, cargo: participante.cargo,
          organizacion: participante.organizacion
        }
      };
      return fetch(AC_BACKEND, {
        method: "POST", mode: "no-cors",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify(carga)
      }).then(() => ({ ok: true })).catch(err => ({ ok: false, motivo: String(err) }));
    }
  };

  /* ---------------------------------------------------------------
     8. Portal: indice de legajo
     --------------------------------------------------------------- */
  const Portal = {
    render(sel) {
      const nodo = $(sel);
      if (!nodo) return;

      nodo.innerHTML = AC_PROGRAMA.modulos.map(m => {
        const r = Progreso.modulo(m.id);
        const abierto = Progreso.disponible(m.id);
        const publicado = m.estadoPublicacion === "publicado";
        const habilitado = abierto && publicado;

        let estado = "pendiente", texto = "Pendiente";
        if (r.aprobado) { estado = "aprobado"; texto = r.convalidado ? "Convalidado" : "Aprobado"; }
        else if (!publicado) { estado = "bloqueado"; texto = m.estadoPublicacion === "en produccion" ? "En preparación" : "No publicado"; }
        else if (!abierto) { estado = "bloqueado"; texto = "Requiere " + AC_PROGRAMA.modulos[AC_PROGRAMA.modulos.findIndex(x => x.id === m.id) - 1].ref; }
        else if (Object.keys(r.cedulas).length) { estado = "curso"; texto = "En curso"; }

        const etiqueta = habilitado ? "a" : "div";
        const attrs = habilitado
          ? 'href="' + esc(m.url) + '"'
          : 'aria-disabled="true" tabindex="0" role="link" aria-label="' + esc(m.titulo + ". " + texto) + '"';

        return "<" + etiqueta + ' class="ac-fila" ' + attrs + ">" +
          '<div class="ac-ref">' + esc(m.ref) + "</div>" +
          "<div>" +
            '<div class="ac-fila-tit">' + esc(m.titulo) + "</div>" +
            '<div class="ac-fila-sub">' + esc(m.resumen) + "</div>" +
          "</div>" +
          '<div class="ac-fila-meta">' + m.horas.toFixed(1).replace(".", ",") + " h · " + esc(m.clase) + "<br>" +
            esc(m.entregable) + "</div>" +
          '<div><span class="ac-estado ' + estado + '">' + esc(texto) + "</span></div>" +
          '<div class="ac-marca-aud ' + (r.aprobado ? "puesta" : "") + '">' + (r.aprobado ? esc(m.marca) : "") + "</div>" +
        "</" + etiqueta + ">";
      }).join("");

      this.avance();
    },

    avance() {
      const lleno = $("#ac-avance-lleno");
      const txt = $("#ac-avance-txt");
      if (!lleno) return;
      const n = Progreso.aprobados(), t = AC_PROGRAMA.modulos.length;
      lleno.style.width = (n / t * 100).toFixed(1) + "%";
      if (txt) txt.textContent = n + " de " + t + " módulos aprobados";
    }
  };

  /* ---------------------------------------------------------------
     9. API publica
     --------------------------------------------------------------- */
  // Rutas de navegacion. El empaquetador de archivo unico las reemplaza
  // por rutas de hash para que el mismo runtime sirva en ambos formatos.
  const Rutas = {
    cert: id => "../certificado.html?modulo=" + id,
    diploma: () => "certificado.html?tipo=programa",
    indice: () => "../index.html"
  };

  global.AC = {
    programa: AC_PROGRAMA,
    Rutas,
    Store, Participante, Progreso, Quiz, Certificado, Backend, Portal,
    util: { esc, hoy, barajar, generarCodigo, $, $$ },
    moduloPorId: id => AC_PROGRAMA.modulos.find(m => m.id === id)
  };

})(window);
