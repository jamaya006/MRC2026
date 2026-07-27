# -*- coding: utf-8 -*-
"""
Laboratorios del programa MRC-2026.

Un laboratorio por modulo, todos en Python. Se anexan como ultima cedula
durante la generacion, de modo que el contenido conceptual y el trabajo
aplicado se mantienen en archivos separados.

Entorno de referencia: Python 3.11, pandas, numpy, scikit-learn, matplotlib.
"""

LABS = {

# ------------------------------------------------------------------ M01
"M01": {
 "ref": "A-7",
 "titulo": "Laboratorio: construir las ventanas y medir la tasa base",
 "bloques": [
  ("p", "Todo el programa trabaja sobre la misma cartera sintética. El primer "
        "ejercicio arma las dos ventanas y obtiene la tasa de incumplimiento, que es "
        "el número contra el cual se comparará todo lo demás."),
  ("codigo", "Ventanas de observación y desempeño",
   """import pandas as pd

cartera = pd.read_csv("cartera.csv",
                      parse_dates=["fecha_originacion", "fecha_default"])

# Ventana de observación: originaciones del período de construcción
obs = cartera[cartera.fecha_originacion.between("2022-01-01", "2022-12-31")].copy()

# Ventana de desempeño: doce meses posteriores a cada originación
obs["fin_desempeno"] = obs.fecha_originacion + pd.DateOffset(months=12)
obs["malo"] = (obs.fecha_default.notna() &
               (obs.fecha_default <= obs.fin_desempeno)).astype(int)

print(f"Operaciones            {len(obs):>10,}")
print(f"Tasa de incumplimiento {obs.malo.mean():>10.2%}")

# Control: ninguna fecha de incumplimiento puede preceder a la originación
con_default = obs[obs.fecha_default.notna()]
assert (con_default.fecha_default >= con_default.fecha_originacion).all()"""),
  ("nota", "Lo que hay que mirar",
   "La tasa de incumplimiento del período de construcción es el punto de comparación "
   "para el resto del programa. Anótala: si difiere de la de los períodos vecinos, esa "
   "diferencia es el primer indicio de una ventana contaminada."),
 ],
},

# ------------------------------------------------------------------ M02
"M02": {
 "ref": "B-7",
 "titulo": "Laboratorio: calcular WOE e information value",
 "bloques": [
  ("p", "La función siguiente reproduce lo que hace cualquier herramienta comercial de "
        "scorecard. Escribirla una vez sirve para saber exactamente qué se está "
        "revisando cuando el equipo de riesgo entrega una tabla de WOE."),
  ("codigo", "WOE e IV por variable",
   """import numpy as np
import pandas as pd

def woe_iv(df, variable, objetivo="malo", tramos=5):
    d = df[[variable, objetivo]].copy()
    if d[variable].dtype.kind in "ifc":
        d["tramo"] = pd.qcut(d[variable], tramos, duplicates="drop")
    else:
        d["tramo"] = d[variable]

    t = d.groupby("tramo", observed=True)[objetivo].agg(["count", "sum"])
    t.columns = ["total", "malos"]
    t["buenos"] = t.total - t.malos

    # Corrección de continuidad: evita el logaritmo de cero en tramos sin eventos
    t["p_buenos"] = (t.buenos + 0.5) / (t.buenos.sum() + 0.5 * len(t))
    t["p_malos"] = (t.malos + 0.5) / (t.malos.sum() + 0.5 * len(t))

    t["woe"] = np.log(t.p_buenos / t.p_malos)
    t["iv"] = (t.p_buenos - t.p_malos) * t.woe
    t["participacion"] = t.total / t.total.sum()
    return t, t.iv.sum()

tabla, iv = woe_iv(desarrollo, "antiguedad_meses")
print(tabla[["total", "participacion", "woe", "iv"]].round(4))
print(f"IV total = {iv:.4f}")"""),
  ("codigo", "Los dos controles de la cédula B-3 y B-4",
   """# Control 1: ningún tramo bajo el 5 % de la población
chicos = tabla[tabla.participacion < 0.05]
if len(chicos):
    print("Tramos con volumen insuficiente:")
    print(chicos[["total", "participacion"]])

# Control 2: information value sospechosamente alto
if iv > 0.50:
    print(f"ALERTA IV={iv:.3f}: verificar cuándo queda disponible esta variable "
          f"frente a la fecha de la decisión de crédito")

# Control 3: monotonía del WOE
if not (tabla.woe.is_monotonic_increasing or tabla.woe.is_monotonic_decreasing):
    print("El WOE no es monótono: requerir justificación de negocio")"""),
  ("riesgo", "Sobre el binning automático",
   "Las rutinas de binning óptimo maximizan el IV en la muestra de desarrollo y tienden "
   "a producir demasiados tramos. Si se usa una, hay que fijar el número máximo de "
   "tramos y el tamaño mínimo por tramo antes de ejecutarla, no después de ver el "
   "resultado."),
 ],
},

# ------------------------------------------------------------------ M03
"M03": {
 "ref": "C-6",
 "titulo": "Laboratorio: comparar dos modelos con criterio",
 "bloques": [
  ("p", "La comparación solo es válida si ambos modelos ven exactamente la misma "
        "partición. El código fija la semilla una vez y la reutiliza, que es la "
        "condición que la cédula C-4 exige verificar."),
  ("codigo", "Comparación sobre partición idéntica",
   """from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score

SEMILLA = 20260722          # queda registrada en el expediente del modelo

X_tr, X_va, y_tr, y_va = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=SEMILLA)

candidatos = {
    "Logística": LogisticRegression(max_iter=1000),
    "Boosting":  GradientBoostingClassifier(random_state=SEMILLA),
}

for nombre, modelo in candidatos.items():
    modelo.fit(X_tr, y_tr)
    auc_des = roc_auc_score(y_tr, modelo.predict_proba(X_tr)[:, 1])
    auc_val = roc_auc_score(y_va, modelo.predict_proba(X_va)[:, 1])
    print(f"{nombre:<11} desarrollo {auc_des:.3f}   "
          f"validación {auc_val:.3f}   caída {auc_des - auc_val:+.3f}")"""),
  ("nota", "Cómo se lee el resultado",
   "Lo que decide la adopción es la columna de validación, no la de desarrollo. La "
   "caída de cada modelo, por separado, indica cuánto sobreajustó. Un boosting con "
   "caída de 0,10 y una logística con caída de 0,02 dicen más sobre el riesgo del "
   "modelo que la diferencia entre ambos."),
  ("codigo", "Registro de reproducibilidad",
   """import sys, sklearn, pandas, numpy

print(f"Python       {sys.version.split()[0]}")
print(f"scikit-learn {sklearn.__version__}")
print(f"pandas       {pandas.__version__}")
print(f"numpy        {numpy.__version__}")
print(f"Semilla      {SEMILLA}")
# Esta salida se adjunta al expediente: sin ella no hay validación replicable"""),
 ],
},

# ------------------------------------------------------------------ M04
"M04": {
 "ref": "D-6",
 "titulo": "Laboratorio: segmentar y evaluar la elección de k",
 "bloques": [
  ("p", "El ejercicio incluye la estandarización, que es el paso que se omite con más "
        "frecuencia y el que explica la mayoría de las segmentaciones sin sentido "
        "económico."),
  ("codigo", "Estandarizar, elegir k y perfilar",
   """from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

SEMILLA = 20260722
variables = ["monto_original", "antiguedad_meses", "carga_financiera", "renta"]

# Sin estandarizar, el monto en pesos domina por completo la distancia
Z = StandardScaler().fit_transform(cartera[variables])

for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=SEMILLA).fit(Z)
    print(f"k={k}   inercia {km.inertia_:>12,.0f}   "
          f"silueta {silhouette_score(Z, km.labels_):.3f}")"""),
  ("codigo", "Perfil de riesgo por segmento",
   """km = KMeans(n_clusters=4, n_init=10, random_state=SEMILLA).fit(Z)
cartera["segmento"] = km.labels_

perfil = cartera.groupby("segmento").agg(
    operaciones=("malo", "size"),
    incumplimientos=("malo", "sum"),
    tasa=("malo", "mean"),
    monto_medio=("monto_original", "mean"))
print(perfil.round(4))

# Control de la cédula D-3: volumen suficiente para estimar una PD
insuficientes = perfil[perfil.incumplimientos < 30]
if len(insuficientes):
    print("Segmentos sin eventos suficientes para estimar PD confiable:")
    print(insuficientes)"""),
  ("umbral", "Criterio del laboratorio",
   "Un segmento con menos de treinta incumplimientos no permite estimar una "
   "probabilidad estable entre períodos, por nítida que sea su separación en el "
   "gráfico de silueta."),
 ],
},

# ------------------------------------------------------------------ M05
"M05": {
 "ref": "E-6",
 "titulo": "Laboratorio: métricas, punto de corte y calibración",
 "bloques": [
  ("p", "Tres bloques que producen la cédula de desempeño completa: discriminación, "
        "corte económico y tabla de calibración."),
  ("codigo", "Discriminación",
   """import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix

p = modelo.predict_proba(X_va)[:, 1]
fpr, tpr, cortes = roc_curve(y_va, p)

auc = roc_auc_score(y_va, p)
ks = (tpr - fpr).max()
corte_ks = cortes[(tpr - fpr).argmax()]

print(f"AUC   {auc:.3f}")
print(f"Gini  {2 * auc - 1:.3f}      (es la misma medida que el AUC)")
print(f"KS    {ks:.1%}  en probabilidad {corte_ks:.3f}")"""),
  ("codigo", "Punto de corte de mínimo costo",
   """PERDIDA = 1.00      # por unidad de exposición incumplida
MARGEN  = 0.12      # por unidad de exposición sana

rejilla = np.arange(0.01, 0.51, 0.01)
costo = [((y_va == 1) & (p < c)).sum() * PERDIDA +
         ((y_va == 0) & (p >= c)).sum() * MARGEN for c in rejilla]

optimo = rejilla[int(np.argmin(costo))]
print(f"Corte de mínimo costo: {optimo:.0%}")
print(confusion_matrix(y_va, (p >= optimo).astype(int)))
# El corte queda muy por debajo del 50 % porque los errores no cuestan igual"""),
  ("codigo", "Calibración: la evidencia que sostiene la provisión",
   """import pandas as pd

cal = pd.DataFrame({"pd_estimada": p, "observado": y_va})
cal["tramo"] = pd.qcut(cal.pd_estimada, 5,
                       labels=["muy bajo", "bajo", "medio", "alto", "muy alto"])

tabla = cal.groupby("tramo", observed=True).agg(
    operaciones=("observado", "size"),
    pd_estimada=("pd_estimada", "mean"),
    observado=("observado", "mean"))
tabla["desvio"] = tabla.observado - tabla.pd_estimada
print(tabla.round(4))

if (tabla.desvio > 0).all():
    print("El modelo subestima en todos los tramos: la provisión queda corta")"""),
 ],
},

# ------------------------------------------------------------------ M06
"M06": {
 "ref": "F-6",
 "titulo": "Laboratorio: función de PSI reutilizable",
 "bloques": [
  ("p", "Esta función es el entregable del módulo. Sirve tanto para el puntaje como "
        "para cualquier variable de entrada, y devuelve el detalle por tramo, que es lo "
        "que el total puede ocultar."),
  ("codigo", "PSI con detalle por tramo",
   """import numpy as np
import pandas as pd

def psi(referencia, actual, tramos=10):
    \"\"\"Índice de estabilidad poblacional entre dos períodos.

    Los cortes se fijan con los percentiles del período de referencia:
    es la distribución de construcción la que define la grilla.
    \"\"\"
    cortes = np.percentile(referencia, np.linspace(0, 100, tramos + 1))
    cortes[0], cortes[-1] = -np.inf, np.inf

    r = np.histogram(referencia, cortes)[0] / len(referencia)
    a = np.histogram(actual, cortes)[0] / len(actual)
    r, a = np.clip(r, 1e-6, None), np.clip(a, 1e-6, None)

    detalle = pd.DataFrame({"referencia": r, "actual": a,
                            "aporte": (a - r) * np.log(a / r)})
    return detalle, float(detalle.aporte.sum())


detalle, valor = psi(score_construccion, score_actual)
print(detalle.round(4))
print(f"PSI = {valor:.4f}  ->",
      "estable" if valor < 0.10 else
      "desplazamiento moderado" if valor < 0.25 else
      "REVISAR EL MODELO")"""),
  ("codigo", "Monitoreo por variable y tramos que se compensan",
   """# Tramos que aportan mucho aunque el total sea bajo
relevantes = detalle[detalle.aporte > 0.02]
if len(relevantes) and valor < 0.10:
    print("PSI total bajo pero con movimientos que se compensan:")
    print(relevantes.round(4))

# La cédula F-3 exige PSI también por variable de entrada
for v in variables_modelo:
    _, psi_v = psi(desarrollo[v], actual[v])
    marca = "  <-- REVISAR" if psi_v > 0.25 else ""
    print(f"{v:<24} PSI {psi_v:.4f}{marca}")"""),
  ("nota", "Uso en encargos",
   "Guarda esta función como parte del papel de trabajo. Aplicada sobre la extracción "
   "del cliente, produce en minutos la evidencia que sostiene la observación sobre "
   "monitoreo de modelos."),
 ],
},

# ------------------------------------------------------------------ M07
"M07": {
 "ref": "G-6",
 "titulo": "Laboratorio: recálculo de provisión y conciliación",
 "bloques": [
  ("p", "El recálculo reproduce la provisión desde los parámetros y la concilia contra "
        "el mayor. Es el entregable del módulo y el procedimiento que se ejecuta en un "
        "encargo real."),
  ("codigo", "Etapas, parámetros y pérdida esperada",
   """import pandas as pd

c = pd.read_csv("cartera_cierre.csv")

# Clasificación por etapa según el criterio documentado por la entidad
c["etapa"] = 1
c.loc[c.dias_mora.between(30, 89), "etapa"] = 2
c.loc[c.dias_mora >= 90, "etapa"] = 3

# El horizonte cambia con la etapa: doce meses en la 1, toda la vida en 2 y 3
c["pd_aplicable"] = c.pd_12m.where(c.etapa == 1, c.pd_lifetime)

# EAD incluye el contingente por su factor de conversión
c["ead"] = c.saldo + c.linea_no_usada * c.factor_conversion

c["perdida_esperada"] = c.pd_aplicable * c.lgd * c.ead"""),
  ("codigo", "Conciliación contra el mayor",
   """resumen = c.groupby("etapa").agg(
    operaciones=("ead", "size"),
    exposicion=("ead", "sum"),
    provision=("perdida_esperada", "sum"))
resumen["cobertura"] = resumen.provision / resumen.exposicion
print(resumen.round(2))

SALDO_MAYOR = 4_812_357.90          # cuenta de provisión al cierre
recalculado = c.perdida_esperada.sum()
diferencia = recalculado - SALDO_MAYOR

print(f"\\nRecálculo   {recalculado:>14,.2f}")
print(f"Mayor       {SALDO_MAYOR:>14,.2f}")
print(f"Diferencia  {diferencia:>14,.2f}")

if abs(diferencia) > 0.01:
    print("Requerir la composición del ajuste de la administración")"""),
  ("codigo", "Sensibilidad de la LGD",
   """# La LGD suele no tener modelo detrás: conviene medir cuánto pesa
for factor in (0.9, 1.0, 1.1, 1.2):
    total = (c.pd_aplicable * (c.lgd * factor).clip(upper=1) * c.ead).sum()
    print(f"LGD x{factor:>4}   provisión {total:>14,.0f}   "
          f"variación {total / recalculado - 1:+.1%}")"""),
  ("nota", "Qué documentar",
   "La diferencia contra el mayor, su explicación línea por línea y el efecto de la "
   "sensibilidad de LGD. Ese conjunto es la cédula de provisión del encargo."),
 ],
},

# ------------------------------------------------------------------ M08
"M08": {
 "ref": "H-6",
 "titulo": "Laboratorio: distribución de pérdidas, VaR y tensión",
 "bloques": [
  ("p", "La simulación construye la distribución completa de pérdidas de la cartera. "
        "De ahí salen los dos números del módulo: la media, que se provisiona, y la "
        "cola, que se cubre con capital."),
  ("codigo", "Simulación de la distribución de pérdidas",
   """import numpy as np

rng = np.random.default_rng(20260722)
SIMULACIONES = 50_000

pd_ = c.pd_aplicable.to_numpy()
lgd = c.lgd.to_numpy()
ead = c.ead.to_numpy()

perdidas = np.empty(SIMULACIONES)
for i in range(SIMULACIONES):
    incumple = rng.random(pd_.size) < pd_
    perdidas[i] = (ead[incumple] * lgd[incumple]).sum()

esperada = perdidas.mean()
var99 = np.percentile(perdidas, 99)

print(f"Pérdida esperada    {esperada:>14,.0f}   -> provisión")
print(f"VaR 99 %            {var99:>14,.0f}")
print(f"Pérdida inesperada  {var99 - esperada:>14,.0f}   -> capital")"""),
  ("riesgo", "El supuesto que hay que cuestionar",
   "El bucle anterior sortea cada operación de forma independiente. En una crisis los "
   "incumplimientos ocurren juntos, y esa correlación es precisamente lo que engorda "
   "la cola de la distribución. Un modelo que asume independencia subestima el capital "
   "necesario sin que ningún dato observado lo delate."),
  ("codigo", "Efecto de la correlación y escenario de tensión",
   """# Factor común: un shock sistémico que afecta a toda la cartera a la vez
RHO = 0.15
for rho in (0.0, 0.10, 0.20):
    tot = np.empty(10_000)
    for i in range(10_000):
        shock = rng.standard_normal()
        umbral = (np.sqrt(rho) * shock + np.sqrt(1 - rho) *
                  rng.standard_normal(pd_.size))
        incumple = umbral < np.quantile(umbral, pd_.mean())
        tot[i] = (ead[incumple] * lgd[incumple]).sum()
    print(f"rho={rho:.2f}   VaR 99 % {np.percentile(tot, 99):>14,.0f}")

# Escenario adverso: al menos tan severo como la peor crisis observada
pd_estres = np.clip(pd_ * 2.4, 0, 1)
print(f"\\nPérdida esperada bajo tensión "
      f"{(pd_estres * lgd * ead).sum():,.0f}")"""),
  ("nota", "Cierre del programa",
   "Con este laboratorio quedan cubiertos los ocho entregables. El memorando de "
   "validación independiente consolida los hallazgos de los ocho módulos con su efecto "
   "cuantificado sobre la cifra."),
 ],
},

}
