# -*- coding: utf-8 -*-
"""Modulo VII — Perdida esperada y provision NIIF 9. Fuente: Clases 6 y 7."""

MODULO = {
    "ref": "G",
    "titulo": "Pérdida esperada y provisión NIIF 9",
    "proposito": "Seguir el recorrido completo desde el parámetro estadístico hasta el asiento "
                 "contable y la revelación, e identificar en qué punto de ese recorrido se pierde "
                 "la trazabilidad.",

    "cedulas": [
        {
            "ref": "G-1",
            "titulo": "Qué es una provisión y por qué existe",
            "bloques": [
                ("p", "La provisión por riesgo de crédito es la reserva que constituye una "
                      "institución financiera para cubrir las pérdidas potenciales derivadas del "
                      "incumplimiento de sus clientes. No es efectivo apartado: es un pasivo que "
                      "reconoce una obligación probable."),
                ("cita", "Es la reserva que tienen las instituciones financieras para cubrir las "
                         "potenciales pérdidas que se provocan por incumplimiento de contratos con "
                         "los clientes.",
                 "Clase 6, aprox. 00:00:19"),
                ("p", "La analogía que ordena el concepto para un contador es la depreciación. Un "
                      "activo se deteriora y ese deterioro se reconoce para que los libros muestren "
                      "el valor real del activo. La cartera de créditos es un activo, y la provisión "
                      "es el reconocimiento de su deterioro."),
                ("cita", "Como cualquier activo, para mí la provisión es el concepto del deterioro "
                         "de ese activo, como hablar de una depreciación: para tener en los libros "
                         "el valor real de ese activo.",
                 "Clase 6, aprox. 00:09:08"),
                ("nota", "Consecuencia para la auditoría",
                 "Si la cartera tiene más probabilidad de impago, la provisión debe ser mayor. La "
                 "pregunta de auditoría no es si la provisión existe, sino si su magnitud "
                 "corresponde al riesgo efectivo de la cartera en la fecha de cierre."),
            ],
        },
        {
            "ref": "G-2",
            "titulo": "Los tres parámetros y la fórmula",
            "bloques": [
                ("p", "La pérdida esperada se compone de tres parámetros. Cada uno proviene de un "
                      "modelo distinto, con datos, supuestos y responsables distintos. Revisarlos "
                      "como un solo bloque es el error de enfoque más frecuente."),
                ("tabla", [
                    ["Parámetro", "Qué estima", "Origen habitual del dato"],
                    ["PD", "Probabilidad de que el cliente incumpla", "Modelo de score o matriz de transición"],
                    ["LGD", "Porcentaje de la exposición que no se recupera", "Historia de recuperación y garantías"],
                    ["EAD", "Exposición al momento del incumplimiento", "Saldo más factores de conversión del contingente"],
                ]),
                ("p", "La pérdida esperada de una operación es el producto de los tres. Como es un "
                      "producto, un error en cualquiera de ellos se traslada íntegro al resultado: "
                      "un 20 % de error en la LGD produce un 20 % de error en la provisión, "
                      "cualquiera sea la calidad del modelo de PD."),
                ("cita", "Es poco común que el criterio prospectivo se aplique sobre la EAD, porque "
                         "la EAD corresponde básicamente a los factores del contingente.",
                 "Clase 8, aprox. 00:01:54"),
                ("riesgo", "Qué sale mal",
                 "Toda la atención de validación se concentra en el modelo de PD, que es el más "
                 "elaborado y el que tiene métricas atractivas. La LGD suele ser un promedio "
                 "histórico sin modelo detrás y sin revisión, y pesa exactamente igual en la cifra."),
                ("nota", "Procedimiento",
                 "Solicitar por separado la documentación de PD, LGD y EAD. Registrar cuál de las "
                 "tres carece de metodología formal. Habitualmente es la LGD, y ahí suele estar el "
                 "mayor riesgo no cubierto."),
            ],
        },
        {
            "ref": "G-3",
            "titulo": "Etapas y horizonte de estimación",
            "bloques": [
                ("p", "El marco de pérdida esperada clasifica las operaciones en tres etapas según "
                      "haya o no aumento significativo del riesgo desde el reconocimiento inicial. "
                      "La etapa determina el horizonte sobre el que se estima la pérdida."),
                ("tabla", [
                    ["Etapa", "Situación", "Horizonte de la pérdida esperada"],
                    ["1", "Sin aumento significativo del riesgo", "Doce meses"],
                    ["2", "Aumento significativo, sin deterioro crediticio", "Toda la vida del instrumento"],
                    ["3", "Con deterioro crediticio", "Toda la vida, con interés sobre saldo neto"],
                ]),
                ("p", "El paso de etapa 1 a etapa 2 multiplica la provisión de una operación, porque "
                      "cambia el horizonte. Por eso el criterio de aumento significativo del riesgo "
                      "es una de las definiciones con mayor efecto sobre la cifra y una de las menos "
                      "formalizadas."),
                ("riesgo", "Qué sale mal",
                 "El criterio de traspaso está definido de forma cualitativa o depende de un umbral "
                 "que se puede ajustar sin cambiar la metodología documentada. Mover ese umbral "
                 "mueve la provisión sin que aparezca como cambio de política contable."),
                ("nota", "Procedimiento",
                 "Obtener el criterio cuantitativo de traspaso entre etapas, verificar que está "
                 "aprobado formalmente y recalcular la distribución de la cartera por etapa "
                 "aplicándolo sobre una muestra. Documentar cualquier diferencia contra el reporte."),
            ],
        },
        {
            "ref": "G-4",
            "titulo": "Información prospectiva",
            "bloques": [
                ("p", "El marco exige incorporar información prospectiva: la estimación no puede "
                      "basarse solo en lo observado, debe considerar condiciones futuras esperadas. "
                      "En la práctica esto se traduce en proyectar los parámetros según escenarios "
                      "macroeconómicos."),
                ("cita", "Se busca que se tomen los criterios prospectivos tanto en la probabilidad "
                         "de incumplimiento como en la LGD. El criterio es que usted debe proyectar.",
                 "Clase 8, aprox. 00:02:42"),
                ("p", "Los escenarios se ponderan por probabilidad de ocurrencia. Esa ponderación es "
                      "una decisión de la administración con efecto directo sobre la provisión, y "
                      "es uno de los puntos donde la subjetividad es mayor."),
                ("umbral", "Qué debe estar documentado",
                 "Escenarios utilizados, variables macroeconómicas de cada uno, fuente de las "
                 "proyecciones, ponderación asignada a cada escenario, fundamento de esa "
                 "ponderación y quién la aprobó."),
                ("riesgo", "Qué sale mal",
                 "La ponderación de escenarios se ajusta para alcanzar un nivel de provisión "
                 "predefinido. Sin fundamento documentado y sin comparación con la ponderación del "
                 "período anterior, el ajuste es indetectable en el estado financiero."),
                ("nota", "Procedimiento",
                 "Comparar la ponderación de escenarios entre cierres consecutivos. Todo cambio "
                 "debe tener fundamento documentado y aprobación. Un cambio de ponderación sin "
                 "cambio en las proyecciones macroeconómicas subyacentes exige explicación."),
            ],
        },
        {
            "ref": "G-5",
            "titulo": "Del parámetro al asiento",
            "bloques": [
                ("p", "La cadena completa tiene ocho eslabones y la trazabilidad se pierde casi "
                      "siempre en el mismo punto: entre la salida del motor de cálculo y el asiento "
                      "contable, donde suelen aplicarse ajustes manuales."),
                ("pasos", [
                    "Extracción de datos de los sistemas de origen.",
                    "Cálculo de los parámetros por operación o por segmento.",
                    "Aplicación de la fórmula de pérdida esperada.",
                    "Agregación por cartera y por etapa.",
                    "Ajustes de la administración, si existen.",
                    "Asiento contable del gasto y de la provisión acumulada.",
                    "Conciliación entre el motor de cálculo y el mayor contable.",
                    "Revelación en notas.",
                ]),
                ("riesgo", "El ajuste de la administración",
                 "Es la diferencia entre lo que el modelo calcula y lo que finalmente se contabiliza. "
                 "Puede estar justificado, por ejemplo cuando el modelo no captura un riesgo "
                 "reciente. Pero debe estar cuantificado, fundamentado y aprobado, y debe "
                 "conciliar con el mayor."),
                ("umbral", "Prueba mínima de conciliación",
                 "La suma de la provisión por operación del motor de cálculo debe conciliar con el "
                 "saldo del mayor. Toda diferencia debe estar explicada línea por línea. Una "
                 "diferencia sin explicación es un hallazgo, aunque su monto sea inmaterial: "
                 "revela que el control de conciliación no opera."),
                ("nota", "Entregable de este módulo",
                 "La hoja de recálculo de provisión: se toma una muestra de operaciones, se "
                 "reconstruye la pérdida esperada con los parámetros vigentes y se concilia contra "
                 "lo contabilizado."),
            ],
        },
    ],

    "banco": [
        {"id": "g1", "puntaje": 10,
         "texto": "¿Qué representa contablemente la provisión por riesgo de crédito?",
         "opciones": [
             {"txt": "Un pasivo que reconoce el deterioro esperado de la cartera, análogo a la "
                     "depreciación de un activo", "ok": True},
             {"txt": "Efectivo apartado en una cuenta restringida"},
             {"txt": "Un activo contingente"},
             {"txt": "Una reserva patrimonial de libre disposición"},
         ],
         "retro": "Es un pasivo, no liquidez reservada. La cartera es un activo y la provisión "
                  "reconoce su deterioro."},

        {"id": "g2", "puntaje": 10,
         "texto": "La LGD utilizada es un promedio histórico sin metodología documentada, mientras "
                  "la PD proviene de un modelo validado. ¿Cuál es la observación?",
         "opciones": [
             {"txt": "La LGD pesa igual que la PD en el producto: un error en ella se traslada "
                     "íntegro a la provisión", "ok": True},
             {"txt": "No hay observación: la PD es el parámetro determinante"},
             {"txt": "La LGD no requiere metodología por norma"},
             {"txt": "El efecto se compensa con la EAD"},
         ],
         "retro": "La pérdida esperada es un producto. Un 20 % de error en LGD produce 20 % de "
                  "error en la provisión, por bueno que sea el modelo de PD."},

        {"id": "g3", "puntaje": 10,
         "texto": "Una operación pasa de etapa 1 a etapa 2. ¿Qué cambia en el cálculo?",
         "opciones": [
             {"txt": "El horizonte de estimación pasa de doce meses a toda la vida del instrumento", "ok": True},
             {"txt": "Se deja de reconocer interés"},
             {"txt": "La LGD se fija en 100 %"},
             {"txt": "La operación se castiga"},
         ],
         "retro": "El cambio de etapa cambia el horizonte, y por eso multiplica la provisión de la "
                  "operación."},

        {"id": "g4", "puntaje": 10,
         "texto": "El criterio de aumento significativo del riesgo está definido cualitativamente y "
                  "depende de un umbral ajustable. ¿Cuál es el riesgo?",
         "opciones": [
             {"txt": "Se puede mover la provisión ajustando el umbral, sin que aparezca como cambio "
                     "de política contable", "ok": True},
             {"txt": "Se incumple la definición de cartera vencida"},
             {"txt": "Se afecta la clasificación del activo en el balance"},
             {"txt": "Ninguno, mientras el umbral esté dentro de rangos de mercado"},
         ],
         "retro": "El traspaso entre etapas es una de las definiciones con mayor efecto sobre la "
                  "cifra. Debe ser cuantitativo y aprobado formalmente."},

        {"id": "g5", "puntaje": 10,
         "texto": "¿Qué significa incorporar información prospectiva en la estimación?",
         "opciones": [
             {"txt": "Proyectar los parámetros considerando condiciones macroeconómicas futuras "
                     "esperadas, no solo la historia observada", "ok": True},
             {"txt": "Estimar la provisión del ejercicio siguiente"},
             {"txt": "Usar solo el último año de datos"},
             {"txt": "Proyectar el crecimiento de la cartera"},
         ],
         "retro": "La estimación no puede apoyarse únicamente en lo observado. Se proyecta según "
                  "escenarios y se pondera por probabilidad de ocurrencia."},

        {"id": "g6", "puntaje": 10,
         "texto": "La ponderación de escenarios cambió respecto del cierre anterior sin que "
                  "cambiaran las proyecciones macroeconómicas. ¿Qué corresponde?",
         "opciones": [
             {"txt": "Requerir el fundamento documentado y la aprobación del cambio", "ok": True},
             {"txt": "Aceptarlo: la ponderación es una decisión discrecional"},
             {"txt": "Recalcular la provisión con la ponderación anterior y reportar la diferencia "
                     "como error"},
             {"txt": "Reportarlo solo si el efecto supera la materialidad"},
         ],
         "retro": "La ponderación tiene efecto directo sobre la provisión y es uno de los puntos de "
                  "mayor subjetividad. Todo cambio requiere fundamento."},

        {"id": "g7", "puntaje": 10,
         "texto": "¿En qué punto de la cadena se pierde con más frecuencia la trazabilidad?",
         "opciones": [
             {"txt": "Entre la salida del motor de cálculo y el asiento contable, donde se aplican "
                     "ajustes manuales", "ok": True},
             {"txt": "En la extracción de datos de los sistemas de origen"},
             {"txt": "En la aplicación de la fórmula de pérdida esperada"},
             {"txt": "En la revelación en notas"},
         ],
         "retro": "Los ajustes de la administración pueden estar justificados, pero deben estar "
                  "cuantificados, fundamentados y conciliados con el mayor."},

        {"id": "g8", "puntaje": 10,
         "texto": "Existe una diferencia inmaterial y sin explicación entre el motor de cálculo y el "
                  "mayor contable. ¿Cómo se trata?",
         "opciones": [
             {"txt": "Es un hallazgo: revela que el control de conciliación no está operando", "ok": True},
             {"txt": "No se reporta por ser inmaterial"},
             {"txt": "Se ajusta contra resultados del ejercicio"},
             {"txt": "Se documenta como diferencia de redondeo"},
         ],
         "retro": "La materialidad del monto no determina la conclusión sobre el control. Una "
                  "diferencia sin explicación indica que la conciliación no se está ejecutando."},

        {"id": "g9", "puntaje": 10,
         "texto": "¿Cuál de los tres parámetros suele carecer de metodología formal?",
         "opciones": [
             {"txt": "La LGD", "ok": True},
             {"txt": "La PD"},
             {"txt": "La EAD"},
             {"txt": "Ninguno: los tres se documentan por igual"},
         ],
         "retro": "La PD concentra la atención por sus métricas. La LGD suele ser un promedio "
                  "histórico sin revisión, y pesa igual en la fórmula."},

        {"id": "g10", "puntaje": 10,
         "texto": "¿Qué evidencia sustenta mejor la suficiencia de la provisión de un segmento?",
         "opciones": [
             {"txt": "La comparación entre PD estimada e incumplimiento efectivamente observado en "
                     "una ventana cerrada", "ok": True},
             {"txt": "El área bajo la curva del modelo de PD"},
             {"txt": "El acta del comité que aprobó la metodología"},
             {"txt": "El PSI del puntaje del período"},
         ],
         "retro": "La suficiencia depende del nivel, no del orden. Solo la comparación entre "
                  "estimado y observado prueba que la provisión está bien dimensionada."},
    ],
}
