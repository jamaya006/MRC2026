# -*- coding: utf-8 -*-
"""Modulo II — De la variable al scorecard. Fuente: Clase 2."""

MODULO = {
    "ref": "B",
    "titulo": "De la variable al scorecard",
    "proposito": "Revisar cómo se eligen y transforman las variables de un modelo de score, "
                 "y detectar las tres fallas que más se repiten en esa etapa: correlación mal "
                 "medida, tramos hechos por conveniencia y modelos ajustados a su propia muestra.",

    "cedulas": [
        {
            "ref": "B-1",
            "titulo": "Selección de variables: por qué la correlación no alcanza",
            "bloques": [
                ("p", "El primer filtro de un modelo es descartar variables redundantes. El error "
                      "frecuente es aplicar correlación de Pearson a todo el conjunto sin mirar la "
                      "naturaleza de cada variable. Pearson mide asociación lineal entre variables "
                      "continuas; aplicada a variables cualitativas o a continuas ya tramificadas, "
                      "entrega un número que no significa lo que el modelador cree."),
                ("cita", "Hay que tener en cuenta la naturaleza de las variables a la hora de "
                         "analizarlas por correlación, sobre todo cuando son cualitativas, porque "
                         "la correlación de Pearson por sí sola no ayuda.",
                 "Clase 2, aprox. 00:13:05"),
                ("riesgo", "Qué sale mal",
                 "Dos variables que miden lo mismo sobreviven al filtro porque su correlación "
                 "calculada fue baja. El modelo queda con multicolinealidad, los coeficientes se "
                 "vuelven inestables y basta un cambio menor de muestra para que cambien de signo."),
                ("nota", "Procedimiento",
                 "Solicitar la matriz de correlación junto con el diccionario de variables y "
                 "verificar que el estadístico usado corresponde al tipo de variable. Para pares "
                 "categórica-categórica corresponde V de Cramér o chi cuadrado; para "
                 "categórica-continua, razón de correlación. Documentar el umbral de descarte y "
                 "confirmar que se aplicó de forma consistente."),
            ],
        },
        {
            "ref": "B-2",
            "titulo": "Weight of evidence: qué mide y cómo se lee",
            "bloques": [
                ("p", "El weight of evidence, o WOE, se calcula por tramo de una variable. Compara "
                      "la proporción de clientes buenos que caen en ese tramo con la proporción de "
                      "clientes malos que caen en el mismo tramo, y toma el logaritmo de esa razón. "
                      "Un WOE positivo indica concentración de buenos; uno negativo, de malos."),
                ("cita", "El WOE se define a nivel de cada tramo: el logaritmo de la proporción de "
                         "buenos en la categoría sobre el total de buenos, contra la proporción "
                         "equivalente de malos.",
                 "Clase 2, aprox. 00:19:57"),
                ("p", "La utilidad para auditoría es que el WOE hace visible el comportamiento de "
                      "la variable tramo por tramo. Una variable puede tener buen poder predictivo "
                      "global y aun así comportarse de forma incoherente en un tramo específico."),
                ("tabla", [
                    ["Tramo de antigüedad", "Buenos", "Malos", "WOE", "Lectura"],
                    ["Menos de 6 meses", "1.200", "480", "-0,62", "Concentra malos"],
                    ["6 a 24 meses", "3.400", "610", "0,18", "Cerca del promedio"],
                    ["24 a 60 meses", "4.100", "390", "0,71", "Concentra buenos"],
                    ["Más de 60 meses", "2.300", "340", "0,41", "Rompe la monotonía"],
                ]),
                ("riesgo", "Qué sale mal",
                 "El último tramo baja en lugar de seguir subiendo. Si el modelador no lo explica, "
                 "hay dos posibilidades: el tramo tiene pocos casos y el WOE es ruido, o la variable "
                 "no se comporta como el negocio supone. Ambas exigen respuesta antes de aceptar "
                 "el modelo."),
                ("nota", "Procedimiento",
                 "Pedir la tabla de WOE por variable con el conteo de casos por tramo. Marcar todo "
                 "tramo con menos del 5 % de la población y todo quiebre de monotonía sin "
                 "justificación escrita en la documentación del modelo."),
            ],
        },
        {
            "ref": "B-3",
            "titulo": "Information value: el umbral que se puede citar",
            "bloques": [
                ("p", "Mientras el WOE describe cada tramo, el information value resume en un solo "
                      "número el poder predictivo de la variable completa. Se usa para decidir qué "
                      "variables entran al modelo, y es especialmente habitual en regresión "
                      "logística binaria y en modelos de score."),
                ("cita", "El information value mide la predicción del atributo, y es muy útil "
                         "cuando se trabaja con regresiones logísticas binarias, en particular "
                         "para un modelo de score.",
                 "Clase 2, aprox. 00:15:17"),
                ("umbral", "Rangos de referencia del information value",
                 "Bajo 0,02 la variable no aporta. Entre 0,02 y 0,10 el aporte es débil. Entre 0,10 "
                 "y 0,30 es aceptable. Entre 0,30 y 0,50 es fuerte. Sobre 0,50 hay que sospechar: "
                 "una variable así de predictiva suele contener información que no estaba "
                 "disponible al momento de decidir."),
                ("riesgo", "Qué sale mal",
                 "El caso clásico es una variable con IV superior a 0,8 que resulta ser el estado "
                 "de morosidad del propio período que se quiere predecir. El modelo luce excelente "
                 "en desarrollo y no sirve en producción, porque esa variable no existe cuando hay "
                 "que decidir sobre un cliente nuevo."),
                ("nota", "Procedimiento",
                 "Listar las variables con IV sobre 0,50 y para cada una reconstruir el momento en "
                 "que el dato queda disponible. Contrastarlo con la fecha de la decisión de crédito. "
                 "Si el dato es posterior, hay fuga de información y el desempeño reportado está "
                 "sobrestimado."),
            ],
        },
        {
            "ref": "B-4",
            "titulo": "Binning: dónde se pierde la trazabilidad",
            "bloques": [
                ("p", "Convertir una variable continua en tramos se llama binning. Existen rutinas "
                      "de binning óptimo que buscan automáticamente los cortes que maximizan el "
                      "information value. El problema es que el óptimo estadístico y el óptimo de "
                      "gestión no coinciden."),
                ("cita", "El binning óptimo maximiza la diferencia a través del information "
                         "value. El problema de ese óptimo es que maximiza los grupos: busca "
                         "muchos grupos.",
                 "Clase 2, aprox. 00:29:06"),
                ("p", "Muchos tramos elevan el IV en la muestra de desarrollo y al mismo tiempo "
                      "dejan tramos con pocos casos, que son los primeros en volverse inestables "
                      "cuando la cartera cambia. Un modelo con veinte tramos por variable es un "
                      "modelo difícil de explicar a un comité y difícil de monitorear."),
                ("umbral", "Criterio práctico de revisión",
                 "Entre cuatro y seis tramos por variable, cada uno con al menos 5 % de la "
                 "población, y WOE monótono salvo justificación de negocio documentada."),
                ("riesgo", "Qué sale mal",
                 "Los cortes se rehacen sobre la misma muestra hasta que el modelo alcanza la "
                 "métrica que el comité quería ver. No queda registro de los cortes descartados y "
                 "el resultado es un modelo ajustado a su propia muestra."),
                ("nota", "Procedimiento",
                 "Solicitar la bitácora de construcción del binning: cortes probados, criterio de "
                 "selección y quién los aprobó. La ausencia de esa bitácora es en sí misma un "
                 "hallazgo de control interno, independiente de la calidad estadística del modelo."),
            ],
        },
        {
            "ref": "B-5",
            "titulo": "Del modelo al scorecard: odds, puntos y escala",
            "bloques": [
                ("p", "La salida de una regresión logística es una probabilidad. Una probabilidad "
                      "de 0,037 no es un número con el que un comité de crédito trabaje cómodamente. "
                      "Por eso se aplica una transformación lineal que lleva esa probabilidad a una "
                      "escala de puntos: eso es la scorecard."),
                ("cita", "La probabilidad no siempre es fácil de interpretar en un comité. Por eso "
                         "se instauró la scorecard, que es hacer una transformación lineal de las "
                         "probabilidades a una escala entendible.",
                 "Clase 2, aprox. 00:56:32"),
                ("p", "El odds es la razón entre buenos y malos de la población. Si por cada veinte "
                      "clientes buenos hay uno malo, el odds es veinte a uno. La escala se define "
                      "fijando un puntaje de referencia para un odds dado y los puntos necesarios "
                      "para duplicar ese odds."),
                ("tabla", [
                    ["Atributo del solicitante", "Puntos"],
                    ["Base de la escala", "83"],
                    ["Sexo declarado: hombre", "98"],
                    ["Línea disponible entre 2,5 y 4,5 veces el ingreso", "93"],
                    ["Puntaje total del ejemplo", "274"],
                ]),
                ("riesgo", "Qué sale mal",
                 "La escala es una transformación, no información nueva. Reescalar no mejora un "
                 "modelo malo: solo lo hace ver ordenado. Un scorecard bien presentado puede "
                 "esconder un modelo con discriminación insuficiente."),
                ("nota", "Procedimiento",
                 "Verificar que el puntaje de corte usado en la operación corresponde a la "
                 "probabilidad que la política de crédito dice aceptar. Es frecuente que la escala "
                 "se recalibre y el punto de corte quede en el valor antiguo, aprobando clientes "
                 "que la política vigente rechazaría."),
                ("riesgo", "Atributos sensibles",
                 "Cuando la scorecard asigna puntos por sexo, edad, nacionalidad o domicilio, hay "
                 "que verificar si la normativa aplicable lo permite y si existe evaluación de "
                 "trato diferenciado. Es un riesgo regulatorio y reputacional, no solo estadístico."),
            ],
        },
        {
            "ref": "B-6",
            "titulo": "Sobreajuste y regularización",
            "bloques": [
                ("p", "Un modelo sobreajustado es el que funciona muy bien sobre la población con "
                      "la que se construyó y falla al aplicarse a otra. Es el riesgo central de "
                      "toda la etapa de construcción, y por eso importa el binning, el número de "
                      "variables y la separación entre muestra de desarrollo y de validación."),
                ("cita", "Cuando trato de perfeccionar tanto el modelo, ese modelo tiende a "
                         "sobreajustarse: funciona muy bien para la población con la que se "
                         "construyó, pero no cuando se aplica a una población diferente.",
                 "Clase 2, aprox. 01:17:07"),
                ("p", "Ridge y Lasso son técnicas de regularización: penalizan los coeficientes "
                      "grandes para que el modelo generalice mejor y para reducir "
                      "multicolinealidad. Lasso además puede llevar coeficientes exactamente a "
                      "cero, con lo que selecciona variables."),
                ("umbral", "Señal de alerta",
                 "Una caída del área bajo la curva superior a cinco puntos porcentuales entre la "
                 "muestra de desarrollo y la de validación indica sobreajuste y exige explicación."),
                ("nota", "Procedimiento",
                 "Pedir las métricas de desempeño calculadas por separado en desarrollo y en "
                 "validación, con el detalle de cómo se dividió la muestra. Si solo existe una "
                 "cifra global, el modelo no fue validado: fue descrito."),
            ],
        },
    ],

    "banco": [
        {"id": "b1", "puntaje": 10,
         "texto": "El equipo de riesgo descartó variables usando correlación de Pearson sobre todo "
                  "el conjunto, incluidas variables categóricas. ¿Cuál es la observación correcta?",
         "opciones": [
             {"txt": "Pearson no es el estadístico apropiado para variables categóricas, por lo que "
                     "el filtro pudo dejar pasar variables redundantes", "ok": True},
             {"txt": "Es correcto: Pearson se aplica a cualquier tipo de variable"},
             {"txt": "El problema es el umbral usado, no el estadístico"},
             {"txt": "No corresponde observación porque la correlación es una etapa exploratoria"},
         ],
         "retro": "Pearson mide asociación lineal entre continuas. Para pares categóricos "
                  "corresponde V de Cramér o chi cuadrado. El riesgo es multicolinealidad no "
                  "detectada y coeficientes inestables."},

        {"id": "b2", "puntaje": 10,
         "texto": "Una variable presenta WOE de -0,62 en el primer tramo y 0,71 en el tercero. "
                  "¿Qué indica el signo negativo?",
         "opciones": [
             {"txt": "Que ese tramo concentra proporcionalmente más clientes malos que buenos", "ok": True},
             {"txt": "Que la variable fue mal calculada, porque el WOE no puede ser negativo"},
             {"txt": "Que el tramo tiene pocos casos"},
             {"txt": "Que la variable debe eliminarse del modelo"},
         ],
         "retro": "El WOE es un logaritmo de razón de proporciones: negativo significa mayor peso "
                  "de malos en ese tramo. Es informativo, no un defecto."},

        {"id": "b3", "puntaje": 10,
         "texto": "Una variable presenta information value de 0,84. ¿Cuál es la primera hipótesis "
                  "que debe verificar el auditor?",
         "opciones": [
             {"txt": "Que la variable contiene información no disponible al momento de la decisión "
                     "de crédito", "ok": True},
             {"txt": "Que la variable es excelente y debe ponderarse más"},
             {"txt": "Que el binning tiene pocos tramos"},
             {"txt": "Que el modelo está subajustado"},
         ],
         "retro": "Un IV sobre 0,50 es sospechoso. El caso típico es una variable que refleja el "
                  "propio evento que se quiere predecir. El desempeño reportado queda sobrestimado."},

        {"id": "b4", "puntaje": 10,
         "texto": "El modelador usó una rutina de binning óptimo que generó dieciocho tramos para "
                  "una variable continua. ¿Cuál es el riesgo principal?",
         "opciones": [
             {"txt": "Tramos con pocos casos que se vuelven inestables al cambiar la cartera, y un "
                     "modelo difícil de explicar y monitorear", "ok": True},
             {"txt": "Ninguno: más tramos siempre mejoran la capacidad predictiva"},
             {"txt": "Que el information value quede subestimado"},
             {"txt": "Que la variable pase a ser categórica"},
         ],
         "retro": "El óptimo estadístico maximiza el IV en la muestra de desarrollo. Eso eleva la "
                  "métrica y al mismo tiempo fragiliza el modelo fuera de esa muestra."},

        {"id": "b5", "puntaje": 10,
         "texto": "En la revisión del binning, el equipo no conserva registro de los cortes "
                  "probados y descartados. ¿Cómo se clasifica esto?",
         "opciones": [
             {"txt": "Hallazgo de control interno por falta de trazabilidad, independiente de la "
                     "calidad estadística del resultado", "ok": True},
             {"txt": "No es hallazgo si el modelo alcanza las métricas mínimas"},
             {"txt": "Hallazgo solo si el regulador lo exige expresamente"},
             {"txt": "Observación menor que se comunica verbalmente"},
         ],
         "retro": "Sin bitácora no se puede descartar que los cortes se hayan ajustado hasta "
                  "obtener la métrica deseada. La ausencia de evidencia es el hallazgo."},

        {"id": "b6", "puntaje": 10,
         "texto": "¿Qué es el odds en la construcción de una scorecard?",
         "opciones": [
             {"txt": "La razón entre clientes buenos y malos de la población", "ok": True},
             {"txt": "La probabilidad de incumplimiento del cliente"},
             {"txt": "El puntaje mínimo para aprobar una solicitud"},
             {"txt": "La diferencia entre puntaje observado y esperado"},
         ],
         "retro": "El odds es una razón, no una probabilidad. Si hay veinte buenos por cada malo, "
                  "el odds es veinte a uno. La escala de puntos se construye sobre esa razón."},

        {"id": "b7", "puntaje": 10,
         "texto": "Riesgo recalibró la escala de la scorecard pero el sistema mantiene el punto de "
                  "corte anterior. ¿Cuál es el efecto?",
         "opciones": [
             {"txt": "Se están aprobando o rechazando solicitudes con un criterio distinto al que "
                     "fija la política vigente", "ok": True},
             {"txt": "Ninguno: la escala es solo presentación"},
             {"txt": "Mejora la aprobación porque la escala es más precisa"},
             {"txt": "Se corrige solo en el siguiente ciclo de monitoreo"},
         ],
         "retro": "La escala es una transformación, pero el punto de corte opera sobre la escala. "
                  "Si una cambia y el otro no, la política deja de aplicarse como está escrita."},

        {"id": "b8", "puntaje": 10,
         "texto": "El área bajo la curva es 0,86 en desarrollo y 0,74 en validación. ¿Qué "
                  "corresponde concluir?",
         "opciones": [
             {"txt": "Hay indicio de sobreajuste y se debe requerir explicación antes de aceptar el "
                     "modelo", "ok": True},
             {"txt": "El modelo es aceptable porque ambos valores superan 0,70"},
             {"txt": "La muestra de validación es demasiado pequeña"},
             {"txt": "Corresponde recalcular el information value de las variables"},
         ],
         "retro": "Doce puntos de caída exceden ampliamente el margen razonable. El desempeño real "
                  "esperable es el de validación, no el de desarrollo."},

        {"id": "b9", "puntaje": 10,
         "texto": "¿Cuál es el aporte de Lasso frente a Ridge en un modelo de riesgo?",
         "opciones": [
             {"txt": "Puede llevar coeficientes exactamente a cero, con lo que también selecciona "
                     "variables", "ok": True},
             {"txt": "Elimina la necesidad de muestra de validación"},
             {"txt": "Aumenta el information value de las variables incluidas"},
             {"txt": "Convierte la regresión logística en un modelo no paramétrico"},
         ],
         "retro": "Ambas penalizan coeficientes grandes para mejorar la generalización. Lasso "
                  "además anula coeficientes, por lo que reduce el número de variables."},

        {"id": "b10", "puntaje": 10,
         "texto": "La scorecard asigna puntos por sexo del solicitante. ¿Qué corresponde hacer?",
         "opciones": [
             {"txt": "Verificar si la normativa aplicable lo permite y si existe evaluación "
                     "documentada de trato diferenciado", "ok": True},
             {"txt": "Nada, si la variable tiene information value suficiente"},
             {"txt": "Eliminar la variable sin más análisis"},
             {"txt": "Reportarlo solo si algún cliente reclama"},
         ],
         "retro": "El uso de atributos protegidos es un riesgo regulatorio y reputacional. El poder "
                  "predictivo no sustituye la evaluación de admisibilidad legal."},
    ],
}
