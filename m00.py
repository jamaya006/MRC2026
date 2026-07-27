# -*- coding: utf-8 -*-
"""Modulo 0 — Python para quien nunca ha programado. Fuente: preparado para el programa."""

MODULO = {
    "ref": "0",
    "titulo": "Python para quien nunca ha programado",
    "proposito": "Llegar a leer y modificar el código de los módulos siguientes sin haber "
                 "programado nunca. Empieza en la primera línea y no supone ningún "
                 "conocimiento previo. Si trabajas con Excel, ya sabes más de lo que crees.",

    "cedulas": [
        {
            "ref": "0-1",
            "titulo": "Por qué un contador debería tocar código",
            "bloques": [
                ("p", "No para programar. Para no depender de que otro te entregue el número "
                      "ya calculado. Cuando el equipo de riesgo dice que la provisión son "
                      "cuatro mil ochocientos millones, hay dos posiciones posibles: creerlo, "
                      "o rehacer el cálculo por tu cuenta."),
                ("p", "Con una planilla puedes revisar mil operaciones. La cartera tiene "
                      "cuatrocientas mil. Ese es todo el motivo."),
                ("tabla", [
                    ["Lo que haces en Excel", "Cómo se llama acá"],
                    ["Abrir un archivo", "Leer un CSV"],
                    ["Una hoja con filas y columnas", "Un DataFrame"],
                    ["Filtrar con autofiltro", "Filtrar por condición"],
                    ["Tabla dinámica", "Agrupar y resumir"],
                    ["Una fórmula en una columna nueva", "Crear una columna"],
                    ["BUSCARV", "Unir dos tablas"],
                ]),
                ("nota", "Lo que este módulo no es",
                 "No es un curso de programación. No vas a aprender a construir sistemas ni te "
                 "van a pedir que memorices nada. El objetivo es que puedas abrir el código de "
                 "un laboratorio, entender qué hace cada línea y cambiar un número para ver "
                 "qué pasa."),
            ],
        },
        {
            "ref": "0-2",
            "titulo": "Dónde escribir: no hay que instalar nada",
            "bloques": [
                ("p", "Existe una herramienta gratuita de Google llamada Colab. Se abre en el "
                      "navegador, como Gmail. No se instala nada en el computador y no hace "
                      "falta permiso del área de sistemas."),
                ("pasos", [
                    "Entra a colab.research.google.com con tu cuenta de Google.",
                    "Elige Archivo, luego Nuevo cuaderno.",
                    "Vas a ver un recuadro gris con un triángulo a la izquierda. Eso es una celda.",
                    "Escribe dentro de la celda y presiona el triángulo, o Control y Enter juntos.",
                ]),
                ("p", "El resultado aparece justo debajo de la celda. Una celda es como una "
                      "fórmula de Excel: escribes algo, lo ejecutas y ves el resultado. La "
                      "diferencia es que aquí puedes escribir varias instrucciones seguidas."),
                ("nota", "Sobre los datos del curso",
                 "Los laboratorios trabajan con una cartera sintética generada para el "
                 "programa. No contiene datos de ningún cliente real. Cuando apliques esto en un "
                 "encargo, la extracción del cliente se trata con las mismas reglas de "
                 "confidencialidad que cualquier otro papel de trabajo."),
            ],
        },
        {
            "ref": "0-3",
            "titulo": "Tu primera línea",
            "bloques": [
                ("p", "Empecemos por lo más simple que existe. Escribe esto en una celda y "
                      "ejecútalo."),
                ("codigo", "La primera línea",
                 """print("Hola")"""),
                ("p", "Debajo aparece la palabra Hola. Eso es todo lo que hace `print`: mostrar "
                      "en pantalla lo que le pongas entre paréntesis. Nada más. Lo vas a usar "
                      "durante todo el curso para ver resultados."),
                ("p", "Ahora algo con más sentido para nosotros:"),
                ("codigo", "Guardar un valor y usarlo",
                 """saldo = 1500000
tasa_provision = 0.032

provision = saldo * tasa_provision
print(provision)"""),
                ("p", "Resultado: 48000. Las tres primeras líneas guardan valores con un "
                      "nombre; a eso se le llama variable, y funciona como darle nombre a una "
                      "celda en Excel. La cuarta hace la multiplicación. La quinta la muestra."),
                ("nota", "Dos detalles que van a aparecer siempre",
                 "El signo igual no significa igualdad matemática: significa guarda esto con "
                 "este nombre. Y los decimales se escriben con punto, no con coma: 0.032, "
                 "nunca 0,032. La coma tiene otro uso en Python y confundirlas es el primer "
                 "error de todo el mundo."),
                ("codigo", "Mostrar un texto y un número juntos",
                 """print("La provisión es", provision)
print(f"La provisión es {provision:,.0f}")"""),
                ("p", "La segunda forma, con la f delante de las comillas, permite meter el "
                      "valor dentro del texto y darle formato. Los dos puntos y la coma le "
                      "piden separador de miles. Es la que se usa en los laboratorios."),
            ],
        },
        {
            "ref": "0-4",
            "titulo": "Una tabla: el DataFrame",
            "bloques": [
                ("p", "Una variable guarda un valor. Para trabajar con una cartera completa "
                      "hace falta algo que guarde una tabla entera. Eso es un DataFrame, y es "
                      "prácticamente una hoja de Excel dentro del programa."),
                ("p", "Viene en una caja de herramientas llamada pandas, que hay que pedir una "
                      "vez al principio:"),
                ("codigo", "Pedir la herramienta y crear una tabla pequeña",
                 """import pandas as pd

cartera = pd.DataFrame({
    "cliente": ["Ana", "Luis", "Marta", "Pedro"],
    "saldo":   [1500000, 820000, 3400000, 210000],
    "mora":    [0, 45, 0, 120],
})

print(cartera)"""),
                ("p", "La primera línea trae pandas y le pone el apodo pd, que es lo "
                      "acostumbrado. El resto arma la tabla: cada nombre entre comillas es una "
                      "columna, y la lista entre corchetes son sus valores. Al ejecutar, "
                      "aparece la tabla con sus cuatro filas."),
                ("codigo", "Mirar una columna y un resumen",
                 """print(cartera["saldo"])          # una columna completa
print(cartera["saldo"].sum())    # la suma
print(cartera["saldo"].mean())   # el promedio
print(cartera.shape)             # cuántas filas y columnas"""),
                ("nota", "Sobre el numeral",
                 "Todo lo que va después de un # es un comentario: Python lo ignora por "
                 "completo. Sirve para dejar anotado qué hace cada línea, igual que un "
                 "comentario en una celda de Excel. En los laboratorios del curso hay "
                 "comentarios en casi todas las líneas."),
            ],
        },
        {
            "ref": "0-5",
            "titulo": "Filtrar, crear columnas y agrupar",
            "bloques": [
                ("p", "Con estas tres operaciones se hace el noventa por ciento del trabajo. Son "
                      "el autofiltro, la fórmula en columna nueva y la tabla dinámica."),
                ("codigo", "Filtrar: quedarse con parte de las filas",
                 """morosos = cartera[cartera["mora"] > 30]
print(morosos)

# Se lee de adentro hacia afuera:
#   cartera["mora"] > 30   pregunta fila por fila si la mora pasa de 30
#   cartera[ ... ]         se queda solo con las filas donde la respuesta fue sí"""),
                ("codigo", "Crear una columna nueva",
                 """cartera["etapa"] = 1
cartera.loc[cartera["mora"] >= 30, "etapa"] = 2
cartera.loc[cartera["mora"] >= 90, "etapa"] = 3

print(cartera)

# La primera línea pone 1 en toda la columna.
# Las dos siguientes sobrescriben solo las filas que cumplen la condición.
# El orden importa: 90 días se evalúa después, así que gana sobre 30."""),
                ("codigo", "Agrupar: la tabla dinámica",
                 """resumen = cartera.groupby("etapa").agg(
    operaciones=("saldo", "size"),   # cuántas filas hay en cada etapa
    exposicion=("saldo", "sum"),     # cuánto suman
    saldo_medio=("saldo", "mean"),   # el promedio
)
print(resumen)"""),
                ("p", "Esa es exactamente la tabla dinámica: agrupar por etapa y pedir tres "
                      "cálculos. La única diferencia es que aquí queda escrito, así que cualquiera "
                      "puede revisar cómo se obtuvo y repetirlo el mes siguiente."),
                ("nota", "Por qué importa para auditoría",
                 "Un resultado de Excel no dice cómo se llegó a él: hay que reconstruir las "
                 "fórmulas celda por celda. Un bloque de código es el procedimiento escrito. "
                 "Esa es la razón de fondo por la que la evidencia en código es mejor papel de "
                 "trabajo que una planilla."),
            ],
        },
        {
            "ref": "0-6",
            "titulo": "Leer el archivo del curso y ejecutar el primer control",
            "bloques": [
                ("p", "Hasta ahora la tabla la escribimos a mano. Lo normal es leerla de un "
                      "archivo. Con esto ya puedes hacer todos los laboratorios del programa."),
                ("codigo", "Leer un archivo y mirarlo",
                 """import pandas as pd

cartera = pd.read_csv("cartera.csv")

print(cartera.shape)     # cuántas filas y columnas trae
print(cartera.head())    # las primeras cinco filas
print(cartera.columns)   # los nombres de las columnas"""),
                ("p", "En Colab, el archivo se sube con el icono de carpeta del panel izquierdo. "
                      "Se arrastra ahí y queda disponible con solo su nombre."),
                ("codigo", "El primer control de auditoría, completo",
                 """# ¿Hay saldos negativos donde no debería haberlos?
negativos = cartera[cartera["saldo"] < 0]
print(f"Saldos negativos: {len(negativos)}")

# ¿Hay operaciones duplicadas?
duplicados = cartera["id_operacion"].duplicated().sum()
print(f"Identificadores repetidos: {duplicados}")

# ¿Hay campos vacíos en las columnas que alimentan el modelo?
print(cartera[["saldo", "dias_mora", "renta"]].isna().sum())"""),
                ("nota", "Esto ya es un papel de trabajo",
                 "Tres controles de integridad sobre la cartera completa, en nueve líneas, "
                 "repetibles y revisables por un tercero. Es el mismo procedimiento que harías "
                 "sobre una muestra, aplicado al cien por ciento de la población."),
                ("riesgo", "Un aviso honesto",
                 "Vas a equivocarte y el programa va a mostrar mensajes de error en rojo. Es "
                 "normal y no rompe nada. Casi siempre es una comilla sin cerrar, un paréntesis "
                 "de más o el nombre de una columna mal escrito. La última línea del mensaje es "
                 "la que dice qué pasó."),
            ],
        },
    ],

    "banco": [
        {"id": "z1", "puntaje": 10,
         "texto": "¿Qué hace la instrucción print?",
         "opciones": [
             {"txt": "Muestra en pantalla lo que se le pase entre paréntesis", "ok": True},
             {"txt": "Envía el contenido a la impresora"},
             {"txt": "Guarda el resultado en un archivo"},
             {"txt": "Calcula una suma"},
         ],
         "retro": "Solo muestra. Es la forma de ver qué está pasando dentro del programa."},

        {"id": "z2", "puntaje": 10,
         "texto": "En Python, ¿cómo se escribe tres coma dos por ciento como decimal?",
         "opciones": [
             {"txt": "0.032", "ok": True},
             {"txt": "0,032"},
             {"txt": "3,2%"},
             {"txt": "3.2%"},
         ],
         "retro": "Con punto. La coma tiene otro uso en Python, y confundirlas es el error más "
                  "frecuente al empezar."},

        {"id": "z3", "puntaje": 10,
         "texto": "¿Qué es un DataFrame?",
         "opciones": [
             {"txt": "Una tabla con filas y columnas dentro del programa, equivalente a una hoja "
                     "de cálculo", "ok": True},
             {"txt": "Un archivo guardado en el disco"},
             {"txt": "Un tipo de gráfico"},
             {"txt": "Una conexión a la base de datos"},
         ],
         "retro": "Es la estructura sobre la que se trabaja todo el curso. Piensa en una hoja de "
                  "Excel que vive dentro del programa."},

        {"id": "z4", "puntaje": 10,
         "texto": "¿Qué significa el símbolo # al principio de una línea?",
         "opciones": [
             {"txt": "Es un comentario: Python ignora esa línea por completo", "ok": True},
             {"txt": "Marca la línea como importante"},
             {"txt": "Indica que la línea tiene un error"},
             {"txt": "Convierte el texto en título"},
         ],
         "retro": "Sirve para dejar anotado qué hace cada paso. No afecta la ejecución."},

        {"id": "z5", "puntaje": 10,
         "texto": "¿Qué operación de Excel equivale a groupby con agg?",
         "opciones": [
             {"txt": "La tabla dinámica", "ok": True},
             {"txt": "BUSCARV"},
             {"txt": "El autofiltro"},
             {"txt": "Formato condicional"},
         ],
         "retro": "Agrupar por una columna y pedir cálculos sobre las demás es exactamente lo "
                  "que hace una tabla dinámica."},

        {"id": "z6", "puntaje": 10,
         "texto": "¿Qué hace `cartera[cartera[\"mora\"] > 30]`?",
         "opciones": [
             {"txt": "Se queda solo con las filas cuya mora supera los treinta días", "ok": True},
             {"txt": "Cambia el valor de la mora a 30"},
             {"txt": "Ordena la tabla por días de mora"},
             {"txt": "Cuenta cuántas operaciones tienen mora"},
         ],
         "retro": "Es el autofiltro. La condición se evalúa fila por fila y quedan las que "
                  "responden que sí."},

        {"id": "z7", "puntaje": 10,
         "texto": "En el bloque de clasificación por etapa, ¿por qué la línea de 90 días va "
                  "después de la de 30?",
         "opciones": [
             {"txt": "Porque se ejecutan en orden y la última sobrescribe a la anterior en las "
                     "filas que cumplen ambas", "ok": True},
             {"txt": "Porque 90 es mayor que 30"},
             {"txt": "Porque Python ordena las condiciones automáticamente"},
             {"txt": "Por costumbre, el orden no afecta el resultado"},
         ],
         "retro": "Una operación con 120 días de mora cumple ambas condiciones. Como la de 90 se "
                  "ejecuta después, queda en etapa 3. Invertir el orden cambia el resultado."},

        {"id": "z8", "puntaje": 10,
         "texto": "Aparece un mensaje de error en rojo al ejecutar una celda. ¿Qué corresponde "
                  "hacer?",
         "opciones": [
             {"txt": "Leer la última línea del mensaje, que indica qué ocurrió, y revisar comillas, "
                     "paréntesis y nombres de columna", "ok": True},
             {"txt": "Reiniciar el computador"},
             {"txt": "Volver a escribir todo el cuaderno desde el principio"},
             {"txt": "Ignorarlo y seguir con la celda siguiente"},
         ],
         "retro": "El error no rompe nada. La última línea del mensaje es la informativa; el resto "
                  "es el recorrido interno."},

        {"id": "z9", "puntaje": 10,
         "texto": "¿Por qué un bloque de código es mejor papel de trabajo que una planilla?",
         "opciones": [
             {"txt": "Porque deja el procedimiento escrito y cualquiera puede revisarlo y "
                     "repetirlo", "ok": True},
             {"txt": "Porque es más rápido de ejecutar"},
             {"txt": "Porque ocupa menos espacio en disco"},
             {"txt": "Porque no admite errores de cálculo"},
         ],
         "retro": "En una planilla hay que reconstruir las fórmulas celda por celda. El código es "
                  "el procedimiento explícito, y esa es la ventaja para auditoría."},

        {"id": "z10", "puntaje": 10,
         "texto": "¿Qué se necesita instalar en el computador para hacer los laboratorios del "
                  "programa?",
         "opciones": [
             {"txt": "Nada: Colab funciona en el navegador con una cuenta de Google", "ok": True},
             {"txt": "Python y un editor de código"},
             {"txt": "Una máquina virtual con Linux"},
             {"txt": "Una licencia del software estadístico"},
         ],
         "retro": "Se abre en el navegador como cualquier página. No requiere permisos del área de "
                  "sistemas."},
    ],
}
