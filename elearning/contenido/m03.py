# -*- coding: utf-8 -*-
"""Modulo III — Modelos alternativos y criterio de aceptacion. Fuente: Clases 2 y 5."""

MODULO = {
    "ref": "C",
    "titulo": "Modelos alternativos y criterio de aceptación",
    "proposito": "Decidir cuándo un modelo más complejo que la regresión logística se justifica y "
                 "cuándo es un riesgo. El criterio no es cuál predice mejor, sino cuál se puede "
                 "explicar, reproducir y monitorear.",

    "cedulas": [
        {
            "ref": "C-1",
            "titulo": "Por qué aparecen los árboles y qué cambian",
            "bloques": [
                ("p", "La regresión logística impone una forma: el efecto de cada variable es "
                      "monótono y se suma al de las demás. Un árbol de decisión no impone esa "
                      "forma. Divide la población en grupos mediante cortes sucesivos y captura "
                      "interacciones que la logística solo reproduce si alguien las declara "
                      "explícitamente."),
                ("p", "Esa flexibilidad tiene un costo. Un árbol profundo puede separar casi "
                      "perfectamente la muestra de desarrollo y perder gran parte de ese desempeño "
                      "fuera de ella. Es el mismo sobreajuste del módulo anterior, con más "
                      "capacidad de producirlo."),
                ("nota", "Lo que cambia para el auditor",
                 "En una logística se revisa el signo y la magnitud de cada coeficiente. En un "
                 "árbol no hay coeficientes: se revisa la estructura de cortes, la profundidad, el "
                 "mínimo de casos por hoja y la estabilidad de esas reglas entre muestras."),
            ],
        },
        {
            "ref": "C-2",
            "titulo": "Bagging y boosting: qué se gana y qué se pierde",
            "bloques": [
                ("p", "Un árbol solo es inestable. Las técnicas de ensamble combinan muchos árboles "
                      "para estabilizar el resultado. Bagging los entrena en paralelo sobre "
                      "remuestreos y promedia; boosting los entrena en secuencia, cada uno "
                      "corrigiendo los errores del anterior."),
                ("tabla", [
                    ["Enfoque", "Cómo combina", "Fortaleza", "Riesgo dominante"],
                    ["Árbol único", "No combina", "Reglas legibles", "Inestabilidad"],
                    ["Bagging", "Promedio en paralelo", "Reduce varianza", "Pierde legibilidad"],
                    ["Boosting", "Secuencial y ponderado", "Mayor desempeño", "Sobreajuste y sensibilidad al ruido"],
                ]),
                ("riesgo", "Qué sale mal",
                 "Boosting persigue los errores de los pasos anteriores. Si la muestra contiene "
                 "registros con errores de carga o períodos anómalos, el modelo dedica capacidad a "
                 "ajustar precisamente esos casos. El resultado luce mejor en desarrollo y se "
                 "deteriora rápido en producción."),
                ("nota", "Procedimiento",
                 "Antes de evaluar el desempeño de un ensamble, revisar la depuración de la muestra. "
                 "Un modelo de boosting sobre datos sucios amplifica la suciedad en lugar de "
                 "promediarla."),
            ],
        },
        {
            "ref": "C-3",
            "titulo": "Interpretabilidad: el requisito que no es negociable",
            "bloques": [
                ("p", "Una institución debe poder explicar por qué rechazó una solicitud, tanto al "
                      "cliente como al supervisor. Un modelo cuya decisión no se puede descomponer "
                      "en razones concretas genera un problema operativo antes que estadístico."),
                ("p", "La regresión logística con scorecard resuelve esto de forma natural: el "
                      "puntaje es una suma de puntos atribuibles a atributos concretos. Un ensamble "
                      "de cientos de árboles requiere herramientas adicionales de atribución, y esas "
                      "herramientas son aproximaciones, no la decisión real del modelo."),
                ("riesgo", "Qué sale mal",
                 "La institución adopta un modelo de mayor desempeño y mantiene la scorecard "
                 "anterior solo para explicar decisiones. Se termina con dos modelos: uno que "
                 "decide y otro que justifica. La explicación entregada al cliente no corresponde "
                 "al criterio que se aplicó."),
                ("nota", "Procedimiento",
                 "Verificar que el modelo que produce la decisión es el mismo que genera la razón "
                 "de rechazo comunicada. Solicitar diez casos rechazados y reconstruir la razón "
                 "entregada al cliente desde la salida del modelo en producción."),
            ],
        },
        {
            "ref": "C-4",
            "titulo": "Criterio de aceptación de un modelo más complejo",
            "bloques": [
                ("p", "La pregunta no es si el modelo complejo predice mejor. Casi siempre predice "
                      "algo mejor en la muestra de desarrollo. La pregunta es si esa mejora "
                      "sobrevive en validación y si compensa el costo de explicarlo, mantenerlo y "
                      "monitorearlo."),
                ("umbral", "Regla de decisión propuesta",
                 "Se acepta el modelo más complejo si la mejora de área bajo la curva en la muestra "
                 "de validación, no en desarrollo, supera tres puntos porcentuales y se mantiene "
                 "en una ventana fuera de tiempo. Por debajo de eso, la ganancia no compensa la "
                 "pérdida de interpretabilidad."),
                ("pasos", [
                    "Comparar ambos modelos sobre exactamente la misma muestra de validación.",
                    "Verificar que la partición de datos fue idéntica y con la misma semilla.",
                    "Repetir la comparación sobre una ventana temporal posterior.",
                    "Estimar el efecto de la diferencia sobre la provisión, no solo sobre la métrica.",
                    "Documentar la decisión y los responsables que la aprobaron.",
                ]),
                ("riesgo", "Qué sale mal",
                 "Se comparan modelos evaluados sobre muestras distintas o con particiones "
                 "diferentes. La comparación no es válida y la decisión de reemplazo queda sin "
                 "sustento."),
            ],
        },
        {
            "ref": "C-5",
            "titulo": "Reproducibilidad: el hallazgo más frecuente",
            "bloques": [
                ("p", "Un modelo de aprendizaje automático depende de una semilla aleatoria, de "
                      "versiones específicas de librerías y del orden de los datos de entrada. Si "
                      "alguno de esos elementos no está documentado, el modelo no se puede "
                      "reproducir y, por lo tanto, no se puede validar de forma independiente."),
                ("umbral", "Elementos mínimos del expediente del modelo",
                 "Semilla utilizada, versión del lenguaje y de cada librería, criterio y semilla de "
                 "la partición de la muestra, hiperparámetros finales, fecha de extracción de los "
                 "datos y responsable de cada paso."),
                ("nota", "Procedimiento",
                 "Ejecutar de nuevo el modelo con el expediente entregado y comparar la salida con "
                 "la reportada. Diferencias en el cuarto decimal son normales; diferencias en la "
                 "métrica de desempeño indican que el expediente está incompleto."),
                ("riesgo", "Qué sale mal",
                 "El modelo se entrenó en el equipo de un analista que ya no está en la "
                 "institución, con versiones de librerías que nadie registró. El modelo sigue "
                 "operando y nadie puede reconstruirlo. Es una observación de continuidad "
                 "operacional, además de una limitación al alcance de la validación."),
            ],
        },
    ],

    "banco": [
        {"id": "c1", "puntaje": 10,
         "texto": "¿Cuál es la diferencia estructural entre una regresión logística y un árbol de "
                  "decisión?",
         "opciones": [
             {"txt": "El árbol captura interacciones entre variables sin que haya que declararlas, "
                     "mientras la logística requiere especificarlas", "ok": True},
             {"txt": "El árbol siempre tiene mejor desempeño"},
             {"txt": "La logística no admite variables categóricas"},
             {"txt": "El árbol no requiere muestra de validación"},
         ],
         "retro": "La logística impone efectos aditivos y monótonos. El árbol no, y por eso captura "
                  "interacciones, pero también sobreajusta con más facilidad."},

        {"id": "c2", "puntaje": 10,
         "texto": "¿Por qué el boosting es especialmente sensible a la calidad de los datos?",
         "opciones": [
             {"txt": "Porque cada iteración se concentra en los errores de la anterior, y los "
                     "registros erróneos se comportan como errores a corregir", "ok": True},
             {"txt": "Porque no admite variables continuas"},
             {"txt": "Porque promedia los resultados y diluye la señal"},
             {"txt": "Porque requiere más memoria que otras técnicas"},
         ],
         "retro": "El algoritmo pondera lo que no logró ajustar. Datos sucios reciben más atención, "
                  "no menos, y el modelo termina ajustando ruido."},

        {"id": "c3", "puntaje": 10,
         "texto": "La institución decide con un modelo de boosting y explica los rechazos con la "
                  "scorecard anterior. ¿Cuál es el hallazgo?",
         "opciones": [
             {"txt": "La razón comunicada al cliente no corresponde al criterio que efectivamente "
                     "se aplicó", "ok": True},
             {"txt": "No hay hallazgo si ambas herramientas fueron aprobadas por el comité"},
             {"txt": "El hallazgo es que la scorecard está desactualizada"},
             {"txt": "Es una buena práctica de doble control"},
         ],
         "retro": "Decidir con un modelo y justificar con otro deja a la institución sin capacidad "
                  "real de explicar sus decisiones ante el cliente o el supervisor."},

        {"id": "c4", "puntaje": 10,
         "texto": "Un modelo complejo mejora el área bajo la curva de 0,81 a 0,88 en desarrollo y "
                  "de 0,78 a 0,79 en validación. ¿Qué corresponde recomendar?",
         "opciones": [
             {"txt": "No adoptarlo: la mejora real es de un punto y no compensa la pérdida de "
                     "interpretabilidad", "ok": True},
             {"txt": "Adoptarlo por la mejora de siete puntos"},
             {"txt": "Adoptarlo y revisar la validación más adelante"},
             {"txt": "Rehacer el desarrollo con más variables"},
         ],
         "retro": "La mejora en desarrollo es sobreajuste. Lo que se puede esperar en producción es "
                  "el resultado de validación: un punto porcentual."},

        {"id": "c5", "puntaje": 10,
         "texto": "Al comparar dos modelos candidatos, ¿qué condición hace inválida la comparación?",
         "opciones": [
             {"txt": "Que se hayan evaluado sobre muestras de validación distintas o con "
                     "particiones diferentes", "ok": True},
             {"txt": "Que uno sea logística y el otro un ensamble"},
             {"txt": "Que uno use más variables que el otro"},
             {"txt": "Que se hayan entrenado en fechas distintas"},
         ],
         "retro": "Sin la misma muestra y la misma partición, la diferencia de métricas puede "
                  "deberse a la muestra y no al modelo."},

        {"id": "c6", "puntaje": 10,
         "texto": "¿Qué elemento es imprescindible en el expediente para poder replicar un modelo?",
         "opciones": [
             {"txt": "La semilla aleatoria y las versiones de las librerías utilizadas", "ok": True},
             {"txt": "El nombre comercial del software"},
             {"txt": "El acta del comité que lo aprobó"},
             {"txt": "El presupuesto del proyecto"},
         ],
         "retro": "Sin semilla ni versiones, la ejecución no es reproducible y la validación "
                  "independiente pierde su base."},

        {"id": "c7", "puntaje": 10,
         "texto": "El validador reproduce el modelo y obtiene área bajo la curva de 0,74 frente al "
                  "0,82 reportado. ¿Cuál es la conclusión inmediata?",
         "opciones": [
             {"txt": "El expediente entregado está incompleto y hay una limitación al alcance", "ok": True},
             {"txt": "El modelo original está mal y debe descartarse"},
             {"txt": "Es una diferencia normal por aleatoriedad"},
             {"txt": "Corresponde ajustar la semilla hasta igualar el resultado"},
         ],
         "retro": "Ajustar la semilla hasta reproducir el número es exactamente lo contrario de "
                  "validar. La diferencia indica que falta información en el expediente."},

        {"id": "c8", "puntaje": 10,
         "texto": "¿Qué se revisa en un árbol que no tiene equivalente en una regresión logística?",
         "opciones": [
             {"txt": "La profundidad, el mínimo de casos por hoja y la estabilidad de los cortes", "ok": True},
             {"txt": "El signo de los coeficientes"},
             {"txt": "El information value de cada variable"},
             {"txt": "El intercepto del modelo"},
         ],
         "retro": "Un árbol no tiene coeficientes. Su control de complejidad está en la profundidad "
                  "y en el tamaño mínimo de las hojas."},

        {"id": "c9", "puntaje": 10,
         "texto": "El analista que construyó el modelo dejó la institución y nadie registró el "
                  "entorno de ejecución. El modelo sigue operando. ¿Cómo se reporta?",
         "opciones": [
             {"txt": "Como observación de continuidad operacional y limitación al alcance de la "
                     "validación", "ok": True},
             {"txt": "Como observación de recursos humanos"},
             {"txt": "No se reporta mientras el modelo funcione"},
             {"txt": "Como deficiencia estadística del modelo"},
         ],
         "retro": "El modelo puede ser estadísticamente correcto y aun así representar un riesgo "
                  "operacional: no se puede mantener, corregir ni validar."},

        {"id": "c10", "puntaje": 10,
         "texto": "¿Qué aporta el bagging respecto de un árbol único?",
         "opciones": [
             {"txt": "Reduce la varianza del resultado al promediar árboles entrenados sobre "
                     "remuestreos", "ok": True},
             {"txt": "Aumenta la interpretabilidad del modelo"},
             {"txt": "Elimina la necesidad de tramificar variables"},
             {"txt": "Garantiza que no exista sobreajuste"},
         ],
         "retro": "El bagging estabiliza. Lo que gana en varianza lo pierde en legibilidad: ya no "
                  "hay un conjunto único de reglas que mostrar."},
    ],
}
