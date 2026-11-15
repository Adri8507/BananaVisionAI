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
    background-color: #FFFDF5;
}

.titulo {
    text-align: center;
    color: #D97706;
    font-size: 50px;
    font-weight: bold;
}

.subtitulo {
    text-align: center;
    font-size: 20px;
}

.footer {
    text-align:center;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# ENCABEZADO
# ==================================================

st.markdown(
    '<p class="titulo">🍌 BananaVision AI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitulo">Sistema Inteligente para Clasificación de Madurez de Bananos</p>',
    unsafe_allow_html=True
)

st.write("### Proyecto Final - Visión por Computador")
st.write("### Maestría en Inteligencia Artificial")

st.divider()

# ==================================================
# OBJETIVO
# ==================================================

with st.expander("🎯 Objetivo del Proyecto", expanded=True):

    st.write("""
Desarrollar una aplicación web basada en Inteligencia Artificial capaz de identificar
automáticamente el estado de maduración de un banano a partir de imágenes digitales,
integrando Visión por Computador, Deep Learning y servicios en la nube.
""")

# ==================================================
# DESCRIPCIÓN
# ==================================================

with st.expander("📖 Descripción de la Aplicación"):

    st.write("""
BananaVision AI permite analizar imágenes de bananos utilizando un modelo de
Deep Learning desplegado en Microsoft Azure.

El usuario carga una imagen y la aplicación envía la fotografía a una API REST,
la cual devuelve la categoría detectada, la confianza y las probabilidades
de clasificación.
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

La confianza indica el porcentaje de seguridad del modelo respecto a la predicción realizada.
""")

# ==================================================
# MÉTRICAS
# ==================================================

with st.expander("📊 Métricas del Modelo"):

    st.markdown("""
| Métrica | Valor |
|----------|----------|
| Accuracy | 95% |
| Precision | 94% |
| Recall | 95% |
| F1 Score | 94% |
| AUC | 97% |

*Reemplacen estos valores por los reales obtenidos en el notebook.*
""")

# ==================================================
# ARQUITECTURA
# ==================================================

with st.expander("🏗️ Arquitectura de la Solución"):

    st.code("""
Usuario
   ↓
Aplicación Streamlit
   ↓
API REST (Azure)
   ↓
Modelo Deep Learning
   ↓
Predicción
""")

# ==================================================
# INTEGRANTES
# ==================================================

st.subheader("👩‍🎓 Equipo del Proyecto")

col1, col2 = st.columns(2)

with col1:
    st.success("Adriana Milena Huertas Martín")

with col2:
    st.success("Adriana Patricia Fernández Infante")

st.divider()

# ==================================================
# ESTADO API
# ==================================================

st.subheader("☁️ Estado del Servicio")

try:

    response = requests.get(API_HEALTH, timeout=10)

    if response.status_code == 200:
        st.success("✅ API conectada correctamente en Microsoft Azure")
    else:
        st.warning("⚠️ La API respondió pero presentó una novedad.")

except Exception as e:

    st.error(f"❌ Error de conexión: {e}")

st.divider()

# ==================================================
# CLASIFICACIÓN
# ==================================================

st.subheader("📷 Clasificación de Imagen")

archivo = st.file_uploader(
    "Seleccione una imagen",
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
                        "Sin dato"
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
                        f"Clase Predicha: {clase}"
                    )

                    st.metric(
                        "Confianza",
                        f"{confianza*100:.2f}%"
                    )

                    st.progress(float(confianza))

                    if probabilidades:

                        st.subheader("📈 Probabilidades")

                        df = pd.DataFrame({
                            "Clase": list(probabilidades.keys()),
                            "Probabilidad (%)": [
                                v * 100
                                for v in probabilidades.values()
                            ]
                        })

                        st.bar_chart(
                            df.set_index("Clase")
                        )

                    st.subheader("📝 Interpretación")

                    if clase == "Unripe":
                        st.warning("Banano verde.")

                    elif clase == "Half_Ripe":
                        st.info("Banano semimaduro.")

                    elif clase == "Ripe":
                        st.success("Banano maduro.")

                    elif clase == "Overripe":
                        st.error("Banano sobremaduro.")

                else:

                    st.error(
                        f"Error de API: {respuesta.status_code}"
                    )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

st.divider()

st.markdown("""
<div class="footer">

🍌 BananaVision AI

Proyecto Final de Visión por Computador

Maestría en Inteligencia Artificial

Adriana Milena Huertas Martín

Adriana Patricia Fernández Infante

2026

</div>
""", unsafe_allow_html=True)
