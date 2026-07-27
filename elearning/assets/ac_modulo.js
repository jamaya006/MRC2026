/* ===================================================================
   AuditCaat's — Runtime de pagina de modulo  (ac_modulo.js)
   Requiere ac_programa.js y ac_engine.js.

   Un modulo solo declara su contenido y su banco de preguntas.
   Toda la mecanica vive aqui: marcado de cedulas, habilitacion de la
   evaluacion, calificacion y emision del certificado.
   =================================================================== */

(function (global) {
  "use strict";
  const $ = AC.util.$, $$ = AC.util.$$;

  const ACModulo = {
    iniciar(moduloId, banco) {
      const mod = AC.moduloPorId(moduloId);
      if (!mod) { console.error("Módulo no declarado en ac_programa.js:", moduloId); return; }

      // Sin inscripcion no se abre el modulo: los certificados necesitan
      // los datos del participante.
      if (!AC.Participante.obtener()) {
        location.href = AC.Rutas.indice();
        return;
      }

      this.mod = mod;
      this.banco = banco;

      if (getComputedStyle(document.documentElement).getPropertyValue("--ac-logo").trim() !== "none") {
        const l = $("#logo"); if (l) l.classList.add("tiene-imagen");
      }
      const t = $("#cab-titulo"); if (t) t.textContent = mod.titulo;
      const r = $("#cab-ref");   if (r) r.textContent = "Referencia " + mod.ref + " · " + mod.horas.toFixed(1).replace(".", ",") + " h";
      document.title = mod.titulo + " · AuditCaat's";

      this.restaurarCedulas();
      this.enlazarBotones();
      AC.Quiz.render("#quiz", banco);
      this.actualizarEstado();

      const btn = $("#btn-calificar");
      if (btn) btn.addEventListener("click", () => this.calificar());
    },

    cedulas() { return $$("[data-cedula]").map(n => n.dataset.cedula); },

    restaurarCedulas() {
      const p = AC.Progreso.modulo(this.mod.id);
      this.cedulas().forEach(id => { if (p.cedulas[id]) this.estampar(id, false); });
    },

    enlazarBotones() {
      $$("[data-marcar]").forEach(b =>
        b.addEventListener("click", () => {
          AC.Progreso.marcarCedula(this.mod.id, b.dataset.marcar);
          this.estampar(b.dataset.marcar, true);
          this.actualizarEstado();
        })
      );
    },

    estampar(cedulaId, animar) {
      const sello = $('[data-marca-de="' + cedulaId + '"]');
      if (sello) {
        sello.textContent = this.mod.marca;
        if (animar) sello.classList.add("puesta");
        else { sello.style.opacity = 1; sello.classList.add("puesta"); }
      }
      const btn = $('[data-marcar="' + cedulaId + '"]');
      if (btn) { btn.disabled = true; btn.textContent = "Cédula revisada"; }
    },

    actualizarEstado() {
      const p = AC.Progreso.modulo(this.mod.id);
      const total = this.cedulas().length;
      const hechas = this.cedulas().filter(id => p.cedulas[id]).length;

      const lleno = $("#ac-avance-lleno"), txt = $("#ac-avance-txt");
      if (lleno) lleno.style.width = (total ? hechas / total * 100 : 0).toFixed(1) + "%";
      if (txt) txt.textContent = hechas + " de " + total + " cédulas revisadas";

      const listo = total > 0 && hechas === total;
      const btn = $("#btn-calificar");
      if (btn && !p.aprobado) btn.disabled = !listo;

      const aviso = $("#eval-aviso");
      if (aviso) {
        aviso.textContent = listo
          ? "Evaluación habilitada. Se aprueba con " + Math.round(AC.programa.aprobacionMinima * 100) + " %."
          : "Faltan " + (total - hechas) + " cédulas para habilitar la evaluación. Se aprueba con " +
            Math.round(AC.programa.aprobacionMinima * 100) + " %.";
      }

      if (p.aprobado) this.mostrarAprobado(p);
    },

    calificar() {
      const r = AC.Quiz.calificar("#quiz", this.banco);

      if (r.sinResponder > 0) {
        // Se califica igual: dejar preguntas en blanco es una decision del
        // participante, no un error del sistema. Solo se informa.
        $("#resultado").textContent = r.sinResponder + " pregunta(s) sin responder. ";
      }

      const aprobado = r.razon >= AC.programa.aprobacionMinima;
      AC.Progreso.guardar(this.mod.id, {
        puntaje: r.puntaje, maximo: r.maximo, aprobado: aprobado,
        rendido: new Date().toISOString()
      });

      $("#btn-calificar").disabled = true;
      const res = $("#resultado");
      res.textContent += r.puntaje + " / " + r.maximo + "  ·  " + Math.round(r.razon * 100) + " %  ·  " +
        (aprobado ? "Aprobado" : "No aprobado");
      res.style.color = aprobado ? "var(--ac-ok)" : "var(--ac-tick)";

      if (aprobado) {
        const cert = AC.Certificado.emitirModulo(this.mod.id);
        this.mostrarAprobado(AC.Progreso.modulo(this.mod.id));
        if (cert) $("#btn-cert").href = AC.Rutas.cert(this.mod.id);
      } else {
        // Reintento: se rehace el render para barajar de nuevo las opciones.
        const nuevo = document.createElement("button");
        nuevo.className = "ac-btn ac-btn-secundario";
        nuevo.textContent = "Repetir evaluación";
        nuevo.addEventListener("click", () => {
          AC.Quiz.render("#quiz", this.banco);
          res.textContent = "";
          $("#btn-calificar").disabled = false;
          nuevo.remove();
        });
        $("#btn-calificar").parentNode.appendChild(nuevo);
      }
    },

    mostrarAprobado(p) {
      const caja = $("#acciones-cert");
      if (caja) caja.style.display = "block";
      const btn = $("#btn-cert");
      if (btn) btn.href = AC.Rutas.cert(this.mod.id);
      const vol = $("#btn-indice");
      if (vol) vol.href = AC.Rutas.indice();
      const b = $("#btn-calificar");
      if (b) b.disabled = true;
    }
  };

  global.ACModulo = ACModulo;
})(window);
