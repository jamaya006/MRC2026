# -*- coding: utf-8 -*-
"""Modulo I — Por que un contador audita modelos. Fuente: Clase 1."""

MODULO = {
    "ref": "A",
    "titulo": "Por qué un contador audita modelos",
    "proposito": "Situar el modelo como fuente de una cifra de los estados financieros y no como "
                 "un asunto técnico del área de riesgo. Al terminar, distinguir los tres tipos de "
                 "modelo, leer una ventana de observación y saber qué significa que un modelo esté "
                 "mal.",

    "cedulas": [
        {
            "ref": "A-1",
            "titulo": "De la pérdida incurrida a la pérdida esperada",
            "bloques": [
                ("p", "Durante décadas la provisión se reconocía cuando existía evidencia objetiva "
                      "de deterioro: el cliente había dejado de pagar. El marco actual invierte el "
                      "orden. La pérdida se estima desde el origen del crédito, antes de que ocurra "
                      "el incumplimiento."),
                ("p", "El cambio tiene una consecuencia práctica para quien audita: la provisión "
                      "dejó de ser el resultado de una regla verificable línea por línea y pasó a "
                      "ser una estimación producida por un modelo. Ya no se recalcula la cifra: se "
                      "evalúa el proceso que la produce."),
                ("nota", "Regla de trabajo del programa",
                 "Ningún concepto estadístico se introduce sin responder tres preguntas: qué cifra "
                 "contable depende de él, qué ocurre si está mal y qué procedimiento de auditoría "
                 "corresponde. Si las tres no tienen respuesta, el concepto no entra al programa."),
            ],
        },
        {
            "ref": "A-2",
            "titulo": "Los tres tipos de modelo",
            "bloques": [
                ("p", "En una institución financiera conviven al menos tres familias de modelos de "
                      "riesgo de crédito. Se construyen distinto, se evalúan contra umbrales "
                      "distintos y fallan de maneras distintas. Tratarlos como uno solo lleva a "
                      "conclusiones equivocadas."),
                ("tabla", [
                    ["Tipo", "Población", "Qué predice", "Información disponible"],
                    ["Admisión", "Cliente nuevo", "Si incumplirá el crédito solicitado", "Externa y declarada"],
                    ["Comportamiento", "Cliente vigente", "Si se deteriorará en los próximos meses", "Historial interno completo"],
                    ["Cobranza", "Cliente en mora", "Si seguirá empeorando o se recuperará", "Historial más gestión de cobro"],
                ]),
                ("cita", "El tercer mundo es todo lo que es cobranza: los recursos dentro de los "
                         "modelos de cobranza no son infinitos.",
                 "Clase 1, aprox. 01:03:31"),
                ("nota", "Consecuencia para la revisión",
                 "El modelo de comportamiento dispone de historial interno y por eso se le exige "
                 "más desempeño que a uno de admisión. Aplicar el mismo umbral a ambos es un error "
                 "que aparece con frecuencia en informes de validación."),
            ],
        },
        {
            "ref": "A-3",
            "titulo": "Ventana de observación y ventana de desempeño",
            "bloques": [
                ("p", "Todo modelo se construye sobre dos períodos. La ventana de observación es "
                      "aquella de la que se toman las características del cliente. La ventana de "
                      "desempeño es el período posterior en el que se observa si incumplió o no."),
                ("p", "Esta separación es lo que hace que el modelo prediga en lugar de describir. "
                      "Si una variable de la ventana de observación contiene información que en "
                      "realidad pertenece a la ventana de desempeño, el modelo está mirando la "
                      "respuesta."),
                ("cita", "Si yo construí un modelo de admisión de cliente con todas las "
                         "originaciones de créditos entre 2018 y 2020…",
                 "Clase 1, aprox. 01:53:29"),
                ("riesgo", "Ventana contaminada",
                 "Un cliente con buen comportamiento histórico dejó de comportarse igual durante la "
                 "pandemia. Un modelo construido con esa ventana aprende un patrón que no se repite "
                 "en condiciones normales, y su calibración queda desplazada aunque el orden entre "
                 "clientes se conserve."),
                ("nota", "Procedimiento",
                 "Solicitar las fechas exactas de ambas ventanas y verificar que no se superponen. "
                 "Preguntar expresamente si alguna abarca períodos con ayudas estatales, "
                 "reprogramaciones masivas o suspensión de cobranza, y qué tratamiento se dio a las "
                 "operaciones afectadas."),
            ],
        },
        {
            "ref": "A-4",
            "titulo": "Qué significa que un modelo esté mal",
            "bloques": [
                ("p", "Un modelo se equivoca en casos individuales por definición: estima "
                      "probabilidades, no certezas. Que rechace a un cliente que habría pagado no "
                      "es una falla. La falla es equivocarse de forma sistemática."),
                ("lista", [
                    "Sesgo: se equivoca siempre en la misma dirección, por ejemplo subestimando la "
                    "probabilidad de incumplimiento de un segmento completo.",
                    "Inestabilidad: funcionaba y dejó de funcionar porque la población cambió.",
                    "Fuga de información: parece funcionar porque usa datos que no existían al "
                    "momento de decidir.",
                    "Desalineación: funciona, pero no se usa como fue diseñado, por ejemplo con un "
                    "punto de corte que no corresponde a la política vigente.",
                ]),
                ("nota", "Por qué importa la distinción",
                 "Los cuatro producen hallazgos distintos y recomendaciones distintas. El sesgo "
                 "afecta la suficiencia de la provisión; la inestabilidad, el monitoreo; la fuga, la "
                 "construcción; la desalineación, el control interno operativo."),
            ],
        },
        {
            "ref": "A-5",
            "titulo": "Cómo se mide que un modelo separa",
            "bloques": [
                ("p", "La primera pregunta sobre cualquier modelo de clasificación es si logra "
                      "separar a quienes incumplen de quienes no. Existen tres medidas de uso "
                      "habitual y conviene reconocer qué aporta cada una."),
                ("cita", "Lo que se denomina tasa de divergencia o índice de divergencia: lo que "
                         "busco es que los promedios de las distribuciones sean lo más distintos "
                         "posibles.",
                 "Clase 1, aprox. 02:26:03"),
                ("umbral", "Referencias citables",
                 "Área bajo la curva ROC sobre 0,80 se considera buena. KS entre 25 % y 35 % es "
                 "normal en admisión y entre 35 % y 50 % en comportamiento. Divergencia sobre 2 "
                 "indica buena separación entre las distribuciones."),
                ("riesgo", "Qué sale mal",
                 "Se presentan las tres métricas como confirmaciones independientes. Área bajo la "
                 "curva y Gini son la misma medida en distinta escala, y las tres miden capacidad "
                 "de ordenar. Ninguna prueba que el nivel de la probabilidad estimada sea correcto."),
                ("nota", "Lo que falta en casi todos los informes",
                 "La comparación entre probabilidad estimada e incumplimiento observado. Es la única "
                 "evidencia que sostiene la suficiencia de la provisión, y se desarrolla en el "
                 "Módulo V."),
            ],
        },
        {
            "ref": "A-6",
            "titulo": "Quién responde por el número",
            "bloques": [
                ("p", "La provisión atraviesa varias áreas antes de llegar al estado financiero, y "
                      "cada una asume una responsabilidad distinta. Identificar quién responde por "
                      "qué es condición previa para dirigir un hallazgo a quien corresponde."),
                ("tabla", [
                    ["Función", "Responsabilidad"],
                    ["Negocio", "Origina las operaciones y aplica la política de crédito"],
                    ["Riesgos", "Construye el modelo y estima los parámetros"],
                    ["Contabilidad", "Registra la provisión y prepara la revelación"],
                    ["Auditoría interna", "Evalúa el diseño y la operación de los controles"],
                    ["Validación independiente", "Verifica que el modelo hace lo que dice hacer"],
                    ["Regulador", "Fija requisitos mínimos y supervisa su cumplimiento"],
                ]),
                ("riesgo", "Qué sale mal",
                 "La validación independiente la realiza el mismo equipo que construyó el modelo, o "
                 "reporta al área de riesgo. La revisión puede ser técnicamente impecable y aun así "
                 "no constituir validación independiente."),
            ],
        },
    ],

    "banco": [
        {"id": "a1", "puntaje": 10,
         "texto": "¿Qué cambió para el auditor con el paso a pérdida esperada?",
         "opciones": [
             {"txt": "La provisión pasó de ser una regla verificable a una estimación producida por "
                     "un modelo, por lo que se evalúa el proceso además de la cifra", "ok": True},
             {"txt": "La provisión dejó de registrarse en resultados"},
             {"txt": "El auditor ya no necesita revisar la cartera"},
             {"txt": "La provisión pasó a ser responsabilidad exclusiva del regulador"},
         ],
         "retro": "El cambio es de naturaleza de la cifra: de hecho verificable a estimación. Eso "
                  "traslada el foco al proceso que la produce."},

        {"id": "a2", "puntaje": 10,
         "texto": "¿Por qué se exige más desempeño a un modelo de comportamiento que a uno de "
                  "admisión?",
         "opciones": [
             {"txt": "Porque dispone del historial interno del cliente, información que el modelo "
                     "de admisión no tiene", "ok": True},
             {"txt": "Porque se aplica a carteras de mayor monto"},
             {"txt": "Porque lo exige expresamente la normativa contable"},
             {"txt": "Porque usa técnicas estadísticas más avanzadas"},
         ],
         "retro": "Más información disponible implica mayor expectativa de desempeño. Por eso los "
                  "umbrales de KS difieren entre ambos tipos."},

        {"id": "a3", "puntaje": 10,
         "texto": "¿Qué distingue a la ventana de observación de la de desempeño?",
         "opciones": [
             {"txt": "La de observación aporta las características del cliente; la de desempeño "
                     "registra si incumplió", "ok": True},
             {"txt": "La de observación es siempre de doce meses"},
             {"txt": "La de desempeño se usa solo en modelos de cobranza"},
             {"txt": "Son nombres distintos para el mismo período"},
         ],
         "retro": "La separación temporal entre ambas es lo que hace que el modelo prediga en lugar "
                  "de describir."},

        {"id": "a4", "puntaje": 10,
         "texto": "Un modelo rechaza a un cliente que habría pagado sin problemas. ¿Es una falla del "
                  "modelo?",
         "opciones": [
             {"txt": "No: el modelo estima probabilidades. La falla sería equivocarse de forma "
                     "sistemática", "ok": True},
             {"txt": "Sí: todo rechazo incorrecto es una falla"},
             {"txt": "Sí, si el cliente reclama formalmente"},
             {"txt": "Solo si el monto del crédito es material"},
         ],
         "retro": "Los errores individuales son inherentes. Lo que se audita es el error "
                  "sistemático: sesgo, inestabilidad, fuga o desalineación."},

        {"id": "a5", "puntaje": 10,
         "texto": "Un modelo funcionaba bien y su desempeño se deterioró porque la cartera cambió de "
                  "composición. ¿Cómo se clasifica?",
         "opciones": [
             {"txt": "Inestabilidad", "ok": True},
             {"txt": "Fuga de información"},
             {"txt": "Sesgo"},
             {"txt": "Desalineación"},
         ],
         "retro": "La inestabilidad apunta al monitoreo: el modelo era válido y la población dejó de "
                  "ser la misma."},

        {"id": "a6", "puntaje": 10,
         "texto": "El modelo opera con un punto de corte distinto al que fija la política vigente. "
                  "¿Cómo se clasifica?",
         "opciones": [
             {"txt": "Desalineación entre el modelo y su uso", "ok": True},
             {"txt": "Sesgo del modelo"},
             {"txt": "Inestabilidad de la población"},
             {"txt": "Error de calibración"},
         ],
         "retro": "El modelo puede ser correcto y estar mal utilizado. Es un hallazgo de control "
                  "interno operativo, no de metodología."},

        {"id": "a7", "puntaje": 10,
         "texto": "Un modelo de admisión reporta área bajo la curva de 0,82. ¿Qué se puede concluir?",
         "opciones": [
             {"txt": "Que ordena bien a los clientes, pero no que la probabilidad estimada tenga el "
                     "nivel correcto", "ok": True},
             {"txt": "Que la provisión está correctamente dimensionada"},
             {"txt": "Que el modelo es estable en el tiempo"},
             {"txt": "Que no requiere validación adicional"},
         ],
         "retro": "Discriminación y calibración son cosas distintas. Ordenar bien no implica estimar "
                  "bien el nivel."},

        {"id": "a8", "puntaje": 10,
         "texto": "¿Qué mide la divergencia?",
         "opciones": [
             {"txt": "Cuán distintos son los promedios de las distribuciones de quienes incumplen y "
                     "quienes no", "ok": True},
             {"txt": "La diferencia entre PD estimada y observada"},
             {"txt": "El desplazamiento de la población entre períodos"},
             {"txt": "La proporción de falsos positivos"},
         ],
         "retro": "Busca que las dos distribuciones estén lo más separadas posible. Valores sobre 2 "
                  "indican buena separación."},

        {"id": "a9", "puntaje": 10,
         "texto": "La validación del modelo la realizó el mismo equipo que lo construyó. ¿Cuál es la "
                  "observación?",
         "opciones": [
             {"txt": "No constituye validación independiente, aunque el trabajo sea técnicamente "
                     "correcto", "ok": True},
             {"txt": "Es adecuado porque conocen mejor el modelo"},
             {"txt": "Solo es observable si el resultado fue favorable"},
             {"txt": "Corresponde observación únicamente si lo exige el regulador"},
         ],
         "retro": "La independencia es una condición orgánica. La calidad técnica del trabajo no la "
                  "reemplaza."},

        {"id": "a10", "puntaje": 10,
         "texto": "¿Qué evidencia falta en casi todos los informes de desempeño?",
         "opciones": [
             {"txt": "La comparación entre probabilidad estimada e incumplimiento observado", "ok": True},
             {"txt": "El área bajo la curva de la muestra de desarrollo"},
             {"txt": "El listado de variables del modelo"},
             {"txt": "El índice de Gini"},
         ],
         "retro": "Es la única evidencia directa sobre la suficiencia de la provisión, y suele estar "
                  "ausente entre métricas de discriminación."},
    ],
}
