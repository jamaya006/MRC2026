# -*- coding: utf-8 -*-
"""Modulo VI — Estabilidad y validacion fuera de tiempo. Fuente: Clase 3 y practica de monitoreo."""

MODULO = {
    "ref": "F",
    "titulo": "Estabilidad y validación fuera de tiempo",
    "proposito": "Detectar el deterioro de un modelo que sigue operando. Es el módulo que sostiene "
                 "el encargo recurrente: un modelo aprobado hace tres años puede estar produciendo "
                 "hoy una provisión que ya no corresponde.",

    "cedulas": [
        {
            "ref": "F-1",
            "titulo": "Tres formas de validar y para qué sirve cada una",
            "bloques": [
                ("p", "Un modelo se evalúa sobre distintas muestras, y cada una responde una "
                      "pregunta diferente. Confundirlas es la causa de que un modelo aprobado se "
                      "deteriore sin que nadie lo advierta."),
                ("tabla", [
                    ["Muestra", "Qué responde", "Qué no detecta"],
                    ["Desarrollo", "Si el modelo aprendió", "Nada sobre generalización"],
                    ["Validación", "Si generaliza a otros clientes del mismo período", "Cambios en el tiempo"],
                    ["Fuera de tiempo", "Si sigue vigente en un período posterior", "—"],
                ]),
                ("cita", "Hay diferentes formas de hacer este corte de datos: algunos ocupan tres, "
                         "entrenamiento, prueba y validación, y lo hacen 60, 20 y 20; en este caso "
                         "vamos a ocupar 80 y 20.",
                 "Clase 3, aprox. 01:50:24"),
                ("riesgo", "Qué sale mal",
                 "La partición se hace al azar sobre todo el histórico. Clientes del mismo período "
                 "quedan en ambas muestras y la validación no prueba nada sobre el paso del tiempo. "
                 "Es el error más común y el más fácil de detectar."),
                ("nota", "Procedimiento",
                 "Solicitar las fechas mínima y máxima de cada muestra. Si los rangos se solapan "
                 "por completo, no existe validación fuera de tiempo, sin importar cómo se llame el "
                 "apartado del informe."),
            ],
        },
        {
            "ref": "F-2",
            "titulo": "PSI: cómo se calcula y qué significa",
            "bloques": [
                ("p", "El índice de estabilidad poblacional compara la distribución de una variable "
                      "o del puntaje entre el período en que se construyó el modelo y el período "
                      "actual. No mide desempeño: mide si la población sigue siendo la misma."),
                ("p", "Se calcula por tramo. Para cada uno se toma la diferencia entre el "
                      "porcentaje actual y el de referencia, se multiplica por el logaritmo de su "
                      "razón, y se suman los tramos."),
                ("tabla", [
                    ["Tramo de puntaje", "% referencia", "% actual", "Aporte al PSI"],
                    ["Bajo 400", "8,0 %", "14,0 %", "0,0336"],
                    ["400 a 500", "17,0 %", "21,0 %", "0,0085"],
                    ["500 a 600", "31,0 %", "29,0 %", "0,0013"],
                    ["600 a 700", "28,0 %", "24,0 %", "0,0062"],
                    ["Sobre 700", "16,0 %", "12,0 %", "0,0115"],
                    ["Total", "100 %", "100 %", "0,0611"],
                ]),
                ("umbral", "Interpretación del PSI",
                 "Bajo 0,10 la población es estable. Entre 0,10 y 0,25 hay desplazamiento "
                 "moderado que exige análisis. Sobre 0,25 el desplazamiento es relevante y el "
                 "modelo debe revisarse formalmente."),
                ("nota", "Qué mirar además del total",
                 "El PSI total puede ser bajo mientras dos tramos se compensan entre sí. Revisar "
                 "siempre el aporte por tramo, no solo la suma."),
            ],
        },
        {
            "ref": "F-3",
            "titulo": "PSI de la población y de las variables",
            "bloques": [
                ("p", "El PSI se aplica sobre el puntaje final y también sobre cada variable de "
                      "entrada. Cuando se calcula sobre las variables suele llamarse índice de "
                      "estabilidad de características. La combinación de ambos identifica el "
                      "origen del problema."),
                ("tabla", [
                    ["PSI del puntaje", "PSI de variables", "Diagnóstico"],
                    ["Bajo", "Bajo", "Población estable"],
                    ["Bajo", "Alto en algunas", "Cambios que se compensan; revisar igualmente"],
                    ["Alto", "Alto en pocas", "Origen identificado en esas variables"],
                    ["Alto", "Bajo en todas", "Revisar integridad del cálculo o cambio de política"],
                ]),
                ("riesgo", "Qué sale mal",
                 "Se monitorea solo el puntaje. Una variable cambia de definición en el sistema de "
                 "origen, el resto compensa y el puntaje se ve estable mientras el modelo ya opera "
                 "sobre datos distintos de los que se construyó."),
                ("nota", "Procedimiento",
                 "Solicitar el PSI por variable del último ciclo de monitoreo. Si no existe, la "
                 "institución no está en condiciones de identificar la causa de un deterioro "
                 "cuando ocurra."),
            ],
        },
        {
            "ref": "F-4",
            "titulo": "Ventanas contaminadas: el caso de la pandemia",
            "bloques": [
                ("p", "La estabilidad supone que el período de referencia es representativo. Cuando "
                      "la ventana de observación o de desempeño abarca un episodio excepcional, esa "
                      "suposición no se cumple y todas las métricas construidas sobre ella quedan "
                      "condicionadas."),
                ("p", "Durante los años de pandemia coexistieron ayudas estatales, "
                      "reprogramaciones masivas y suspensión de cobranza. El resultado fue "
                      "morosidad artificialmente baja. Un modelo construido con esa ventana aprende "
                      "un comportamiento de pago que no se repite en condiciones normales."),
                ("riesgo", "Cómo se manifiesta",
                 "El modelo subestima la probabilidad de incumplimiento de manera sistemática. La "
                 "discriminación puede seguir siendo buena, porque el orden entre clientes se "
                 "mantiene, mientras el nivel de la provisión queda por debajo del riesgo real."),
                ("umbral", "Preguntas obligatorias sobre la ventana",
                 "Qué período cubre la ventana de observación, qué período la de desempeño, si "
                 "alguno abarca episodios excepcionales, y qué tratamiento se dio a las operaciones "
                 "reprogramadas durante esos meses."),
                ("nota", "Procedimiento",
                 "Contrastar la tasa de incumplimiento del período de construcción contra la de los "
                 "períodos anterior y posterior. Una diferencia relevante sin explicación "
                 "documentada es un hallazgo con efecto directo sobre la suficiencia de la "
                 "provisión."),
            ],
        },
        {
            "ref": "F-5",
            "titulo": "Monitoreo: la política que casi nunca existe",
            "bloques": [
                ("p", "Un modelo no se valida una vez. La institución debe tener definido con qué "
                      "frecuencia se mide, qué umbrales disparan una acción y quién decide. Sin eso, "
                      "el monitoreo se convierte en un informe que nadie usa."),
                ("tabla", [
                    ["Indicador", "Frecuencia mínima", "Umbral de acción"],
                    ["PSI del puntaje", "Mensual", "Sobre 0,25"],
                    ["PSI por variable", "Trimestral", "Sobre 0,25 en cualquier variable"],
                    ["Área bajo la curva fuera de tiempo", "Semestral", "Caída sobre 5 puntos"],
                    ["PD estimada contra observada", "Anual", "Desvío sistemático por tramo"],
                    ["Tasa de aprobación", "Mensual", "Variación sin cambio de política"],
                ]),
                ("riesgo", "Qué sale mal",
                 "El monitoreo existe, arroja PSI sobre 0,25 durante cuatro trimestres seguidos y "
                 "no hay evidencia de acción. La deficiencia no es de medición sino de gobierno: "
                 "la institución sabía y no actuó."),
                ("nota", "Entregable de este módulo",
                 "La plantilla de monitoreo con los cinco indicadores, sus umbrales y el "
                 "responsable de cada uno. Es directamente reutilizable en encargos y es lo primero "
                 "que se solicita al revisar el gobierno de modelos."),
            ],
        },
    ],

    "banco": [
        {"id": "f1", "puntaje": 10,
         "texto": "¿Qué prueba una muestra de validación que comparte período con la de desarrollo?",
         "opciones": [
             {"txt": "Que el modelo generaliza a otros clientes del mismo período, pero nada sobre "
                     "el paso del tiempo", "ok": True},
             {"txt": "Que el modelo sigue vigente hoy"},
             {"txt": "Que la población es estable"},
             {"txt": "Que la provisión está bien calculada"},
         ],
         "retro": "Sin separación temporal no hay validación fuera de tiempo, aunque el informe "
                  "use ese título."},

        {"id": "f2", "puntaje": 10,
         "texto": "El PSI del puntaje es 0,31. ¿Qué corresponde?",
         "opciones": [
             {"txt": "Desplazamiento relevante de la población: el modelo debe revisarse "
                     "formalmente", "ok": True},
             {"txt": "Población estable, no se requiere acción"},
             {"txt": "El modelo perdió capacidad de discriminación"},
             {"txt": "La provisión está sobrestimada"},
         ],
         "retro": "Sobre 0,25 el desplazamiento exige revisión formal. El PSI no mide desempeño: "
                  "indica que la población ya no es la de referencia."},

        {"id": "f3", "puntaje": 10,
         "texto": "El PSI total es 0,08 pero dos tramos aportan 0,04 cada uno en direcciones "
                  "opuestas. ¿Qué corresponde observar?",
         "opciones": [
             {"txt": "Hay movimientos que se compensan en el total y deben analizarse por tramo", "ok": True},
             {"txt": "Nada: el total está bajo el umbral"},
             {"txt": "El cálculo del PSI está mal hecho"},
             {"txt": "Corresponde recalibrar el modelo"},
         ],
         "retro": "El total puede ocultar desplazamientos relevantes que se anulan entre sí. Por "
                  "eso se revisa el aporte por tramo."},

        {"id": "f4", "puntaje": 10,
         "texto": "El PSI del puntaje es bajo y el de una variable de entrada es 0,40. ¿Cuál es la "
                  "hipótesis más probable?",
         "opciones": [
             {"txt": "Esa variable cambió y el efecto se compensa con otras dentro del puntaje", "ok": True},
             {"txt": "El modelo está funcionando correctamente"},
             {"txt": "El PSI del puntaje está mal calculado"},
             {"txt": "La cartera creció"},
         ],
         "retro": "Es exactamente el caso que hace insuficiente monitorear solo el puntaje. La "
                  "causa típica es un cambio de definición en el sistema de origen."},

        {"id": "f5", "puntaje": 10,
         "texto": "Un modelo se construyó con ventana de desempeño durante los meses de ayudas "
                  "estatales y reprogramaciones masivas. ¿Cuál es el efecto esperable?",
         "opciones": [
             {"txt": "Subestimación sistemática de la probabilidad de incumplimiento", "ok": True},
             {"txt": "Sobreestimación de la probabilidad de incumplimiento"},
             {"txt": "Pérdida de capacidad de discriminación únicamente"},
             {"txt": "Ningún efecto si la muestra es grande"},
         ],
         "retro": "La morosidad observada fue artificialmente baja. El modelo aprende ese "
                  "comportamiento y estima por debajo del riesgo real."},

        {"id": "f6", "puntaje": 10,
         "texto": "En el caso anterior, ¿por qué la curva ROC puede seguir viéndose bien?",
         "opciones": [
             {"txt": "Porque mide el orden entre clientes, que puede mantenerse aunque el nivel "
                     "esté desplazado", "ok": True},
             {"txt": "Porque la ROC se calcula sobre la muestra de desarrollo"},
             {"txt": "Porque la ROC corrige automáticamente por el período"},
             {"txt": "Porque el desbalance de clases la infla"},
         ],
         "retro": "Discriminación y calibración son independientes. El orden se conserva; el nivel "
                  "no."},

        {"id": "f7", "puntaje": 10,
         "texto": "El PSI superó 0,25 durante cuatro trimestres y no hay evidencia de acción. ¿Cómo "
                  "se clasifica el hallazgo?",
         "opciones": [
             {"txt": "Deficiencia de gobierno de modelos: la institución detectó el deterioro y no "
                     "actuó", "ok": True},
             {"txt": "Deficiencia de la metodología de cálculo del PSI"},
             {"txt": "Observación sin efecto porque el monitoreo se realizó"},
             {"txt": "Hallazgo de auditoría de sistemas"},
         ],
         "retro": "Medir y no actuar es más grave que no medir: existe evidencia documentada de que "
                  "se conocía la situación."},

        {"id": "f8", "puntaje": 10,
         "texto": "¿Qué documento pediría primero al evaluar el monitoreo de un modelo?",
         "opciones": [
             {"txt": "La política que define indicadores, frecuencia, umbrales de acción y "
                     "responsables", "ok": True},
             {"txt": "El código fuente del modelo"},
             {"txt": "El último informe de resultados"},
             {"txt": "El acta de aprobación original"},
         ],
         "retro": "Sin política, cada informe se interpreta a discreción y no hay criterio contra "
                  "el cual medir el incumplimiento."},

        {"id": "f9", "puntaje": 10,
         "texto": "¿Qué evidencia demuestra que existe validación fuera de tiempo?",
         "opciones": [
             {"txt": "Fechas mínima y máxima de cada muestra, con la de prueba en un período "
                     "posterior al de desarrollo", "ok": True},
             {"txt": "El porcentaje de la partición, por ejemplo 80 y 20"},
             {"txt": "El nombre del apartado en el informe de validación"},
             {"txt": "El número de observaciones de cada muestra"},
         ],
         "retro": "La proporción de la partición no dice nada sobre separación temporal. Las fechas "
                  "sí."},

        {"id": "f10", "puntaje": 10,
         "texto": "¿Cuál de estos indicadores detecta un cambio de comportamiento del negocio antes "
                  "que las métricas de desempeño?",
         "opciones": [
             {"txt": "La tasa de aprobación, cuando varía sin cambio de política", "ok": True},
             {"txt": "El área bajo la curva de la muestra de desarrollo"},
             {"txt": "El information value de las variables originales"},
             {"txt": "La exactitud global del modelo"},
         ],
         "retro": "El desempeño requiere que el evento madure. La tasa de aprobación se observa de "
                  "inmediato y anticipa el problema."},
    ],
}
