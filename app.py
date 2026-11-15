import streamlit as st
import requests
import pandas as pd

# ==========================
# CONFIGURACIÓN
# ==========================

st.set_page_config(
    page_title="BananaVision AI",
    page_icon="🍌",
    layout="wide"
)

API_HEALTH = "https://ca-bananavision-api.politestone-cecff6e5.westus2.azurecontainerapps.io/health"
API_PREDICT = "https://ca-bananavision-api.politestone-cecff6e5.westus2.azurecontainerapps.io/predict"

# ==========================
# ESTILO
# ==========================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg,#FFFBEA,#FFE082);
}

h1 {
    color: #D97706;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# TÍTULO
# ==========================

st.markdown("""
<h1>🍌 BananaVision AI</h1>
<h3 style='text-align:center'>
Clasificación Inteligente de Madurez de Bananos
</h3>
""", unsafe_allow_html=True)

st.write("### Proyecto Final - Visión por Computador")
st.write("### Maestría en Inteligencia Artificial")

# ==========================
# OBJETIVO
# ==========================

with st.expander("🎯 Objetivo"):

    st.write("""
Clasificar automáticamente el estado de maduración de un banano
mediante Inteligencia Artificial y Visión por Computador.
""")

# ==========================
# DESCRIPCIÓN
# ==========================

with st.expander("📖 Descripción"):

    st.write("""
La aplicación envía una imagen a una API desplegada en Azure y devuelve:

- Clase predicha
- Confianza
- Probabilidades
- Interpretación
""")

# ==========================
# EQUIPO
# ==========================

st.subheader("👩‍🎓 Equipo del Proyecto")

col1, col2 = st.columns(2)

with col1:
    st.success("Adriana Milena Huertas Martín")

with col2:
    st.success("Adriana Patricia Fernández Infante")

# ==========================
# ESTADO API
# ==========================

st.subheader("☁️ Estado del Servicio")

try:

    health = requests.get(API_HEALTH, timeout=10)

    if health.status_code == 200:
        st.success("✅ API conectada correctamente")

    else:
        st.warning(f"Estado recibido: {health.status_code}")

except Exception as e:

    st.error(f"Error de conexión: {e}")

st.divider()

# ==========================
# SUBIR IMAGEN
# ==========================

st.subheader("📷 Subir Imagen")

archivo = st.file_uploader(
    "Seleccione una imagen",
    type=["jpg", "jpeg", "png", "webp"]
)

if archivo is not None:

    st.image(
        archivo,
        caption="Imagen seleccionada",
        use_container_width=True
    )

    if st.button("🔍 Analizar Imagen"):

        with st.spinner("Analizando..."):

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

                    st.success(
                        f"Clase detectada: {clase}"
                    )

                    st.metric(
                        "Confianza",
                        f"{confianza*100:.2f}%"
                    )

                    st.progress(
                        float(confianza)
                    )

                    if probabilidades:

                        st.subheader(
                            "📊 Probabilidades"
                        )

                        df = pd.DataFrame({
                            "Clase": list(probabilidades.keys()),
                            "Probabilidad (%)":
                            [
                                round(v * 100, 2)
                                for v in probabilidades.values()
                            ]
                        })

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                    st.subheader(
                        "📝 Interpretación"
                    )

                    if clase == "Unripe":

                        st.warning(
                            "🟢 Banano Verde"
                        )

                    elif clase == "Half_Ripe":

                        st.info(
                            "🟡 Banano Semi Maduro"
                        )

                    elif clase == "Ripe":

                        st.success(
                            "✅ Banano Maduro"
                        )

                    elif clase == "Overripe":

                        st.error(
                            "🟤 Banano Sobremaduro"
                        )

                else:

                    st.error(
                        f"Error API: {respuesta.status_code}"
                    )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

# ==========================
# PIE
# ==========================

st.divider()

st.markdown("""
### 🍌 BananaVision AI

Adriana Milena Huertas Martín

Adriana Patricia Fernández Infante

Microsoft Azure • FastAPI • Streamlit • MobileNetV2
""")
