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

### Funcionalidades

✅ Carga una imagen de banano

✅ Envía la imagen a una API REST

✅ Clasifica automáticamente el estado de maduración

✅ Presenta porcentajes de probabilidad

✅ Genera una interpretación automática del resultado
""")

# ==================================================
# EQUIPO
# ==================================================

st.subheader("👩‍🎓 Equipo del Proyecto")

col1, col2 = st.columns(2)

with col1:
    st.success("""
### Adriana Milena Huertas Martín
""")

with col2:
    st.success("""
### Adriana Patricia Fernández Infante
""")

st.divider()

# ==================================================
# ESTADO API
# ==================================================

st.subheader("☁️ Estado del Servicio")

try:

    health = requests.get(API_HEALTH, timeout=10)

    if health.status_code == 200:
        st.success("✅ API BananaVision AI conectada correctamente")
    else:
        st.warning(f"⚠️ Estado recibido: {health.status_code}")

except Exception as e:
    st.error(f"❌ Error de conexión: {e}")

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

                    traduccion = {
                        "Unripe": "Verde",
                        "Half_Ripe": "En Maduración",
                        "Ripe": "Maduro",
                        "Overripe": "Sobremaduro"
                    }

                    clase_original = resultado.get(
                        "clase_predicha",
                        "Sin resultado"
                    )

                    clase = traduccion.get(
                        clase_original,
                        clase_original
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
                            f"{confianza*100:.2f}%"
                        )

                    st.progress(float(confianza))

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
                                "🟢 Verde",
                                f"{unripe:.2f}%"
                            )

                            st.metric(
                                "🟡 En Maduración",
                                f"{half:.2f}%"
                            )

                        with p2:

                            st.metric(
                                "✅ Maduro",
                                f"{ripe:.2f}%"
                            )

                            st.metric(
                                "🟤 Sobremaduro",
                                f"{overripe:.2f}%"
                            )

                        df = pd.DataFrame({
                            "Clase": [
                                "Verde",
                                "En Maduración",
                                "Maduro",
                                "Sobremaduro"
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

Probabilidad Verde: {unripe:.2f} %

Probabilidad En Maduración: {half:.2f} %

Probabilidad Maduro: {ripe:.2f} %

Probabilidad Sobremaduro: {overripe:.2f} %
"""
                        )

                    st.subheader("📝 Interpretación")

                    if clase == "Verde":

                        st.warning("""
### 🟢 Banano Verde

El fruto aún no ha alcanzado el estado adecuado de maduración.

✅ Recomendación:
Esperar algunos días antes del consumo.
""")

                    elif clase == "En Maduración":

                        st.info("""
### 🟡 Banano en Maduración

El fruto se encuentra en una etapa intermedia de maduración.

✅ Recomendación:
Consumir en los próximos días.
""")

                    elif clase == "Maduro":

                        st.success("""
### ✅ Banano Maduro

El fruto se encuentra en condiciones óptimas para el consumo.

✅ Recomendación:
Consumir inmediatamente.
""")

                    elif clase == "Sobremaduro":

                        st.error("""
### 🟤 Banano Sobremaduro

El fruto presenta una maduración avanzada.

✅ Recomendación:
Ideal para preparación de postres, tortas o batidos.
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
# PIE DE PÁGINA
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
