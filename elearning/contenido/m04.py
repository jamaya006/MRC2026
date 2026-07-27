# -*- coding: utf-8 -*-
"""Modulo IV — Segmentacion y sus riesgos. Fuente: Clase 4."""

MODULO = {
    "ref": "D",
    "titulo": "Segmentación y sus riesgos",
    "proposito": "Entender cómo se construye una segmentación de cartera y por qué una "
                 "segmentación mal hecha contamina la provisión de todos los segmentos, no solo "
                 "del que está mal armado.",

    "cedulas": [
        {
            "ref": "D-1",
            "titulo": "Qué se busca al segmentar y por qué importa contablemente",
            "bloques": [
                ("p", "Segmentar es agrupar clientes u operaciones de modo que dentro de cada grupo "
                      "el comportamiento sea parecido y entre grupos sea distinto. No hay una "
                      "variable objetivo: es el algoritmo el que propone los grupos a partir de las "
                      "características observadas."),
                ("cita", "Dentro del clustering se busca el grupo para que se puedan diferenciar en "
                         "base a alguna caracterización que uno haga del grupo.",
                 "Clase 4, aprox. 00:04:51"),
                ("p", "El efecto contable es directo: en los modelos de pérdida esperada se estima "
                      "un conjunto de parámetros por segmento. Si los segmentos están mal "
                      "definidos, los parámetros se calculan sobre poblaciones heterogéneas y la "
                      "provisión resultante no refleja el riesgo de ninguna de ellas."),
                ("nota", "La pregunta de auditoría",
                 "¿La segmentación responde a diferencias reales de comportamiento de pago o a la "
                 "estructura comercial de la institución? Segmentar por línea de negocio es "
                 "cómodo para gestionar y frecuentemente inadecuado para provisionar."),
            ],
        },
        {
            "ref": "D-2",
            "titulo": "Distancia y tipo de algoritmo",
            "bloques": [
                ("p", "El primer elemento de una segmentación es la medida de distancia: el "
                      "criterio numérico para decidir si dos cuentas se parecen. Cambiar la medida "
                      "de distancia cambia los grupos, aun con los mismos datos."),
                ("cita", "Los elementos más importantes dentro de la segmentación son primero las "
                         "medidas de distancia o de proximidad, que son las medidas estadísticas o "
                         "numéricas que se van a utilizar para definir si una cuenta se parece a otra.",
                 "Clase 4, aprox. 00:03:49"),
                ("tabla", [
                    ["Familia", "Cómo agrupa", "Cuándo se usa"],
                    ["Jerárquico", "Aglomera o divide por orden de distancia", "Exploración, carteras pequeñas"],
                    ["No jerárquico (k-medias)", "Asigna a centroides y los recalcula", "Carteras grandes, producción"],
                ]),
                ("p", "Dentro de los métodos jerárquicos, el criterio de enlace también altera el "
                      "resultado: vecino más próximo, vecino más lejano, distancia del centroide o "
                      "método de Ward producen agrupaciones distintas sobre los mismos datos."),
                ("riesgo", "Qué sale mal",
                 "Las variables entran al algoritmo sin estandarizar. Una variable expresada en "
                 "pesos domina por completo la distancia frente a una expresada en meses, y los "
                 "grupos terminan definidos por la unidad de medida en lugar del comportamiento."),
                ("nota", "Procedimiento",
                 "Verificar que las variables fueron estandarizadas antes de calcular distancias y "
                 "que el criterio de estandarización está documentado. Es una revisión de dos "
                 "minutos que explica la mayoría de las segmentaciones sin sentido económico."),
            ],
        },
        {
            "ref": "D-3",
            "titulo": "Cuántos grupos: codo y silueta",
            "bloques": [
                ("p", "El número de grupos no lo entrega el algoritmo: lo elige quien construye el "
                      "modelo. Existen dos apoyos habituales para esa decisión, y ninguno de los "
                      "dos entrega una respuesta única."),
                ("cita", "Hay dos métodos que son los más comunes: el método del codo y el gráfico "
                         "de la silueta.",
                 "Clase 4, aprox. 00:49:55"),
                ("lista", [
                    "Codo: se grafica la variabilidad no explicada contra el número de grupos. La "
                    "curva desciende y en algún punto se aplana. Ese quiebre sugiere el número.",
                    "Silueta: mide, para cada caso, qué tan bien encaja en su grupo comparado con "
                    "el grupo más cercano. Valores altos indican grupos bien separados.",
                ]),
                ("umbral", "Criterio de revisión",
                 "El número elegido debe estar justificado por al menos uno de los dos métodos y "
                 "cada segmento debe contener volumen suficiente para estimar sus parámetros de "
                 "riesgo. Un segmento con muy pocos incumplimientos no permite estimar una "
                 "probabilidad de incumplimiento confiable, por más nítida que sea su separación."),
                ("riesgo", "Qué sale mal",
                 "Se elige el número de grupos que coincide con la estructura comercial existente, "
                 "y el gráfico del codo se agrega después como respaldo. La decisión es previa al "
                 "análisis y el análisis se usa como justificación."),
            ],
        },
        {
            "ref": "D-4",
            "titulo": "Cómo una segmentación mal hecha contamina la provisión",
            "bloques": [
                ("p", "El daño de una segmentación defectuosa no se queda en el segmento mal "
                      "armado. Si un grupo heterogéneo mezcla deudores de riesgo distinto, su "
                      "probabilidad de incumplimiento promedio subestima el riesgo de una parte y "
                      "lo sobreestima en la otra. La provisión total puede parecer razonable "
                      "mientras está mal distribuida entre carteras."),
                ("tabla", [
                    ["Situación", "Efecto en el parámetro", "Efecto en la provisión"],
                    ["Segmento heterogéneo", "PD promedio no representativa", "Mal distribuida entre carteras"],
                    ["Segmento con pocos casos", "PD inestable entre períodos", "Volatilidad no explicada del gasto"],
                    ["Segmentos superpuestos", "Doble conteo de comportamiento", "Riesgo de subprovisión"],
                    ["Reglas de asignación ambiguas", "Migración arbitraria entre segmentos", "Cambios de provisión sin cambio de riesgo"],
                ]),
                ("nota", "Procedimiento",
                 "Solicitar la regla de asignación de un cliente a su segmento y aplicarla sobre una "
                 "muestra. Verificar que un mismo cliente no pueda quedar en dos segmentos y que la "
                 "regla no dependa de campos que cambian por gestión comercial y no por riesgo."),
                ("riesgo", "Señal en los estados financieros",
                 "Un movimiento relevante del gasto por provisión sin cambio equivalente en la "
                 "morosidad observada suele originarse en migración de clientes entre segmentos, no "
                 "en deterioro real de la cartera."),
            ],
        },
        {
            "ref": "D-5",
            "titulo": "Estabilidad de los segmentos en el tiempo",
            "bloques": [
                ("p", "Una segmentación se construye sobre una foto de la cartera. La cartera cambia. "
                      "La pregunta que casi nunca está respondida en la documentación es cada cuánto "
                      "se revisa la segmentación y bajo qué criterio se rehace."),
                ("umbral", "Elementos que debe fijar la política",
                 "Frecuencia de revisión de la segmentación, indicador que dispara una "
                 "reconstrucción, procedimiento para tratar clientes que cambian de segmento y "
                 "responsable de aprobar el cambio."),
                ("riesgo", "Qué sale mal",
                 "La segmentación se rehace cada vez que el resultado no gusta, sin regla previa. "
                 "Reconstruir los grupos es una de las formas más eficaces de mover la provisión sin "
                 "que aparezca como un cambio de metodología."),
                ("nota", "Procedimiento",
                 "Comparar la composición de cada segmento entre dos cierres. Documentar el "
                 "porcentaje de clientes que cambió de segmento y contrastarlo contra el cambio "
                 "observado en el comportamiento de pago. Sin cambio de comportamiento, la "
                 "migración exige explicación."),
            ],
        },
    ],

    "banco": [
        {"id": "d1", "puntaje": 10,
         "texto": "¿Qué distingue a la segmentación de un modelo de score?",
         "opciones": [
             {"txt": "No hay variable objetivo: los grupos surgen de las características "
                     "observadas", "ok": True},
             {"txt": "La segmentación solo usa variables cualitativas"},
             {"txt": "La segmentación no requiere datos históricos"},
             {"txt": "El score no permite agrupar clientes"},
         ],
         "retro": "Es aprendizaje no supervisado. Nadie le dice al algoritmo qué es un buen o mal "
                  "cliente; el algoritmo propone agrupaciones."},

        {"id": "d2", "puntaje": 10,
         "texto": "Las variables entraron al algoritmo sin estandarizar: monto en pesos y "
                  "antigüedad en meses. ¿Cuál es la consecuencia?",
         "opciones": [
             {"txt": "El monto domina la distancia y los grupos quedan definidos por la unidad de "
                     "medida", "ok": True},
             {"txt": "Ninguna: el algoritmo estandariza internamente"},
             {"txt": "Se reduce el número óptimo de grupos"},
             {"txt": "Aumenta el valor de la silueta"},
         ],
         "retro": "Las distancias se calculan sobre las escalas originales. Una variable con valores "
                  "grandes absorbe la distancia total."},

        {"id": "d3", "puntaje": 10,
         "texto": "¿Qué muestra el gráfico del codo?",
         "opciones": [
             {"txt": "El punto donde agregar más grupos deja de reducir apreciablemente la "
                     "variabilidad no explicada", "ok": True},
             {"txt": "El grupo con mayor probabilidad de incumplimiento"},
             {"txt": "La correlación entre las variables usadas"},
             {"txt": "La estabilidad de los grupos en el tiempo"},
         ],
         "retro": "Es una curva descendente que se aplana. El quiebre sugiere el número de grupos, "
                  "pero es una sugerencia, no una respuesta única."},

        {"id": "d4", "puntaje": 10,
         "texto": "Un segmento quedó bien separado según la silueta, pero registra doce "
                  "incumplimientos en el período. ¿Qué corresponde observar?",
         "opciones": [
             {"txt": "El volumen es insuficiente para estimar una probabilidad de incumplimiento "
                     "confiable", "ok": True},
             {"txt": "Nada: la silueta valida el segmento"},
             {"txt": "Debe fusionarse con el segmento de mayor volumen"},
             {"txt": "Corresponde aumentar el número de grupos"},
         ],
         "retro": "La separación estadística no sustituye el volumen. Con pocos eventos la PD del "
                  "segmento será inestable entre períodos."},

        {"id": "d5", "puntaje": 10,
         "texto": "El gasto por provisión subió de forma relevante sin que la morosidad observada "
                  "cambiara. ¿Cuál es una causa a descartar primero?",
         "opciones": [
             {"txt": "Migración de clientes entre segmentos por cambios en la regla de asignación", "ok": True},
             {"txt": "Un error de suma en el estado de resultados"},
             {"txt": "Cambios en la tasa de interés de colocación"},
             {"txt": "Aumento del número de sucursales"},
         ],
         "retro": "Reasignar clientes a un segmento con parámetros distintos mueve la provisión sin "
                  "que exista deterioro real."},

        {"id": "d6", "puntaje": 10,
         "texto": "¿Por qué segmentar por línea de negocio puede ser inadecuado para provisionar?",
         "opciones": [
             {"txt": "Porque la estructura comercial no necesariamente coincide con diferencias "
                     "reales de comportamiento de pago", "ok": True},
             {"txt": "Porque las líneas de negocio cambian de nombre"},
             {"txt": "Porque los sistemas no permiten esa apertura"},
             {"txt": "Porque la norma exige segmentar solo por producto"},
         ],
         "retro": "La segmentación para provisión debe explicar riesgo. Que sea cómoda para "
                  "gestionar no la hace adecuada para estimar parámetros."},

        {"id": "d7", "puntaje": 10,
         "texto": "La documentación no indica cada cuánto se revisa la segmentación. ¿Cómo se "
                  "clasifica?",
         "opciones": [
             {"txt": "Deficiencia de gobierno del modelo: permite rehacer los grupos sin regla "
                     "previa", "ok": True},
             {"txt": "Observación de forma, sin efecto en la cifra"},
             {"txt": "No es observable si los segmentos funcionan"},
             {"txt": "Corresponde a la auditoría de sistemas"},
         ],
         "retro": "Sin frecuencia ni criterio de disparo, la reconstrucción queda a discreción y "
                  "puede usarse para mover la provisión."},

        {"id": "d8", "puntaje": 10,
         "texto": "¿Qué diferencia a un método jerárquico de uno no jerárquico?",
         "opciones": [
             {"txt": "El jerárquico agrupa progresivamente por orden de distancia; el no jerárquico "
                     "asigna a centroides que recalcula", "ok": True},
             {"txt": "El jerárquico no requiere medida de distancia"},
             {"txt": "El no jerárquico solo admite dos grupos"},
             {"txt": "El jerárquico es siempre más preciso"},
         ],
         "retro": "Son familias distintas. Los jerárquicos se usan más para explorar; los no "
                  "jerárquicos escalan mejor a carteras grandes."},

        {"id": "d9", "puntaje": 10,
         "texto": "La regla de asignación permite que un cliente cumpla condiciones de dos "
                  "segmentos. ¿Cuál es el riesgo?",
         "opciones": [
             {"txt": "La asignación queda determinada por el orden de ejecución y puede cambiar sin "
                     "que cambie el riesgo del cliente", "ok": True},
             {"txt": "El cliente recibe doble provisión"},
             {"txt": "Se pierde la trazabilidad contable de la operación"},
             {"txt": "El algoritmo deja de converger"},
         ],
         "retro": "Reglas ambiguas producen asignaciones dependientes de la implementación. Es un "
                  "hallazgo de diseño, no de sistemas."},

        {"id": "d10", "puntaje": 10,
         "texto": "¿Qué evidencia solicitaría para evaluar la estabilidad de la segmentación?",
         "opciones": [
             {"txt": "Composición de cada segmento en dos cierres y porcentaje de clientes que "
                     "migró, contrastado con el comportamiento de pago", "ok": True},
             {"txt": "El acta del comité que aprobó la segmentación"},
             {"txt": "El gráfico de silueta del período actual"},
             {"txt": "El listado de variables usadas"},
         ],
         "retro": "La estabilidad se evalúa comparando períodos. Migración alta sin cambio de "
                  "comportamiento es la señal a perseguir."},
    ],
}
