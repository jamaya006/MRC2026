/* ===================================================================
   AuditCaat's — Catalogo del programa
   Fuente unica de verdad de la malla. El portal, el motor y los
   certificados leen de aqui. Para agregar o reordenar modulos se
   edita solo este archivo.

   marca:  simbolo de auditoria que se estampa al aprobar el modulo
   ref:    referencia de legajo (columna izquierda del indice)
   clase:  transcripcion de origen, para trazabilidad del contenido
   =================================================================== */

const AC_PROGRAMA = {
  codigo: "MRC-2026",
  titulo: "Validación de modelos de riesgo de crédito para auditores y contadores",
  emisor: "AuditCaat's Data Assurance",
  anio: 2026,
  horasTotales: 21,
  entorno: "Python 3.11 · pandas · numpy · scikit-learn",
  aprobacionMinima: 0.70,   // 70% del puntaje del modulo
  modulos: [
    {
      id: "M01", ref: "A", marca: "✓", horas: 2.5, clase: "Clase 1",
      titulo: "Por qué un contador audita modelos",
      resumen: "Ciclo del crédito, ventanas de observación y desempeño, tipos de modelo y qué significa que un modelo esté mal.",
      entregable: "Programa de entendimiento del modelo",
      estadoPublicacion: "publicado",
      url: "modulos/m01.html",
      congelado: true   // hay certificados emitidos: quien ya lo aprobó puede convalidarlo
    },
    {
      id: "M02", ref: "B", marca: "Δ", horas: 3.0, clase: "Clase 2",
      titulo: "De la variable al scorecard",
      resumen: "WOE, information value, binning, regresión logística, construcción del scorecard, sobreajuste y regularización.",
      entregable: "Cédula de revisión de variables y binning",
      estadoPublicacion: "publicado",
      url: "modulos/m02.html"
    },
    {
      id: "M03", ref: "C", marca: "○", horas: 2.5, clase: "Clases 2 y 5",
      titulo: "Modelos alternativos y criterio de aceptación",
      resumen: "Árboles, bagging, boosting. Cuándo un modelo más complejo se justifica y cuándo es un riesgo de auditoría.",
      entregable: "Matriz comparativa de modelos candidatos",
      estadoPublicacion: "publicado",
      url: "modulos/m03.html"
    },
    {
      id: "M04", ref: "D", marca: "×", horas: 2.5, clase: "Clase 4",
      titulo: "Segmentación y sus riesgos",
      resumen: "Cluster y k-means, criterios de corte, cómo una segmentación mal construida contamina la provisión.",
      entregable: "Matriz de riesgos de segmentación",
      estadoPublicacion: "publicado",
      url: "modulos/m04.html"
    },
    {
      id: "M05", ref: "E", marca: "≡", horas: 3.0, clase: "Clases 3 y 5",
      titulo: "Desempeño y evidencia gráfica",
      resumen: "ROC, Gini, KS, divergencia, matriz de confusión y punto de corte. Lectura de gráficos de contorno y tablas de percentiles.",
      entregable: "Cédula de desempeño del modelo",
      estadoPublicacion: "publicado",
      url: "modulos/m05.html"
    },
    {
      id: "M06", ref: "F", marca: "≠", horas: 2.5, clase: "Clase 3",
      titulo: "Estabilidad y validación fuera de tiempo",
      resumen: "PSI, CSI, deterioro fuera de muestra y fuera de tiempo. El módulo con mayor uso en encargos reales.",
      entregable: "Plantilla de monitoreo con PSI",
      estadoPublicacion: "publicado",
      url: "modulos/m06.html"
    },
    {
      id: "M07", ref: "G", marca: "∫", horas: 2.5, clase: "Clases 6 y 7",
      titulo: "Pérdida esperada y provisión NIIF 9",
      resumen: "Stages, PD, LGD y EAD. Del parámetro estadístico al asiento contable y a la revelación.",
      entregable: "Hoja de recálculo de provisión",
      estadoPublicacion: "publicado",
      url: "modulos/m07.html"
    },
    {
      id: "M08", ref: "H", marca: "§", horas: 2.5, clase: "Clase 8",
      titulo: "Pérdida inesperada, capital y stress test",
      resumen: "Capital económico, pruebas de tensión y cierre del programa con el memorando de validación independiente.",
      entregable: "Memorando de validación independiente",
      estadoPublicacion: "publicado",
      url: "modulos/m08.html"
    }
  ]
};

/* ---------------------------------------------------------------
   Backend. Reemplazar por la URL del despliegue vigente de Apps
   Script. Usar SIEMPRE "Nueva version" sobre el mismo despliegue;
   crear un despliegue nuevo cambia la URL y rompe la verificacion
   de los certificados ya emitidos.
   --------------------------------------------------------------- */
const AC_BACKEND = "";  // ej: https://script.google.com/a/macros/auditcaats.com/s/XXXX/exec
