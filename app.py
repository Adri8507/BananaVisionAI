import streamlit as st
import requests
import pandas as pd

# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="BananaVision AI",
    page_icon="🍌",
    layout="wide"
)

API_HEALTH = "https://ca-bananavision-api.politestone-cecff6e5.westus2.azurecontainerapps.io/health"
API_PREDICT = "https://ca-bananavision-api.politestone-cecff6e5.westus2.azurecontainerapps.io/predict"

# ==================================================
# ESTILOS
# ==================================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(180deg,#FFFBE6,#FFE082);
}

.big-title{
    text-align:center;
    font-size:60px;
    font-weight:800;
    color:#D97706;
}

.sub-title{
    text-align:center;
    font-size:22px;
    color:#444444;
}

.footer{
    text-align:center;
    color:#444444;
    padding:20px;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    padding:15px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# ENCABEZADO
# ==================================================

st.markdown("""
<div class="big-title">
🍌 BananaVision AI
</div>

<div class="sub-title">
Sistema Inteligente de Clasificación de Madurez de Bananos
<br><br>
Proyecto Final - Visión por Computador
<br>
Maestría en Inteligencia Artificial
</div>
""", unsafe_allow_html=True)

st.divider()

# ==================================================
# OBJETIVO
# ==================================================

with st.expander("🎯 Objetivo del Proyecto", expanded=True):

    st.markdown("""
### Objetivo General

Desarrollar una aplicación web capaz de clasificar automáticamente el estado de maduración de bananos mediante técnicas de Inteligencia Artificial, Deep Learning y Visión por Computador.

### Objetivos Específicos

✅ Clasificar imágenes de bananos.

✅ Integrar una API REST desplegada en Microsoft Azure.

✅ Obtener resultados en tiempo real.

✅ Apoyar procesos de control de calidad agrícola.
""")

# ==================================================
# DESCRIPCIÓN
# ==================================================

with st.expander("📖 Descripción de la Aplicación"):

    st.markdown("""
### ¿Qué hace BananaVision AI?

La aplicación recibe una fotografía de un banano y la envía a un modelo de Inteligencia Artificial desplegado en Microsoft Azure.

El sistema devuelve:

- Clase predicha
- Confianza
- Probabilidades por categoría
- Interpretación automática

### Categorías

🟢 Unripe

🟡 Half_Ripe

✅ Ripe

🟤 Overripe
""")

# ==================================================
# INTERPRETACIÓN
# ==================================================

with st.expander("🧠 Cómo Interpretar los Resultados"):

    st.markdown("""
- 🟢 **Unripe**: Banano verde.
- 🟡 **Half_Ripe**: Banano semimaduro.
- ✅ **Ripe**: Banano maduro.
- 🟤 **Overripe**: Banano sobremaduro.

La confianza indica qué tan seguro está el modelo respecto a la clasificación realizada.
""")

# ==================================================
# MÉTRICAS
# ==================================================

with st.expander("📊 Métricas del Modelo", expanded=True):

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Accuracy", "95%")
    c2.metric("Precision", "94%")
    c3.metric("Recall", "95%")
    c4.metric("F1 Score", "94%")
    c5.metric("AUC", "97%")

    st.info(
        "Reemplacen estos valores por las métricas reales del notebook."
    )

# ==================================================
# ARQUITECTURA
# ==================================================

with st.expander("🏗️ Arquitectura de la Solución"):

    st.code("""
Usuario
    ↓
Aplicación Streamlit
    ↓
API REST Azure
    ↓
Modelo Deep Learning
    ↓
Predicción
""")

# ==================================================
# EQUIPO
# ==================================================

st.subheader("👩‍🎓 Equipo del Proyecto")

col1, col2 = st.columns(2)

with col1:

    st.success("""
### Adriana Milena Huertas Martín

✅ Dataset

✅ Entrenamiento

✅ Evaluación
""")

with col2:

    st.success("""
### Adriana Patricia Fernández Infante

✅ Azure

✅ API REST

✅ Despliegue
""")

st.divider()

# ==================================================
# ESTADO DEL SERVICIO
# ==================================================

st.subheader("☁️ Estado del Servicio")

try:

    health = requests.get(API_HEALTH, timeout=10)

    if health.status_code == 200:

        st.success(
            "✅ API BananaVision AI conectada correctamente."
        )

    else:

        st.warning(
            f"⚠️ Respuesta recibida: {health.status_code}"
        )

except Exception as e:

    st.error(
        f"❌ Error de conexión: {e}"
    )

st.divider()

# ==================================================
# CLASIFICACIÓN
# ==================================================

st.subheader("📷 Clasificación de Imagen")

archivo = st.file_uploader(
    "Seleccione una imagen de banano",
    type=["jpg", "jpeg", "png", "webp"]
)

if archivo is not None:

    st.image(
        archivo,
        caption="Imagen cargada",
        use_container_width=True
    )

    if st.button("🔍 Analizar Imagen"):

        with st.spinner("Analizando imagen..."):

            try:

                files = {
                    "file": (
                        archivo.name,
                        archivo.getvalue(),
                        archivo.type
                    )
                }

                respuesta = requests.post(
                    API_PREDICT,
                    files=files,
                    timeout=30
                )

                if respuesta.status_code == 200:

                    resultado = respuesta.json()

                    clase = resultado.get(
                        "clase_predicha",
                        "Sin resultado"
                    )

                    confianza = resultado.get(
                        "confianza",
                        0
                    )

                    probabilidades = resultado.get(
                        "probabilidades",
                        {}
                    )

                    st.divider()

                    c1, c2 = st.columns(2)

                    with c1:
                        st.metric(
                            "Clase Predicha",
                            clase
                        )

                    with c2:
                        st.metric(
                            "Confianza",
                            f"{confianza * 100:.2f}%"
                        )

                    st.progress(float(confianza))

                    if probabilidades:

                        st.subheader("📈 Probabilidades")

                        df = pd.DataFrame({
                            "Clase": list(probabilidades.keys()),
                            "Probabilidad (%)": [
                                round(v * 100, 2)
                                for v in probabilidades.values()
                            ]
                        })

                        st.bar_chart(
                            df.set_index("Clase")
                        )

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                    st.subheader("📝 Interpretación")

                    if clase == "Unripe":

                        st.warning("""
### 🟢 Banano Verde

Aún no ha alcanzado su estado óptimo de maduración.

**Recomendación:** esperar algunos días antes de consumir.
""")

                    elif clase == "Half_Ripe":

                        st.info("""
### 🟡 Banano Semi Maduro

Se encuentra en transición hacia la madurez.

**Recomendación:** consumir próximamente.
""")

                    elif clase == "Ripe":

                        st.success("""
### ✅ Banano Maduro

Estado ideal para consumo.

**Recomendación:** consumo inmediato.
""")

                    elif clase == "Overripe":

                        st.error("""
### 🟤 Banano Sobremaduro

Maduración avanzada.

**Recomendación:** utilizar en postres o batidos.
""")

                else:

                    st.error(
                        f"Error API: {respuesta.status_code}"
                    )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

st.divider()

st.markdown("""
<div class="footer">

🍌 BananaVision AI

<br>

Proyecto Final de Visión por Computador

<br>

Maestría en Inteligencia Artificial

<br><br>

Adriana Milena Huertas Martín

<br>

Adriana Patricia Fernández Infante

<br><br>

Python • Streamlit • FastAPI • Azure • Deep Learning

<br><br>

2026

</div>
""", unsafe_allow_html=True)
