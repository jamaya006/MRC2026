/* ===================================================================
   AuditCaat's — Simuladores del programa  (ac_widgets.js)

   Cada simulador se declara en el contenido como ("widget", "id") y
   se monta sobre <div data-widget="id">. Todo se calcula en el
   navegador con SVG: sin librerias, sin red, sin imagenes.

   Los datos son sinteticos y deterministas: todos los participantes
   ven exactamente los mismos numeros.
   =================================================================== */

(function (global) {
  "use strict";

  /* ---------- Utilidades ------------------------------------------ */

  // Generador con semilla: misma semilla, misma serie, en todo navegador.
  function azar(semilla) {
    let a = semilla >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function normal(r) {                       // Box-Muller
    return Math.sqrt(-2 * Math.log(1 - r())) * Math.cos(2 * Math.PI * r());
  }
  const fmt = (n, d) => n.toLocaleString("es-CL", {
    minimumFractionDigits: d === undefined ? 0 : d,
    maximumFractionDigits: d === undefined ? 0 : d });
  const pct = (n, d) => fmt(n * 100, d === undefined ? 1 : d) + " %";
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

  /* ---------- Andamiaje de la interfaz ----------------------------- */

  function control(cfg) {
    const id = "w" + Math.random().toString(36).slice(2, 8);
    return `<div class="ac-w-ctrl">
      <label for="${id}">${cfg.etiqueta}<b data-valor></b></label>
      <input type="range" id="${id}" min="${cfg.min}" max="${cfg.max}"
             step="${cfg.paso || 1}" value="${cfg.valor}" data-slider="${cfg.nombre}">
    </div>`;
  }

  function interruptor(cfg) {
    return `<label class="ac-w-check">
      <input type="checkbox" data-check="${cfg.nombre}" ${cfg.valor ? "checked" : ""}>
      <span>${cfg.etiqueta}</span></label>`;
  }

  function armar(nodo, cfg) {
    nodo.innerHTML = `
      <div class="ac-widget">
        <div class="ac-w-encab">
          <span>Simulador</span><em>${cfg.titulo}</em>
        </div>
        <div class="ac-w-cuerpo">
          <div class="ac-w-controles">${cfg.controles}</div>
          <div class="ac-w-lienzo" data-lienzo></div>
          <div class="ac-w-lectura" data-lectura></div>
        </div>
        <div class="ac-w-pie">${cfg.pie}</div>
      </div>`;

    const estado = {};
    const sliders = nodo.querySelectorAll("[data-slider]");
    const checks = nodo.querySelectorAll("[data-check]");

    function leer() {
      sliders.forEach(s => { estado[s.dataset.slider] = parseFloat(s.value); });
      checks.forEach(c => { estado[c.dataset.check] = c.checked; });
      return estado;
    }
    function refrescar() {
      leer();
      sliders.forEach(s => {
        const b = s.closest(".ac-w-ctrl").querySelector("[data-valor]");
        if (b) b.textContent = cfg.etiquetaValor(s.dataset.slider, parseFloat(s.value));
      });
      cfg.dibujar(estado,
        nodo.querySelector("[data-lienzo]"),
        nodo.querySelector("[data-lectura]"));
    }
    sliders.forEach(s => s.addEventListener("input", refrescar));
    checks.forEach(c => c.addEventListener("change", refrescar));
    refrescar();
  }

  // Marco SVG con ejes
  function svg(ancho, alto, contenido) {
    return `<svg viewBox="0 0 ${ancho} ${alto}" preserveAspectRatio="xMidYMid meet"
                 role="img" aria-hidden="true">${contenido}</svg>`;
  }
  const eje = (x1, y1, x2, y2) =>
    `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="w-eje"/>`;
  const texto = (x, y, t, clase) =>
    `<text x="${x}" y="${y}" class="w-txt ${clase || ""}">${t}</text>`;

  function lectura(items) {
    return items.map(i =>
      `<div class="${i.alerta ? "alerta" : ""}"><dt>${i.k}</dt><dd>${i.v}</dd></div>`).join("");
  }

  /* =================================================================
     M01 — El horizonte cambia la tasa de incumplimiento
     ================================================================= */
  const wVentana = {
    titulo: "Ventana de desempeño",
    montar(nodo) {
      const r = azar(20260722);
      // Momento del incumplimiento de cada operación, en meses
      const meses = Array.from({ length: 4000 }, () => {
        const u = r();
        return u < 0.14 ? 1 + Math.floor(Math.abs(normal(r)) * 14) : 999;
      });
      armar(nodo, {
        titulo: this.titulo,
        controles: control({ nombre: "h", etiqueta: "Horizonte observado", min: 3, max: 36, valor: 12 }),
        etiquetaValor: (n, v) => v + " meses",
        dibujar(e, lienzo, lect) {
          const h = e.h;
          const tasa = meses.filter(m => m <= h).length / meses.length;
          const A = 620, B = 190;
          let barras = "";
          for (let m = 1; m <= 36; m++) {
            const n = meses.filter(x => x === m).length;
            const alto = (n / 90) * 130;
            barras += `<rect x="${20 + (m - 1) * 16.4}" y="${160 - alto}" width="13"
              height="${Math.max(alto, 0.5)}" class="${m <= h ? "w-barra-on" : "w-barra-off"}"/>`;
          }
          const xc = 20 + h * 16.4 - 1.5;
          lienzo.innerHTML = svg(A, B,
            barras +
            `<line x1="${xc}" y1="14" x2="${xc}" y2="162" class="w-corte"/>` +
            texto(xc + 5, 24, "corte", "w-corte-t") +
            eje(18, 162, 606, 162) +
            texto(20, 182, "mes 1") + texto(546, 182, "mes 36"));
          lect.innerHTML = lectura([
            { k: "Tasa de incumplimiento", v: pct(tasa, 2) },
            { k: "Operaciones malas", v: fmt(meses.filter(m => m <= h).length) },
            { k: "Aún sin madurar", v: fmt(meses.filter(m => m > h && m < 999).length),
              alerta: h < 12 }
          ]);
        },
        pie: "La misma cartera tiene tasas distintas según el horizonte. Un modelo a doce " +
             "meses y otro a veinticuatro no son comparables aunque midan lo mismo. Si la " +
             "ventana es corta, parte de los incumplimientos todavía no ocurrió."
      });
    }
  };

  /* =================================================================
     M02 — Cuántos tramos: el IV sube y los tramos se vacían
     ================================================================= */
  const wBinning = {
    titulo: "Tramos, WOE e information value",
    montar(nodo) {
      const r = azar(880123);
      const datos = Array.from({ length: 6000 }, () => {
        const x = clamp(30 + normal(r) * 18, 0, 96);          // antigüedad en meses
        const p = 1 / (1 + Math.exp((x - 26) / 9));           // más antiguo, mejor
        return { x: x, malo: r() < p * 0.30 ? 1 : 0 };
      }).sort((a, b) => a.x - b.x);

      armar(nodo, {
        titulo: this.titulo,
        controles: control({ nombre: "k", etiqueta: "Número de tramos", min: 2, max: 20, valor: 5 }) +
                   interruptor({ nombre: "opt", etiqueta: "Cortes automáticos por information value", valor: false }),
        etiquetaValor: (n, v) => v + " tramos",
        dibujar(e, lienzo, lect) {
          const k = e.k, n = datos.length, porTramo = Math.floor(n / k);
          // Dos formas de cortar: por cuantiles deja tramos parejos; el corte
          // automatico busca maximizar el IV y produce tramos muy desiguales.
          const min = datos[0].x, max = datos[n - 1].x;
          const grupo = i => {
            if (!e.opt) return datos.slice(i * porTramo, i === k - 1 ? n : (i + 1) * porTramo);
            const a = min + (max - min) * (i / k), b = min + (max - min) * ((i + 1) / k);
            return datos.filter(d => d.x >= a && (i === k - 1 ? d.x <= b : d.x < b));
          };
          const B = Math.max(1, datos.filter(d => !d.malo).length);
          const M = Math.max(1, datos.filter(d => d.malo).length);
          let iv = 0, chicos = 0, woes = [];
          for (let i = 0; i < k; i++) {
            const g = grupo(i);
            if (!g.length) { woes.push({ w: 0, part: 0 }); chicos++; continue; }
            const mal = g.filter(d => d.malo).length, bue = g.length - mal;
            const pb = (bue + 0.5) / (B + 0.5 * k), pm = (mal + 0.5) / (M + 0.5 * k);
            const w = Math.log(pb / pm);
            iv += (pb - pm) * w;
            woes.push({ w: w, part: g.length / n });
            if (g.length / n < 0.05) chicos++;
          }
          const A = 620, H = 190, cero = 100, ancho = 580 / k;
          let barras = woes.map((o, i) => {
            const alto = clamp(o.w * 42, -84, 84);
            return `<rect x="${22 + i * ancho + 2}" y="${alto > 0 ? cero - alto : cero}"
              width="${Math.max(ancho - 4, 2)}" height="${Math.abs(alto) || 1}"
              class="${o.part < 0.05 ? "w-barra-mal" : (o.w >= 0 ? "w-barra-on" : "w-barra-neg")}"/>`;
          }).join("");
          lienzo.innerHTML = svg(A, H,
            barras + eje(20, cero, 606, cero) +
            texto(22, 22, "WOE positivo: concentra buenos") +
            texto(22, 182, "WOE negativo: concentra malos"));
          lect.innerHTML = lectura([
            { k: "Information value", v: fmt(iv, 4), alerta: iv > 0.5 },
            { k: "Tramos bajo el 5 %", v: chicos, alerta: chicos > 0 },
            { k: "Lectura", v: iv < 0.02 ? "no aporta" : iv < 0.1 ? "débil"
                 : iv < 0.3 ? "aceptable" : iv < 0.5 ? "fuerte" : "sospechoso" }
          ]);
        },
        pie: "Con cortes por cuantiles los tramos quedan parejos. Activa los cortes " +
             "automáticos y sube el número de tramos: el information value mejora y al mismo " +
             "tiempo aparecen tramos en rojo, con menos del 5 % de la población. Ese es el " +
             "costo oculto del binning automático, y es lo que hay que pedir que justifiquen."
      });
    }
  };

  /* =================================================================
     M03 — Complejidad contra desempeño real
     ================================================================= */
  const wComplejidad = {
    titulo: "Complejidad del modelo y sobreajuste",
    montar(nodo) {
      armar(nodo, {
        titulo: this.titulo,
        controles: control({ nombre: "c", etiqueta: "Complejidad del modelo", min: 1, max: 20, valor: 4 }),
        etiquetaValor: (n, v) => "nivel " + v,
        dibujar(e, lienzo, lect) {
          const des = c => 0.70 + 0.29 * (1 - Math.exp(-c / 4.2));
          const val = c => 0.70 + 0.13 * (1 - Math.exp(-c / 3.0)) - 0.011 * Math.max(0, c - 6);
          const A = 620, H = 200, x = c => 30 + (c - 1) * 29, y = a => 178 - (a - 0.68) * 470;
          const linea = f => Array.from({ length: 20 }, (_, i) =>
            `${i ? "L" : "M"}${x(i + 1)},${y(f(i + 1))}`).join(" ");
          lienzo.innerHTML = svg(A, H,
            eje(28, 178, 606, 178) + eje(28, 12, 28, 178) +
            `<path d="${linea(des)}" class="w-linea-b"/>` +
            `<path d="${linea(val)}" class="w-linea-a"/>` +
            `<circle cx="${x(e.c)}" cy="${y(des(e.c))}" r="5" class="w-pto-b"/>` +
            `<circle cx="${x(e.c)}" cy="${y(val(e.c))}" r="5" class="w-pto-a"/>` +
            `<line x1="${x(e.c)}" y1="12" x2="${x(e.c)}" y2="178" class="w-corte"/>` +
            texto(36, 24, "desarrollo", "w-t-b") + texto(36, 40, "validación", "w-t-a") +
            texto(30, 194, "simple") + texto(556, 194, "complejo"));
          const brecha = des(e.c) - val(e.c);
          lect.innerHTML = lectura([
            { k: "AUC en desarrollo", v: fmt(des(e.c), 3) },
            { k: "AUC en validación", v: fmt(val(e.c), 3) },
            { k: "Brecha", v: fmt(brecha, 3), alerta: brecha > 0.05 }
          ]);
        },
        pie: "La curva de desarrollo nunca baja: por eso no sirve para decidir. La de " +
             "validación sube, se estanca y empieza a caer. Cuando la brecha pasa de cinco " +
             "puntos, el modelo está aprendiendo su propia muestra."
      });
    }
  };

  /* =================================================================
     M04 — Estandarizar o no estandarizar
     ================================================================= */
  const wSegmentos = {
    titulo: "Segmentación y escala de las variables",
    montar(nodo) {
      const r = azar(4477);
      // monto en millones, antigüedad en meses: escalas muy distintas
      const puntos = [];
      [[8, 12], [8, 46], [34, 14], [34, 48]].forEach(c => {
        for (let i = 0; i < 45; i++)
          puntos.push({ m: c[0] + normal(r) * 5, a: c[1] + normal(r) * 6 });
      });

      function kmedias(pts, k, estandarizar) {
        const em = estandarizar ? 1 / 13 : 1 / 13, ea = estandarizar ? 1 / 16 : 1 / 400;
        const cen = Array.from({ length: k }, (_, i) => ({
          m: pts[i * 37 % pts.length].m, a: pts[i * 53 % pts.length].a }));
        let asig = [];
        for (let it = 0; it < 25; it++) {
          asig = pts.map(p => {
            let mej = 0, d0 = Infinity;
            cen.forEach((c, j) => {
              const d = Math.pow((p.m - c.m) * em, 2) + Math.pow((p.a - c.a) * ea, 2);
              if (d < d0) { d0 = d; mej = j; }
            });
            return mej;
          });
          cen.forEach((c, j) => {
            const g = pts.filter((_, i) => asig[i] === j);
            if (g.length) {
              c.m = g.reduce((s, p) => s + p.m, 0) / g.length;
              c.a = g.reduce((s, p) => s + p.a, 0) / g.length;
            }
          });
        }
        return asig;
      }

      armar(nodo, {
        titulo: this.titulo,
        controles: control({ nombre: "k", etiqueta: "Número de grupos", min: 2, max: 6, valor: 4 }) +
                   interruptor({ nombre: "std", etiqueta: "Estandarizar las variables", valor: false }),
        etiquetaValor: (n, v) => "k = " + v,
        dibujar(e, lienzo, lect) {
          const asig = kmedias(puntos, e.k, e.std);
          const A = 620, H = 210;
          const px = p => 40 + (p.m / 46) * 550, py = p => 180 - (p.a / 62) * 160;
          const circulos = puntos.map((p, i) =>
            `<circle cx="${px(p).toFixed(1)}" cy="${py(p).toFixed(1)}" r="3.6"
              class="w-c${asig[i] % 6}"/>`).join("");
          lienzo.innerHTML = svg(A, H,
            circulos + eje(36, 182, 600, 182) + eje(36, 10, 36, 182) +
            texto(300, 202, "monto del crédito") +
            `<text x="14" y="100" class="w-txt" transform="rotate(-90 14 100)">antigüedad</text>`);
          // ¿los grupos se separan por monto o por antigüedad?
          const gs = Array.from({ length: e.k }, (_, j) => puntos.filter((_, i) => asig[i] === j));
          const varM = gs.map(g => g.length ? g.reduce((s, p) => s + p.m, 0) / g.length : 0);
          const varA = gs.map(g => g.length ? g.reduce((s, p) => s + p.a, 0) / g.length : 0);
          const disp = v => Math.max(...v) - Math.min(...v);
          const domina = disp(varM) / 46 > disp(varA) / 62 * 1.6;
          lect.innerHTML = lectura([
            { k: "Variables", v: e.std ? "estandarizadas" : "en su escala original" },
            { k: "Los grupos se separan por", v: domina ? "el monto, casi solo" : "ambas variables" },
            { k: "Diagnóstico", v: domina ? "la escala manda sobre el comportamiento" : "segmentación razonable",
              alerta: domina }
          ]);
        },
        pie: "Con las variables sin estandarizar, el monto absorbe toda la distancia y los " +
             "cortes salen verticales: la antigüedad deja de importar. Activa la casilla y " +
             "mira cómo se reordenan los grupos con exactamente los mismos datos."
      });
    }
  };

  /* =================================================================
     M05 — Punto de corte y costo de los dos errores
     ================================================================= */
  const wCorte = {
    titulo: "Punto de corte, matriz de confusión y costo",
    montar(nodo) {
      const r = azar(9091);
      const pob = Array.from({ length: 5000 }, () => {
        const malo = r() < 0.08;
        const s = clamp(malo ? 0.34 + normal(r) * 0.16 : 0.10 + normal(r) * 0.09, 0.001, 0.999);
        return { malo: malo, p: s };
      });

      armar(nodo, {
        titulo: this.titulo,
        controles:
          control({ nombre: "c", etiqueta: "Punto de corte", min: 1, max: 60, valor: 20 }) +
          control({ nombre: "rel", etiqueta: "Pérdida frente al margen", min: 2, max: 25, valor: 8 }),
        etiquetaValor: (n, v) => n === "c" ? v + " %" : v + " veces",
        dibujar(e, lienzo, lect) {
          const c = e.c / 100;
          const VP = pob.filter(o => o.malo && o.p >= c).length;
          const FN = pob.filter(o => o.malo && o.p < c).length;
          const FP = pob.filter(o => !o.malo && o.p >= c).length;
          const VN = pob.filter(o => !o.malo && o.p < c).length;
          const costo = k => pob.filter(o => o.malo && o.p < k).length * e.rel +
                             pob.filter(o => !o.malo && o.p >= k).length;
          let mejor = 0.01, cm = Infinity;
          for (let k = 0.01; k <= 0.60; k += 0.01) { const v = costo(k); if (v < cm) { cm = v; mejor = k; } }

          const A = 620, H = 200;
          const hist = (filtro, clase) => {
            let s = "";
            for (let i = 0; i < 60; i++) {
              const n = pob.filter(o => filtro(o) && o.p >= i / 100 && o.p < (i + 1) / 100).length;
              if (n) s += `<rect x="${24 + i * 9.6}" y="${170 - n / 2.2}" width="8.4"
                height="${n / 2.2}" class="${clase}"/>`;
            }
            return s;
          };
          const xc = 24 + e.c * 9.6, xo = 24 + mejor * 100 * 9.6;
          lienzo.innerHTML = svg(A, H,
            hist(o => !o.malo, "w-hist-b") + hist(o => o.malo, "w-hist-m") +
            eje(22, 172, 606, 172) +
            `<line x1="${xo}" y1="16" x2="${xo}" y2="172" class="w-optimo"/>` +
            `<line x1="${xc}" y1="10" x2="${xc}" y2="172" class="w-corte"/>` +
            texto(28, 24, "no incumplen", "w-t-b") + texto(28, 40, "incumplen", "w-t-a") +
            texto(xo - 18, 192, "óptimo", "w-optimo-t"));
          lect.innerHTML = lectura([
            { k: "Rechazados que habrían pagado", v: fmt(FP) },
            { k: "Aprobados que incumplieron", v: fmt(FN), alerta: FN > VP },
            { k: "Costo total del corte", v: fmt(costo(c)) },
            { k: "Corte de mínimo costo", v: pct(mejor, 0), alerta: Math.abs(mejor - c) > 0.03 }
          ]);
        },
        pie: "Mueve el corte y observa que el mínimo costo casi nunca está en 50 %. Sube la " +
             "razón entre pérdida y margen: cuanto más cuesta un crédito que no se paga, más " +
             "hacia la izquierda se va el corte óptimo."
      });
    }
  };

  /* =================================================================
     M06 — Cuánto desplazamiento hace falta para cruzar 0,25
     ================================================================= */
  const wPsi = {
    titulo: "Índice de estabilidad poblacional",
    montar(nodo) {
      const base = [0.06, 0.11, 0.17, 0.22, 0.19, 0.14, 0.08, 0.03];
      armar(nodo, {
        titulo: this.titulo,
        controles:
          control({ nombre: "d", etiqueta: "Desplazamiento de la población", min: -30, max: 30, valor: 0 }) +
          control({ nombre: "e", etiqueta: "Concentración", min: -20, max: 30, valor: 0 }),
        etiquetaValor: (n, v) => (v > 0 ? "+" : "") + v,
        dibujar(e, lienzo, lect) {
          const n = base.length, centro = (n - 1) / 2;
          let act = base.map((p, i) => {
            const mov = 1 + (e.d / 100) * (i - centro);
            const con = 1 + (e.e / 100) * (1 - Math.abs(i - centro) / centro);
            return Math.max(p * mov * con, 0.001);
          });
          const s = act.reduce((a, b) => a + b, 0);
          act = act.map(v => v / s);

          let psi = 0, aportes = [];
          act.forEach((a, i) => {
            const ap = (a - base[i]) * Math.log(a / base[i]);
            psi += ap; aportes.push(ap);
          });

          const A = 620, H = 190, w = 66;
          let barras = "";
          base.forEach((b, i) => {
            const x = 30 + i * w;
            barras += `<rect x="${x}" y="${168 - b * 480}" width="26" height="${b * 480}" class="w-barra-ref"/>`;
            barras += `<rect x="${x + 28}" y="${168 - act[i] * 480}" width="26"
              height="${act[i] * 480}" class="${aportes[i] > 0.02 ? "w-barra-mal" : "w-barra-on"}"/>`;
          });
          lienzo.innerHTML = svg(A, H,
            barras + eje(26, 168, 606, 168) +
            texto(30, 22, "construcción", "w-t-ref") + texto(30, 38, "período actual", "w-t-a") +
            texto(30, 186, "puntaje bajo") + texto(520, 186, "puntaje alto"));
          const est = psi < 0.10 ? "población estable" : psi < 0.25
            ? "desplazamiento moderado: analizar" : "desplazamiento relevante: revisar el modelo";
          lect.innerHTML = lectura([
            { k: "PSI", v: fmt(psi, 4), alerta: psi >= 0.25 },
            { k: "Diagnóstico", v: est, alerta: psi >= 0.25 },
            { k: "Tramos con aporte alto", v: aportes.filter(a => a > 0.02).length,
              alerta: aportes.filter(a => a > 0.02).length > 0 }
          ]);
        },
        pie: "Prueba a mover la población hacia un lado y luego a concentrarla en el centro. " +
             "Fíjate en algo incómodo: se pueden tener dos tramos claramente distintos y un " +
             "PSI total todavía bajo, porque los movimientos se compensan."
      });
    }
  };

  /* =================================================================
     M07 — Los tres parámetros pesan igual
     ================================================================= */
  const wProvision = {
    titulo: "Pérdida esperada y sus tres parámetros",
    montar(nodo) {
      const EXPOSICION = 4200000000;
      armar(nodo, {
        titulo: this.titulo,
        controles:
          control({ nombre: "pd", etiqueta: "PD", min: 5, max: 150, valor: 32, paso: 1 }) +
          control({ nombre: "lgd", etiqueta: "LGD", min: 10, max: 90, valor: 45 }) +
          control({ nombre: "cf", etiqueta: "Factor de conversión del contingente", min: 0, max: 100, valor: 40 }),
        etiquetaValor: (n, v) => n === "pd" ? fmt(v / 10, 1) + " %" : v + " %",
        dibujar(e, lienzo, lect) {
          const pd = e.pd / 1000, lgd = e.lgd / 100;
          const ead = EXPOSICION * (1 + 0.22 * (e.cf / 100));
          const prov = pd * lgd * ead;
          const baseProv = 0.032 * 0.45 * EXPOSICION * 1.088;

          const A = 620, H = 150;
          const barra = (y, etq, frac, clase) =>
            `<rect x="150" y="${y}" width="${clamp(frac, 0, 1) * 430}" height="24" class="${clase}"/>` +
            texto(20, y + 17, etq);
          lienzo.innerHTML = svg(A, H,
            barra(16, "PD", pd / 0.15, "w-barra-on") +
            barra(52, "LGD", lgd, "w-barra-on") +
            barra(88, "EAD", ead / (EXPOSICION * 1.25), "w-barra-on") +
            `<rect x="150" y="120" width="${clamp(prov / (baseProv * 3), 0, 1) * 430}"
               height="24" class="w-barra-tot"/>` + texto(20, 137, "Provisión"));
          const var_ = prov / baseProv - 1;
          lect.innerHTML = lectura([
            { k: "Provisión", v: "$ " + fmt(prov) },
            { k: "Cobertura de la exposición", v: pct(prov / ead, 2) },
            { k: "Variación contra el cierre", v: (var_ > 0 ? "+" : "") + pct(var_, 1),
              alerta: Math.abs(var_) > 0.15 }
          ]);
        },
        pie: "Baja la PD un 10 % y anótalo. Ahora devuélvela y baja la LGD un 10 %. El efecto " +
             "sobre la provisión es idéntico, porque es un producto. Por eso revisar solo el " +
             "modelo de PD deja fuera la mitad del riesgo."
      });
    }
  };

  /* =================================================================
     M08 — La correlación engorda la cola
     ================================================================= */
  const wPerdidas = {
    titulo: "Distribución de pérdidas, VaR y capital",
    montar(nodo) {
      armar(nodo, {
        titulo: this.titulo,
        controles:
          control({ nombre: "rho", etiqueta: "Correlación entre incumplimientos", min: 0, max: 40, valor: 0 }) +
          control({ nombre: "conf", etiqueta: "Nivel de confianza", min: 90, max: 999, valor: 990, paso: 1 }),
        etiquetaValor: (n, v) => n === "rho" ? fmt(v / 100, 2) : fmt(v / 10, 1) + " %",
        dibujar(e, lienzo, lect) {
          const rho = e.rho / 100, conf = e.conf / 1000;
          const r = azar(30303);
          const N = 6000, pd = 0.032, lgd = 0.45, exp_ = 4200000000;
          const perd = new Array(N);
          for (let i = 0; i < N; i++) {
            const shock = normal(r);
            // Modelo de factor único: un shock común mueve a toda la cartera a la vez
            const z = Math.sqrt(rho) * shock + Math.sqrt(1 - rho) * normal(r);
            const tasa = clamp(pd * Math.exp(z * (0.35 + rho * 1.6) - 0.06), 0, 0.6);
            perd[i] = tasa * lgd * exp_;
          }
          perd.sort((a, b) => a - b);
          const media = perd.reduce((a, b) => a + b, 0) / N;
          const varq = perd[Math.min(N - 1, Math.floor(conf * N))];
          const tope = perd[N - 1] * 1.02;

          const A = 620, H = 190, bins = 44;
          let hist = "";
          const cuenta = new Array(bins).fill(0);
          perd.forEach(p => cuenta[Math.min(bins - 1, Math.floor(p / tope * bins))]++);
          const maxc = Math.max(...cuenta);
          cuenta.forEach((c, i) => {
            const x = 24 + i * 13, alto = (c / maxc) * 140;
            const val = (i + 0.5) / bins * tope;
            hist += `<rect x="${x}" y="${164 - alto}" width="11.5" height="${alto || 0.5}"
              class="${val >= varq ? "w-barra-mal" : "w-barra-on"}"/>`;
          });
          const xm = 24 + (media / tope) * bins * 13, xv = 24 + (varq / tope) * bins * 13;
          lienzo.innerHTML = svg(A, H,
            hist + eje(22, 166, 606, 166) +
            `<line x1="${xm}" y1="14" x2="${xm}" y2="166" class="w-optimo"/>` +
            `<line x1="${xv}" y1="14" x2="${xv}" y2="166" class="w-corte"/>` +
            texto(xm + 5, 26, "esperada → provisión", "w-optimo-t") +
            texto(clamp(xv - 150, 24, 420), 46, "VaR → capital", "w-corte-t"));
          lect.innerHTML = lectura([
            { k: "Pérdida esperada", v: "$ " + fmt(media) },
            { k: "VaR al " + fmt(conf * 100, 1) + " %", v: "$ " + fmt(varq) },
            { k: "Pérdida inesperada", v: "$ " + fmt(varq - media) },
            { k: "Capital sobre la media", v: fmt((varq - media) / media, 2) + " veces",
              alerta: (varq - media) / media > 1.5 }
          ]);
        },
        pie: "Con correlación cero, la distribución es estrecha y el capital exigido es " +
             "modesto. Súbela a 0,20 y observa: la pérdida esperada casi no se mueve, pero la " +
             "cola se estira y el capital se multiplica. Ese supuesto no se ve en ningún dato " +
             "observado y decide la cifra."
      });
    }
  };

  /* ---------- Registro y montaje ----------------------------------- */

  const REGISTRO = {
    ventana: wVentana, binning: wBinning, complejidad: wComplejidad,
    segmentos: wSegmentos, corte: wCorte, psi: wPsi,
    provision: wProvision, perdidas: wPerdidas
  };

  global.ACWidgets = {
    registro: REGISTRO,
    montarTodos(raiz) {
      (raiz || document).querySelectorAll("[data-widget]").forEach(n => {
        const w = REGISTRO[n.dataset.widget];
        if (!w) { n.innerHTML = '<p class="ac-riesgo">Simulador no disponible.</p>'; return; }
        try { w.montar(n); }
        catch (err) {
          n.innerHTML = '<p class="ac-riesgo">No se pudo cargar el simulador.</p>';
          if (global.console) console.error("Widget", n.dataset.widget, err);
        }
      });
    }
  };
})(window);
