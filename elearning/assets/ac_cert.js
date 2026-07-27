/* ===================================================================
   AuditCaat's — Vista del certificado  (ac_cert.js)
   Usada por certificado.html y por el empaquetado de archivo unico,
   para que exista una sola definicion del documento emitido.
   =================================================================== */

(function (global) {
  "use strict";

  function logoSrc() {
    const v = getComputedStyle(document.documentElement)
      .getPropertyValue("--ac-logo-tinta").trim();
    if (!v || v === "none") return "";
    // En impresion los fondos CSS no se pintan: el certificado usa <img>.
    return v.replace(/^url\(["']?/, "").replace(/["']?\)$/, "");
  }

  const ACCert = {
    /**
     * @param {Element|string} destino  contenedor donde dibujar
     * @param {Object} opciones  { tipo: "modulo"|"programa", moduloId }
     * @return {Object|null} el certificado dibujado, o null si no existe
     */
    render(destino, opciones) {
      const nodo = typeof destino === "string" ? document.querySelector(destino) : destino;
      const esc = AC.util.esc;
      const p = AC.Participante.obtener();
      if (!nodo || !p) return null;

      let cert, titulo, detalle;

      if (opciones.tipo === "programa") {
        cert = AC.Store.leer().diploma;
        titulo = AC.programa.titulo;
        detalle = "Programa completo de " + AC.programa.horasTotales + " horas · " +
                  AC.programa.modulos.length + " módulos";
      } else {
        const mod = AC.moduloPorId(opciones.moduloId);
        if (!mod) return null;
        cert = AC.Progreso.modulo(mod.id).certificado;
        titulo = mod.titulo;
        detalle = "Módulo " + mod.ref + " · " +
                  mod.horas.toFixed(1).replace(".", ",") + " horas lectivas";
      }

      if (!cert) {
        nodo.innerHTML =
          '<div class="ac-angosto" style="padding:var(--e-7) var(--e-5)">' +
          '<div class="ac-cedula"><div class="ac-cedula-cuerpo">' +
          "<p>Todavía no hay un certificado emitido para este módulo en este " +
          "navegador. Complétalo desde el índice, o convalídalo con su código si " +
          "ya lo aprobaste antes.</p></div></div></div>";
        return null;
      }

      const src = logoSrc();
      const verif = AC_BACKEND
        ? "Verificable en " + esc(AC_BACKEND) + "?verificar=" + esc(cert.codigo)
        : "Código de verificación";

      nodo.innerHTML =
        '<div class="ac-cert"><div class="ac-cert-borde">' +
          (src ? '<img class="logo" src="' + src + '" alt="AuditCaat\'s Data Assurance">' : "") +
          '<div class="sub">' + esc(AC.programa.emisor) + "</div>" +
          "<h1>Certificado de aprobación</h1>" +
          '<p style="text-align:center;margin:8mm 0 4mm">Se deja constancia de que</p>' +
          '<div class="nombre">' + esc(p.nombre) + "</div>" +
          '<p style="text-align:center;margin:0 0 8mm">documento ' + esc(p.documento) +
            " · " + esc(p.organizacion) + "</p>" +
          '<p style="text-align:center">aprobó</p>' +
          '<h2 style="text-align:center;font-size:16pt;margin:4mm 0">' + esc(titulo) + "</h2>" +
          '<p style="text-align:center;color:var(--ac-tinta-2);font-size:10pt">' +
            esc(detalle) + "</p>" +
          '<p style="text-align:center;margin-top:6mm;font-size:10pt">Puntaje obtenido: ' +
            cert.puntaje + " de " + cert.maximo + "</p>" +
          '<p style="text-align:center;margin-top:12mm;font-size:10pt">' + esc(cert.fecha) + "</p>" +
          '<div style="position:absolute;left:0;right:0;bottom:10mm;text-align:center">' +
            '<div class="codigo">' + esc(cert.codigo) + "</div>" +
            '<div style="font-size:8pt;color:var(--ac-tinta-3);margin-top:2mm">' + verif + "</div>" +
          "</div>" +
        "</div></div>";

      return { certificado: cert, titulo: titulo };
    },

    /** Conecta los tres controles de la barra superior. */
    enlazarAcciones(cert, titulo) {
      const li = document.querySelector("#btn-li");
      if (li) li.href = AC.Certificado.urlLinkedIn(cert, titulo);
      const js = document.querySelector("#btn-json");
      if (js) js.onclick = () => AC.Certificado.descargarConstancia(cert);
      const im = document.querySelector("#btn-imprimir");
      if (im) im.onclick = () => window.print();
    }
  };

  global.ACCert = ACCert;
})(window);
