import streamlit as st
import requests
import pandas as pd

# ==================================================
# CONFIGURACIÓN GENERAL
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
    background: linear-gradient(180deg, #FFFDF5, #FFF7D6);
}

.header-container{
    background: linear-gradient(90deg,#FFE259,#FFA751);
    padding:25px;
    border-radius:20px;
    text-align:center;
}

.titulo{
    font-size:50px;
    font-weight:900;
    color:#1F2937;
}

.subtitulo{
    font-size:18px;
    color:#374151;
}

.footer{
    text-align:center;
    color:gray;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# ENCABEZADO
# ==================================================

st.markdown("""
<div class="header-container">

<div class="titulo">
🍌 BananaVision AI
</div>

<div class="subtitulo">

Sistema Inteligente de Clasificación de Madurez de Bananos

<br>

Proyecto Final de Visión por Computador

<br>

Maestría en Inteligencia Artificial

</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==================================================
# OBJETIVO
# ==================================================

with st.expander("🎯 Objetivo del Proyecto", expanded=True):

    st.markdown("""

### Objetivo General

Desarrollar una aplicación web basada en Inteligencia Artificial capaz de identificar automáticamente el estado de maduración de un banano a partir del análisis de imágenes digitales.

### Objetivos Específicos

✅ Implementar técnicas de visión por computador.

✅ Clasificar imágenes mediante Deep Learning.

✅ Integrar una API REST desplegada en Microsoft Azure.

✅ Permitir predicciones en tiempo real.

✅ Facilitar la toma de decisiones sobre el estado de maduración del fruto.

""")

# ==================================================
# DESCRIPCIÓN
# ==================================================

with st.expander("📖 Descripción de la Aplicación"):

    st.markdown("""

### ¿Qué hace BananaVision AI?

BananaVision AI es una aplicación web desarrollada para analizar imágenes de bananos utilizando técnicas de Inteligencia Artificial y Visión por Computador.

La solución consume una API REST desplegada en Microsoft Azure Container Apps y permite determinar automáticamente el nivel de maduración del fruto.

### Tecnologías Implementadas

- Python
- Streamlit
- FastAPI
- Deep Learning
- Visión por Computador
- Microsoft Azure

### Flujo de Funcionamiento

1. El usuario carga una imagen.
2. La imagen se envía a la API desplegada en Azure.
3. El modelo de IA analiza la imagen.
4. Se calcula la predicción.
5. Se muestran probabilidades y confianza.
6. Se genera una recomendación automática.

""")

# ==================================================
# INTERPRETACIÓN
# ==================================================

with st.expander("🧠 Cómo Interpretar los Resultados"):

    st.markdown("""

### Categorías Utilizadas

🟢 Unripe
- Banano verde.
- No apto para consumo inmediato.

🟡 Half_Ripe
- Banano parcialmente maduro.
- Próximo a alcanzar el estado óptimo.

✅ Ripe
- Banano maduro.
- Condición ideal para consumo.

🟤 Overripe
- Banano sobremaduro.
- Recomendado para postres o consumo rápido.

### Nivel de Confianza

El porcentaje de confianza representa qué tan seguro está el modelo sobre la clasificación obtenida.

- Más de 90% → Muy alta confianza.
- Entre 80% y 90% → Alta confianza.
- Entre 60% y 80% → Confianza moderada.
- Menor de 60% → Revisar calidad de la imagen.

""")

st.divider()

# ==================================================
# INTEGRANTES
# ==================================================

st.subheader("👩‍🎓 Equipo del Proyecto")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    Adriana Milena Huertas Martín
    """)

with col2:
    st.success("""
    Adriana Patricia Fernández Infante
    """)

st.divider()

# ==================================================
# ESTADO DE LA API
# ==================================================

st.subheader("☁️ Estado de la Infraestructura")

try:

    health = requests.get(API_HEALTH, timeout=10)

    if health.status_code == 200:

        st.success("✅ API conectada correctamente en Microsoft Azure")

    else:

        st.warning("⚠️ La API respondió pero presentó una novedad.")

except:

    st.error("❌ No fue posible conectar con Azure.")

st.divider()

# ==================================================
# PREDICCIÓN
# ==================================================

st.subheader("📷 Clasificación de Imagen")

archivo = st.file_uploader(
    "Seleccione una imagen de banano",
    type=["jpg","jpeg","png","webp"]
)

if archivo:

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            archivo,
            caption="Imagen Seleccionada",
            use_container_width=True
        )

    with col2:

        st.info("""
        ### Instrucciones

        1. Cargue una imagen de un banano.
        2. Presione Analizar Imagen.
        3. Espere el resultado.
        4. Revise la interpretación generada.
        """)

    if st.button("🔍 Analizar Imagen", use_container_width=True):

        with st.spinner("Analizando imagen utilizando Inteligencia Artificial..."):

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

                    clase = resultado["clase_predicha"]
                    confianza = resultado["confianza"]
                    probabilidades = resultado["probabilidades"]

                    st.divider()

                    st.subheader("📊 Resultado de la Clasificación")

                    c1, c2 = st.columns(2)

                    with c1:
                        st.metric(
                            "Clase Predicha",
                            clase
                        )

                    with c2:
                        st.metric(
                            "Confianza",
                            f"{confianza*100:.2f}%"
                        )

                    st.progress(float(confianza))

                    st.subheader("📈 Distribución de Probabilidades")

                    df = pd.DataFrame({
                        "Clase": list(probabilidades.keys()),
                        "Probabilidad (%)":
                            [v*100 for v in probabilidades.values()]
                    })

                    st.bar_chart(df.set_index("Clase"))

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    st.subheader("📝 Interpretación Generada")

                    if clase == "Unripe":

                        st.warning("""
                        Resultado: Banano Verde.

                        El fruto se encuentra en una fase temprana de maduración y aún no es recomendable para consumo inmediato.
                        """)

                    elif clase == "Half_Ripe":

                        st.info("""
                        Resultado: Banano Semi Maduro.

                        El fruto continúa su proceso natural de maduración y estará listo para consumo en corto tiempo.
                        """)

                    elif clase == "Ripe":

                        st.success("""
                        Resultado: Banano Maduro.

                        El fruto presenta condiciones óptimas para consumo inmediato.
                        """)

                    elif clase == "Overripe":

                        st.error("""
                        Resultado: Banano Sobremaduro.

                        Se recomienda consumir pronto o utilizar en preparaciones como postres o batidos.
                        """)

                else:

                    st.error(
                        f"Error de API: {response.status_code}"
                    )

            except Exception as e:

                st.error(f"Error: {e}")

st.divider()

st.markdown("""
<div class="footer">

🍌 BananaVision AI

Proyecto Final de Visión por Computador

Maestría en Inteligencia Artificial

Tecnologías:

Python • Streamlit • FastAPI • Microsoft Azure • Deep Learning

Adriana Milena Huertas Martín

Adriana Patricia Fernández Infante

2026

</div>
""", unsafe_allow_html=True)