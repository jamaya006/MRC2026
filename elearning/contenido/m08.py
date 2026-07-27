# -*- coding: utf-8 -*-
"""Modulo VIII — Perdida inesperada, capital y stress test. Fuente: Clase 8."""

MODULO = {
    "ref": "H",
    "titulo": "Pérdida inesperada, capital y stress test",
    "proposito": "Cerrar el programa distinguiendo lo que se provisiona de lo que se cubre con "
                 "capital, y consolidar los hallazgos de los ocho módulos en un memorando de "
                 "validación independiente.",

    "cedulas": [
        {
            "ref": "H-1",
            "titulo": "Dos pérdidas distintas y dos respuestas distintas",
            "bloques": [
                ("p", "La pérdida de una cartera no es un número: es una distribución. La pérdida "
                      "esperada es su valor medio. La pérdida inesperada es lo que puede ocurrir "
                      "por sobre ese promedio en un escenario desfavorable."),
                ("cita", "Aparece el concepto de pérdida inesperada, que tiene que ver con todo lo "
                         "que está a la derecha de la pérdida media o de la pérdida esperada.",
                 "Clase 8, aprox. 01:54:08"),
                ("tabla", [
                    ["Concepto", "Qué representa", "Cómo se cubre", "Dónde aparece"],
                    ["Pérdida esperada", "Valor medio de la distribución", "Provisión", "Resultado y balance"],
                    ["Pérdida inesperada", "Desviación adversa sobre la media", "Capital", "Patrimonio y requerimientos"],
                ]),
                ("nota", "Por qué importa la distinción",
                 "Provisionar la pérdida inesperada o pretender cubrir la esperada con capital son "
                 "errores conceptuales con efecto contable. La primera es un gasto del ejercicio; "
                 "la segunda es una exigencia patrimonial."),
            ],
        },
        {
            "ref": "H-2",
            "titulo": "Frecuencia, severidad y valor en riesgo",
            "bloques": [
                ("p", "Para construir la distribución de pérdidas se modelan dos componentes por "
                      "separado: con qué frecuencia ocurren los incumplimientos y de qué magnitud "
                      "es la pérdida cuando ocurren."),
                ("cita", "Se van ajustando cuáles son las mejores distribuciones en términos de "
                         "frecuencia y severidad, y ahí uno compara el valor en riesgo y define cuál "
                         "es la que mejor se ajusta en base a múltiples indicadores.",
                 "Clase 8, aprox. 02:36:37"),
                ("p", "El valor en riesgo es el percentil de esa distribución para un nivel de "
                      "confianza dado. Decir que el valor en riesgo al 99 % es un monto determinado "
                      "significa que, bajo los supuestos del modelo, se espera superar esa pérdida "
                      "en uno de cada cien períodos."),
                ("riesgo", "Qué sale mal",
                 "El resultado depende por completo de la distribución elegida y de la correlación "
                 "supuesta entre incumplimientos. Cambiar el supuesto de correlación altera el "
                 "percentil de forma sustancial sin que cambie ningún dato observado."),
                ("nota", "Procedimiento",
                 "Solicitar el criterio de selección de las distribuciones, las pruebas de bondad de "
                 "ajuste consideradas y el supuesto de correlación. Verificar que el supuesto se "
                 "mantiene entre períodos o que su cambio está fundamentado."),
            ],
        },
        {
            "ref": "H-3",
            "titulo": "Stress test: qué es y qué no es",
            "bloques": [
                ("p", "Una prueba de tensión proyecta el comportamiento de la cartera bajo "
                      "condiciones adversas definidas. No es una predicción: es una medición de "
                      "sensibilidad ante un escenario que se supone posible."),
                ("cita", "El concepto de stress test de riesgo de crédito busca pronosticar "
                         "escenarios futuros, obviamente escenarios de estrés, condiciones adversas.",
                 "Clase 8, aprox. 02:47:21"),
                ("pasos", [
                    "Definir el escenario adverso y sus variables macroeconómicas.",
                    "Traducir esas variables a efectos sobre los parámetros de riesgo.",
                    "Recalcular la pérdida esperada y la inesperada bajo el escenario.",
                    "Evaluar el efecto sobre resultados, provisiones y suficiencia de capital.",
                    "Documentar las acciones de mitigación disponibles.",
                ]),
                ("riesgo", "Qué sale mal",
                 "El escenario adverso es más benigno que la peor situación efectivamente observada "
                 "en la historia de la institución. Una prueba de tensión que no tensiona no "
                 "informa nada, y consume recursos que aparentan cumplimiento."),
                ("nota", "Procedimiento",
                 "Contrastar los supuestos del escenario adverso contra los valores efectivamente "
                 "observados en las últimas crisis relevantes. Si el escenario adverso es menos "
                 "severo que lo ya ocurrido, corresponde observación."),
            ],
        },
        {
            "ref": "H-4",
            "titulo": "Castigo, recupero y presupuesto de riesgo",
            "bloques": [
                ("p", "Cuando una operación se considera irrecuperable se castiga: sale del activo "
                      "contra la provisión constituida. La gestión posterior puede recuperar parte "
                      "de ese monto, y ese recupero se reconoce cuando ocurre."),
                ("cita", "El presupuesto es el gasto en riesgo más el castigo neto de recupero.",
                 "Clase 8, aprox. 03:09:13"),
                ("p", "El momento del castigo es una decisión con efecto sobre la cifra. Adelantarlo "
                      "reduce la cartera bruta y consume provisión; postergarlo mantiene en el "
                      "activo operaciones sin capacidad de recuperación."),
                ("riesgo", "Qué sale mal",
                 "La política de castigo no está formalizada o admite excepciones sin aprobación "
                 "documentada. El castigo pasa a ser una herramienta de administración de "
                 "indicadores en lugar del reconocimiento de un hecho económico."),
                ("nota", "Procedimiento",
                 "Obtener la política de castigo, verificar su aplicación sobre una muestra y "
                 "revisar las excepciones del período con su aprobación. Contrastar la antigüedad "
                 "de la mora al momento del castigo contra el criterio declarado."),
            ],
        },
        {
            "ref": "H-5",
            "titulo": "El memorando de validación independiente",
            "bloques": [
                ("p", "El cierre del programa es el documento que consolida el trabajo: qué se "
                      "revisó, con qué alcance, qué se encontró y qué efecto tiene sobre la cifra. "
                      "Es el entregable que da valor al resto de los papeles de trabajo."),
                ("tabla", [
                    ["Sección", "Contenido", "Módulo que la alimenta"],
                    ["Alcance y limitaciones", "Qué se revisó y qué no, y por qué", "I y III"],
                    ["Datos y variables", "Calidad, fuga de información, binning", "II"],
                    ["Segmentación", "Criterio, estabilidad, efecto en parámetros", "IV"],
                    ["Desempeño", "Discriminación y calibración", "V"],
                    ["Estabilidad", "PSI, fuera de tiempo, monitoreo", "VI"],
                    ["Provisión", "Recálculo y conciliación", "VII"],
                    ["Capital y tensión", "Supuestos y severidad de escenarios", "VIII"],
                    ["Hallazgos y efecto", "Clasificados por severidad y efecto en la cifra", "Todos"],
                ]),
                ("umbral", "Regla de redacción de hallazgos",
                 "Cada hallazgo declara la condición observada, el criterio contra el que se "
                 "compara, la causa, el efecto cuantificado cuando es posible y la recomendación. "
                 "Un hallazgo sin criterio explícito es una opinión."),
                ("nota", "Independencia",
                 "La validación debe ser realizada por alguien distinto de quien construyó el "
                 "modelo, con acceso a los datos y a la documentación, y con capacidad de reportar "
                 "a un nivel distinto del área de riesgo. Sin las tres condiciones, la revisión "
                 "puede ser técnicamente correcta y no constituir validación independiente."),
            ],
        },
    ],

    "banco": [
        {"id": "h1", "puntaje": 10,
         "texto": "¿Cuál es la diferencia entre pérdida esperada e inesperada?",
         "opciones": [
             {"txt": "La esperada es el valor medio de la distribución y se provisiona; la "
                     "inesperada es la desviación adversa y se cubre con capital", "ok": True},
             {"txt": "La inesperada corresponde a fraudes y la esperada a incumplimientos"},
             {"txt": "La esperada es de corto plazo y la inesperada de largo plazo"},
             {"txt": "Ambas se provisionan, con distinto horizonte"},
         ],
         "retro": "Son respuestas distintas a partes distintas de la misma distribución: provisión "
                  "para la media, capital para la cola."},

        {"id": "h2", "puntaje": 10,
         "texto": "¿Qué significa un valor en riesgo al 99 % de un monto determinado?",
         "opciones": [
             {"txt": "Que bajo los supuestos del modelo se espera superar esa pérdida en uno de cada "
                     "cien períodos", "ok": True},
             {"txt": "Que la pérdida máxima posible es ese monto"},
             {"txt": "Que el 99 % de los clientes no incumplirá"},
             {"txt": "Que la provisión debe igualar ese monto"},
         ],
         "retro": "Es un percentil bajo supuestos, no un techo. La pérdida puede superarlo, y ese "
                  "es precisamente el 1 % restante."},

        {"id": "h3", "puntaje": 10,
         "texto": "¿Qué supuesto altera el resultado del valor en riesgo sin que cambie ningún dato "
                  "observado?",
         "opciones": [
             {"txt": "La correlación supuesta entre incumplimientos", "ok": True},
             {"txt": "El número de operaciones de la cartera"},
             {"txt": "La tasa de interés de colocación"},
             {"txt": "El nivel de provisión constituido"},
         ],
         "retro": "La correlación determina la forma de la cola de la distribución. Cambiarla mueve "
                  "el percentil sin que nada observable cambie."},

        {"id": "h4", "puntaje": 10,
         "texto": "El escenario adverso del stress test es menos severo que la peor crisis observada "
                  "por la institución. ¿Qué corresponde?",
         "opciones": [
             {"txt": "Observación: una prueba de tensión que no tensiona no informa sobre la "
                     "resistencia real", "ok": True},
             {"txt": "Aceptarlo si el escenario fue aprobado por el directorio"},
             {"txt": "Aceptarlo si la metodología sigue estándares de mercado"},
             {"txt": "No aplica observación porque el escenario es hipotético"},
         ],
         "retro": "El referente mínimo de severidad es lo efectivamente ocurrido. Un escenario más "
                  "benigno genera cumplimiento aparente."},

        {"id": "h5", "puntaje": 10,
         "texto": "¿Qué ocurre contablemente cuando se castiga una operación?",
         "opciones": [
             {"txt": "Sale del activo contra la provisión constituida, y el recupero posterior se "
                     "reconoce cuando ocurre", "ok": True},
             {"txt": "Se reconoce un gasto adicional por el monto total"},
             {"txt": "Se traslada a etapa 2"},
             {"txt": "Se reversa la provisión contra resultados"},
         ],
         "retro": "El castigo usa la provisión ya constituida. Si la provisión era insuficiente, la "
                  "diferencia sí golpea resultados."},

        {"id": "h6", "puntaje": 10,
         "texto": "La política de castigo admite excepciones sin aprobación documentada. ¿Cuál es el "
                  "riesgo?",
         "opciones": [
             {"txt": "El castigo se transforma en herramienta de administración de indicadores en "
                     "lugar de reconocimiento de un hecho económico", "ok": True},
             {"txt": "Se incumple el plazo legal de prescripción"},
             {"txt": "Se pierde el derecho a cobrar la operación"},
             {"txt": "Aumenta la provisión del período siguiente"},
         ],
         "retro": "Adelantar o postergar el castigo mueve cartera bruta, mora e indicadores. Sin "
                  "regla formal, esa decisión queda a discreción."},

        {"id": "h7", "puntaje": 10,
         "texto": "¿Qué condiciones debe cumplir una revisión para constituir validación "
                  "independiente?",
         "opciones": [
             {"txt": "Ser realizada por alguien distinto del constructor, con acceso a datos y "
                     "documentación, y con reporte a un nivel distinto del área de riesgo", "ok": True},
             {"txt": "Ser realizada por un tercero externo a la institución"},
             {"txt": "Aplicar las mismas métricas que usó el equipo de desarrollo"},
             {"txt": "Contar con la aprobación del área de riesgo"},
         ],
         "retro": "La independencia es orgánica y de acceso. Una revisión que reporta al área que "
                  "construyó el modelo no es independiente, aunque sea técnicamente correcta."},

        {"id": "h8", "puntaje": 10,
         "texto": "¿Qué elemento convierte una observación en un hallazgo de auditoría?",
         "opciones": [
             {"txt": "La existencia de un criterio explícito contra el cual se compara la condición "
                     "observada", "ok": True},
             {"txt": "Que el efecto supere la materialidad"},
             {"txt": "Que el auditado esté de acuerdo"},
             {"txt": "Que exista una recomendación asociada"},
         ],
         "retro": "Sin criterio explícito hay una opinión. Condición, criterio, causa, efecto y "
                  "recomendación son la estructura completa."},

        {"id": "h9", "puntaje": 10,
         "texto": "El presupuesto de riesgo se compone de:",
         "opciones": [
             {"txt": "El gasto en riesgo más el castigo neto de recupero", "ok": True},
             {"txt": "La provisión constituida más el capital regulatorio"},
             {"txt": "La pérdida esperada más la inesperada"},
             {"txt": "El valor en riesgo al 99 %"},
         ],
         "retro": "Es una definición de gestión, no un cálculo de modelo. Sirve para contrastar lo "
                  "presupuestado contra lo efectivamente ocurrido."},

        {"id": "h10", "puntaje": 10,
         "texto": "¿Qué hallazgo del programa tiene efecto más directo sobre la cifra de provisión "
                  "del estado financiero?",
         "opciones": [
             {"txt": "Un desvío sistemático entre PD estimada e incumplimiento observado por tramo", "ok": True},
             {"txt": "La falta de registro de la semilla aleatoria del modelo"},
             {"txt": "El uso de un algoritmo poco interpretable"},
             {"txt": "La ausencia de gráfico de silueta en la segmentación"},
         ],
         "retro": "Los otros tres son deficiencias reales de gobierno y metodología. Solo el desvío "
                  "de calibración se traduce directamente en una provisión mal dimensionada."},
    ],
}
