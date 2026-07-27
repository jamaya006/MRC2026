# -*- coding: utf-8 -*-
"""Modulo V — Desempeno y evidencia grafica. Fuente: Clases 3 y 5."""

MODULO = {
    "ref": "E",
    "titulo": "Desempeño y evidencia gráfica",
    "proposito": "Leer las métricas y los gráficos con que un equipo de riesgo justifica su modelo, "
                 "y saber cuáles admiten conclusión y cuáles solo describen la muestra con que se "
                 "construyó.",

    "cedulas": [
        {
            "ref": "E-1",
            "titulo": "Discriminación: qué mide realmente la curva ROC",
            "bloques": [
                ("p", "La curva ROC responde una sola pregunta: si tomo al azar un cliente que "
                      "incumplió y uno que no, ¿con qué frecuencia el modelo le asigna peor puntaje "
                      "al que incumplió? El área bajo esa curva es esa frecuencia. No dice si la "
                      "probabilidad estimada es correcta en nivel, solo si el orden es correcto."),
                ("cita", "En términos de curva ROC, los modelos sobre 80 % son todos buenos.",
                 "Clase 5, aprox. 00:50:16"),
                ("umbral", "Referencia de discriminación",
                 "Un área bajo la curva de 0,50 equivale a no discriminar. Bajo 0,70 el modelo es "
                 "insuficiente para decisiones de crédito. Entre 0,70 y 0,80 es aceptable con "
                 "reservas. Sobre 0,80 se considera bueno. Sobre 0,95 hay que sospechar fuga de "
                 "información antes de celebrar."),
                ("p", "El índice de Gini expresa lo mismo en otra escala: es dos veces el área bajo "
                      "la curva menos uno. Un área de 0,84 equivale a un Gini de 0,68. No son dos "
                      "evidencias distintas: es la misma cifra presentada dos veces."),
                ("riesgo", "Qué sale mal",
                 "El informe presenta área bajo la curva, Gini y KS como si fueran tres "
                 "confirmaciones independientes del desempeño. Las dos primeras son la misma "
                 "medida; el KS aporta una lectura distinta, pero también sobre la misma capacidad "
                 "de ordenar."),
            ],
        },
        {
            "ref": "E-2",
            "titulo": "KS y divergencia",
            "bloques": [
                ("p", "El estadístico KS mide la máxima distancia entre la distribución acumulada de "
                      "clientes buenos y la de malos a lo largo del puntaje. Responde dónde se "
                      "separan más las dos poblaciones y cuánto."),
                ("umbral", "Rangos habituales de KS por tipo de modelo",
                 "En modelos de admisión, valores entre 25 % y 35 % son normales. En modelos de "
                 "comportamiento, donde hay historial interno del cliente, se esperan valores entre "
                 "35 % y 50 %. Un KS sobre 60 % en admisión debe verificarse antes de aceptarse. "
                 "En divergencia, valores sobre 2 indican buena separación."),
                ("nota", "Por qué importa la distinción",
                 "Un KS de 30 % es un buen resultado en admisión y un mal resultado en "
                 "comportamiento. Evaluar ambos contra el mismo umbral es un error frecuente en "
                 "informes de validación."),
                ("nota", "Procedimiento",
                 "Antes de contrastar cualquier métrica contra un umbral, identificar de qué tipo "
                 "de modelo se trata: admisión, comportamiento o cobranza. El umbral depende del "
                 "tipo, y esa clasificación debe estar en la documentación del modelo."),
            ],
        },
        {
            "ref": "E-3",
            "titulo": "Matriz de confusión y punto de corte",
            "bloques": [
                ("p", "El modelo entrega una probabilidad. Para decidir hace falta un punto de "
                      "corte. La matriz de confusión muestra las cuatro combinaciones posibles entre "
                      "lo que el modelo predijo y lo que efectivamente ocurrió, para ese corte."),
                ("tabla", [
                    ["", "Incumplió", "No incumplió"],
                    ["Modelo rechaza", "Acierto: pérdida evitada", "Falso positivo: negocio perdido"],
                    ["Modelo aprueba", "Falso negativo: pérdida asumida", "Acierto: negocio bueno"],
                ]),
                ("p", "Los dos errores no cuestan lo mismo. Un falso negativo cuesta la pérdida del "
                      "crédito; un falso positivo cuesta el margen que se dejó de ganar. Como la "
                      "pérdida suele ser varias veces el margen, el corte económicamente óptimo "
                      "está bastante por debajo del 50 % que la intuición sugiere."),
                ("umbral", "Consecuencia práctica",
                 "En carteras de consumo, con pérdida por operación incumplida muy superior al "
                 "margen por operación sana, el corte óptimo suele ubicarse en torno al 10 % de "
                 "probabilidad estimada, no al 50 %."),
                ("riesgo", "Qué sale mal",
                 "Se reporta exactitud global como métrica principal. En una cartera con 3 % de "
                 "incumplimiento, un modelo que aprueba todo tiene 97 % de exactitud y valor cero. "
                 "La exactitud no es una métrica útil con clases desbalanceadas."),
                ("nota", "Procedimiento",
                 "Solicitar la justificación económica del punto de corte vigente: costo asumido "
                 "por falso negativo, margen perdido por falso positivo y fecha de la última "
                 "revisión de esos supuestos."),
            ],
        },
        {
            "ref": "E-4",
            "titulo": "Modelos de estimación: cuando la salida no es una probabilidad",
            "bloques": [
                ("p", "No todos los modelos de riesgo predicen un evento binario. Los modelos de "
                      "estimación de renta, por ejemplo, predicen un monto, y ahí no aplican ROC ni "
                      "KS. Se evalúan comparando el valor estimado contra el valor real."),
                ("p", "La herramienta habitual es el gráfico de contorno de valor real contra valor "
                      "estimado. Un modelo que funciona concentra la masa de puntos alrededor de la "
                      "diagonal. Las desviaciones sistemáticas por sobre o por debajo de esa "
                      "diagonal son sesgo, no dispersión."),
                ("lista", [
                    "Nube concentrada sobre la diagonal: el modelo estima bien en ese rango.",
                    "Nube desplazada hacia arriba en los tramos bajos: el modelo sobreestima a los "
                    "clientes de menor renta.",
                    "Nube que se abre en los extremos: el modelo pierde precisión donde hay menos "
                    "observaciones.",
                    "Diferencias entre el contorno de entrenamiento y el de prueba: sobreajuste.",
                ]),
                ("riesgo", "Por qué importa para la provisión",
                 "Si la renta estimada alimenta el cálculo de capacidad de pago, un sesgo "
                 "sistemático de sobreestimación en los tramos bajos produce aprobaciones a "
                 "clientes cuya capacidad real es menor. El efecto aparece después, en la "
                 "morosidad de ese segmento."),
                ("nota", "Procedimiento",
                 "Pedir los gráficos de contorno de entrenamiento y de prueba por segmento y "
                 "compararlos. Si solo se entrega el de entrenamiento, el desempeño no está "
                 "acreditado."),
            ],
        },
        {
            "ref": "E-5",
            "titulo": "Calibración: el desempeño que casi nunca se revisa",
            "bloques": [
                ("p", "Discriminar y calibrar son cosas distintas. Un modelo discrimina bien si "
                      "ordena correctamente. Calibra bien si el nivel de la probabilidad estimada "
                      "coincide con la frecuencia observada. Un modelo puede ordenar "
                      "impecablemente y estimar mal el nivel."),
                ("p", "Para la provisión, la calibración es lo determinante. La probabilidad de "
                      "incumplimiento entra directamente en el cálculo de la pérdida esperada. Si "
                      "el modelo estima 2 % donde se observa 5 %, la provisión queda subestimada "
                      "aunque el área bajo la curva sea excelente."),
                ("tabla", [
                    ["Tramo de PD estimada", "PD promedio estimada", "Incumplimiento observado", "Desvío"],
                    ["Muy bajo", "0,8 %", "0,9 %", "Aceptable"],
                    ["Bajo", "2,1 %", "3,4 %", "Subestima"],
                    ["Medio", "6,5 %", "9,8 %", "Subestima"],
                    ["Alto", "18,0 %", "17,2 %", "Aceptable"],
                ]),
                ("nota", "Procedimiento",
                 "Solicitar la tabla de PD estimada contra incumplimiento observado por tramo, "
                 "sobre una ventana cerrada. Es la prueba directa de que la provisión está bien "
                 "dimensionada y frecuentemente no forma parte del informe de desempeño."),
                ("riesgo", "Qué sale mal",
                 "El informe de validación presenta solo métricas de discriminación. Se concluye "
                 "que el modelo es bueno y no se verificó lo único que afecta directamente la cifra "
                 "contable."),
            ],
        },
    ],

    "banco": [
        {"id": "e1", "puntaje": 10,
         "texto": "¿Qué mide el área bajo la curva ROC?",
         "opciones": [
             {"txt": "La capacidad del modelo de ordenar correctamente: dar peor puntaje a quien "
                     "incumple que a quien no", "ok": True},
             {"txt": "Que la probabilidad estimada coincide con la observada"},
             {"txt": "El porcentaje de decisiones correctas del modelo"},
             {"txt": "La estabilidad del modelo entre períodos"},
         ],
         "retro": "Mide orden, no nivel. Un modelo puede ordenar bien y estimar mal la magnitud de "
                  "la probabilidad."},

        {"id": "e2", "puntaje": 10,
         "texto": "El informe presenta área bajo la curva de 0,84 y Gini de 0,68 como dos "
                  "evidencias de desempeño. ¿Qué corresponde observar?",
         "opciones": [
             {"txt": "Son la misma medida en distinta escala: el Gini es dos veces el área menos "
                     "uno", "ok": True},
             {"txt": "El Gini está mal calculado"},
             {"txt": "Falta reportar la exactitud global"},
             {"txt": "Son evidencias independientes y correctas"},
         ],
         "retro": "0,84 × 2 − 1 = 0,68. Presentarlas como confirmaciones separadas sobreestima el "
                  "respaldo del modelo."},

        {"id": "e3", "puntaje": 10,
         "texto": "Un modelo de comportamiento reporta KS de 28 %. ¿Cómo se evalúa?",
         "opciones": [
             {"txt": "Bajo para un modelo de comportamiento, donde se esperan valores entre 35 % y "
                     "50 %", "ok": True},
             {"txt": "Adecuado, porque supera el 25 %"},
             {"txt": "Excelente para cualquier tipo de modelo"},
             {"txt": "No evaluable sin conocer el área bajo la curva"},
         ],
         "retro": "El umbral depende del tipo de modelo. Un KS de 28 % sería normal en admisión y "
                  "es insuficiente en comportamiento, que dispone de historial interno."},

        {"id": "e4", "puntaje": 10,
         "texto": "En una cartera con 3 % de incumplimiento, un modelo reporta 97 % de exactitud. "
                  "¿Qué conclusión corresponde?",
         "opciones": [
             {"txt": "La exactitud no es informativa con clases desbalanceadas: aprobar todo "
                     "produce el mismo resultado", "ok": True},
             {"txt": "El modelo tiene desempeño sobresaliente"},
             {"txt": "El punto de corte está bien calibrado"},
             {"txt": "Corresponde aumentar el punto de corte"},
         ],
         "retro": "Un modelo que nunca rechaza acierta el 97 % de las veces y no aporta valor. Con "
                  "clases desbalanceadas hay que mirar la matriz de confusión completa."},

        {"id": "e5", "puntaje": 10,
         "texto": "¿Por qué el punto de corte económicamente óptimo suele estar muy por debajo del "
                  "50 %?",
         "opciones": [
             {"txt": "Porque la pérdida de una operación incumplida es varias veces el margen de "
                     "una operación sana", "ok": True},
             {"txt": "Porque la mayoría de los clientes son malos"},
             {"txt": "Porque el modelo subestima sistemáticamente"},
             {"txt": "Porque lo exige la normativa"},
         ],
         "retro": "Los dos errores tienen costos asimétricos. El corte se fija donde el costo "
                  "esperado total es mínimo, no en el punto medio de la probabilidad."},

        {"id": "e6", "puntaje": 10,
         "texto": "En un modelo de estimación de renta, ¿qué indica una nube desplazada por encima "
                  "de la diagonal en los tramos bajos?",
         "opciones": [
             {"txt": "El modelo sobreestima sistemáticamente la renta de los clientes de menor "
                     "ingreso", "ok": True},
             {"txt": "El modelo tiene buena precisión en ese tramo"},
             {"txt": "Hay pocos datos en ese tramo"},
             {"txt": "El modelo está bien calibrado"},
         ],
         "retro": "Es sesgo, no dispersión. Si esa renta alimenta la capacidad de pago, produce "
                  "aprobaciones a clientes con capacidad real menor."},

        {"id": "e7", "puntaje": 10,
         "texto": "El equipo entrega solo el gráfico de contorno de la muestra de entrenamiento. "
                  "¿Cuál es la observación?",
         "opciones": [
             {"txt": "El desempeño no está acreditado: falta el contorno de la muestra de prueba "
                     "para descartar sobreajuste", "ok": True},
             {"txt": "Es suficiente si el gráfico muestra buen ajuste"},
             {"txt": "Corresponde solicitar la curva ROC en su lugar"},
             {"txt": "No aplica porque el modelo no es binario"},
         ],
         "retro": "El ajuste sobre la propia muestra de entrenamiento siempre se ve mejor. La "
                  "comparación entre ambas muestras es la evidencia."},

        {"id": "e8", "puntaje": 10,
         "texto": "¿Cuál es la diferencia entre discriminación y calibración?",
         "opciones": [
             {"txt": "Discriminar es ordenar correctamente; calibrar es que el nivel estimado "
                     "coincida con la frecuencia observada", "ok": True},
             {"txt": "Son sinónimos medidos con estadísticos distintos"},
             {"txt": "La calibración solo aplica a modelos de comportamiento"},
             {"txt": "La discriminación se mide sobre datos fuera de tiempo"},
         ],
         "retro": "Un modelo puede discriminar impecablemente y estimar mal el nivel. Para la "
                  "provisión, lo determinante es la calibración."},

        {"id": "e9", "puntaje": 10,
         "texto": "El modelo estima 2,1 % de PD en un tramo donde se observó 3,4 % de "
                  "incumplimiento. ¿Cuál es el efecto contable?",
         "opciones": [
             {"txt": "La provisión de ese tramo está subestimada, aunque la discriminación sea "
                     "buena", "ok": True},
             {"txt": "Ninguno: la diferencia está dentro de lo esperable"},
             {"txt": "Se compensa con los tramos donde sobreestima"},
             {"txt": "Afecta al punto de corte, no a la provisión"},
         ],
         "retro": "La PD entra directamente en el cálculo de la pérdida esperada. Un desvío "
                  "sistemático hacia abajo produce subprovisión."},

        {"id": "e10", "puntaje": 10,
         "texto": "Un modelo de admisión reporta área bajo la curva de 0,97. ¿Cuál es la primera "
                  "acción?",
         "opciones": [
             {"txt": "Verificar si alguna variable contiene información posterior a la decisión de "
                     "crédito", "ok": True},
             {"txt": "Aprobar el modelo por su desempeño sobresaliente"},
             {"txt": "Reducir el punto de corte"},
             {"txt": "Solicitar el índice de Gini para confirmar"},
         ],
         "retro": "Un desempeño así en admisión es infrecuente. La causa habitual es fuga de "
                  "información, no calidad excepcional del modelo."},
    ],
}
