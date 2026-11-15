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

.stApp {
    background: linear-gradient(180deg,#FFFBE6,#FFE082);
}

.titulo {
    text-align:center;
    font-size:65px;
    font-weight:bold;
    color:#D97706;
}

.subtitulo {
    text-align:center;
    font-size:22px;
    color:#444;
}

.footer {
    text-align:center;
    color:#444;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    padding:10px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# ENCABEZADO
# ==================================================

st.markdown("""
<div class="titulo">
🍌 BananaVision AI
</div>

<div class="subtitulo">
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
Desarrollar una aplicación web basada en Inteligencia Artificial capaz de identificar automáticamente el estado de maduración de un banano mediante técnicas de Visión por Computador y Deep Learning.
""")

# ==================================================
# DESCRIPCIÓN
# ==================================================

with st.expander("📖 Descripción de la Aplicación"):

    st.markdown("""
BananaVision AI permite analizar imágenes de bananos utilizando un modelo de Inteligencia Artificial desplegado en Microsoft Azure.

La aplicación:

✅ Recibe una imagen

✅ La envía a una API REST

✅ Obtiene una clasificación automática

✅ Muestra probabilidades

✅ Genera una interpretación del resultado
""")

# ==================================================
# EQUIPO
# ==================================================

st.subheader("👩‍🎓 Equipo del Proyecto")

col1, col2 = st.columns(2)

with col1:

    st.success("""
### Adriana Milena Huertas Martín

✅ Preparación del Dataset

✅ Entrenamiento del Modelo

✅ Evaluación de Resultados
""")

with col2:

    st.success("""
### Adriana Patricia Fernández Infante

✅ Azure Container Apps

✅ API REST

✅ Despliegue de la Solución
""")

st.divider()

# ==================================================
# ESTADO API
# ==================================================

st.subheader("☁️ Estado del Servicio")

try:

    health = requests.get(API_HEALTH, timeout=10)

    if health.status_code == 200:

        st.success(
            "✅ API BananaVision AI conectada correctamente"
        )

    else:

        st.warning(
            f"⚠️ Estado recibido: {health.status_code}"
        )

except Exception as e:

    st.error(
        f"❌ Error de conexión: {e}"
    )

st.divider()

# ==================================================
# CARGA DE IMAGEN
# ==================================================

st.subheader("📷 Clasificación de Imagen")

archivo = st.file_uploader(
    "Seleccione una imagen de banano",
    type=["jpg", "jpeg", "png", "webp"]
)

if archivo is not None:

    st.image(
        archivo,
        caption="Imagen Seleccionada",
        use_container_width=True
    )

    if st.button("🔍 Analizar Imagen"):

        with st.spinner(
            "Analizando imagen con Inteligencia Artificial..."
        ):

            try:

                files = {
                    "file": (
                        archivo.name,
                        archivo.getvalue(),
                        archivo.type
                    )
                }

                response = requests.post(
                    API_PREDICT,
                    files=files,
                    timeout=30
                )

                if response.status_code == 200:

                    resultado = response.json()

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

                    st.subheader("📊 Resultado del Análisis")

                    c1, c2 = st.columns(2)

                    with c1:

                        st.metric(
                            "🍌 Clase Detectada",
                            clase
                        )

                    with c2:

                        st.metric(
                            "🎯 Confianza",
                            f"{confianza * 100:.2f}%"
                        )

                    st.progress(float(confianza))

                    # ==============================
                    # PROBABILIDADES
                    # ==============================

                    if probabilidades:

                        unripe = probabilidades.get(
                            "Unripe",
                            0
                        ) * 100

                        half = probabilidades.get(
                            "Half_Ripe",
                            0
                        ) * 100

                        ripe = probabilidades.get(
                            "Ripe",
                            0
                        ) * 100

                        overripe = probabilidades.get(
                            "Overripe",
                            0
                        ) * 100

                        st.subheader(
                            "📈 Probabilidades por Categoría"
                        )

                        p1, p2 = st.columns(2)

                        with p1:

                            st.metric(
                                "🟢 Unripe",
                                f"{unripe:.2f}%"
                            )

                            st.metric(
                                "🟡 Half_Ripe",
                                f"{half:.2f}%"
                            )

                        with p2:

                            st.metric(
                                "✅ Ripe",
                                f"{ripe:.2f}%"
                            )

                            st.metric(
                                "🟤 Overripe",
                                f"{overripe:.2f}%"
                            )

                        df = pd.DataFrame({
                            "Clase": [
                                "Unripe",
                                "Half_Ripe",
                                "Ripe",
                                "Overripe"
                            ],
                            "Probabilidad (%)": [
                                unripe,
                                half,
                                ripe,
                                overripe
                            ]
                        })

                        st.bar_chart(
                            df.set_index("Clase")
                        )

                        st.subheader(
                            "📋 Resumen Automático"
                        )

                        st.info(
                            f"""
Clase detectada: {clase}

Confianza del modelo: {confianza * 100:.2f} %

Probabilidad Unripe: {unripe:.2f} %

Probabilidad Half_Ripe: {half:.2f} %

Probabilidad Ripe: {ripe:.2f} %

Probabilidad Overripe: {overripe:.2f} %
"""
                        )

                    # ==============================
                    # INTERPRETACIÓN
                    # ==============================

                    st.subheader(
                        "📝 Interpretación"
                    )

                    if clase == "Unripe":

                        st.warning("""
### 🟢 Banano Verde

El fruto aún no ha alcanzado la madurez adecuada.

✅ Recomendación:
Esperar algunos días antes del consumo.
""")

                    elif clase == "Half_Ripe":

                        st.info("""
### 🟡 Banano Semi Maduro

El proceso de maduración continúa.

✅ Recomendación:
Consumir próximamente.
""")

                    elif clase == "Ripe":

                        st.success("""
### ✅ Banano Maduro

Estado óptimo para consumo.

✅ Recomendación:
Consumir inmediatamente.
""")

                    elif clase == "Overripe":

                        st.error("""
### 🟤 Banano Sobremaduro

Maduración avanzada.

✅ Recomendación:
Ideal para postres, repostería o batidos.
""")

                else:

                    st.error(
                        f"Error API: {response.status_code}"
                    )

            except Exception as e:

                st.error(
                    f"Error de conexión: {e}"
                )

# ==================================================
# PIE
# ==================================================

st.divider()

st.markdown("""
<div class="footer">

🍌 BananaVision AI

<br><br>

Proyecto Final de Visión por Computador

<br>

Maestría en Inteligencia Artificial

<br><br>

Adriana Milena Huertas Martín

<br>

Adriana Patricia Fernández Infante

<br><br>

Microsoft Azure • FastAPI • Streamlit • MobileNetV2

</div>
""", unsafe_allow_html=True)
