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
    background: linear-gradient(180deg,#FFFDF5,#FFF7D6);
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

<br><br>

Proyecto Final de Visión por Computador

<br><br>

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

✅ Facilitar procesos de control de calidad y clasificación de fruta.

""")

# ==================================================
# DESCRIPCIÓN
# ==================================================

with st.expander("📖 Descripción de la Aplicación"):

    st.markdown("""

### ¿Qué es BananaVision AI?

BananaVision AI es una aplicación desarrollada para clasificar automáticamente el estado de maduración de bananos utilizando técnicas de Inteligencia Artificial y Visión por Computador.

La aplicación permite cargar imágenes del fruto y obtener una predicción automática mediante un modelo de Deep Learning desplegado en Microsoft Azure.

### Tecnologías Utilizadas

✅ Python

✅ Streamlit

✅ FastAPI

✅ Microsoft Azure

✅ Deep Learning

✅ Computer Vision

### Flujo de Funcionamiento

1. El usuario selecciona una imagen.
2. La imagen se envía a la API alojada en Azure.
3. El modelo procesa la imagen.
4. Se genera una predicción.
5. Se muestran probabilidades y nivel de confianza.
6. Se interpreta el resultado para el usuario.

""")

# ==================================================
# INTERPRETACIÓN
# ==================================================

with st.expander("🧠 Cómo Interpretar los Resultados"):

    st.markdown("""

### Categorías del Modelo

🟢 Unripe
- Banano verde.
- No recomendado para consumo inmediato.

🟡 Half_Ripe
- Banano parcialmente maduro.
- Próximo a alcanzar la maduración óptima.

✅ Ripe
- Banano maduro.
- Estado ideal para consumo.

🟤 Overripe
- Banano sobremaduro.
- Recomendado para consumo inmediato o elaboración de postres.

### Nivel de Confianza

El porcentaje de confianza representa qué tan seguro está el modelo respecto a la clasificación obtenida.

- Mayor a 90% → Muy alta confianza.
- Entre 80% y 90% → Alta confianza.
- Entre 60% y 80% → Confianza aceptable.
- Menor a 60% → Se recomienda verificar la calidad de la imagen.

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
| F1-Score | 94% |
| AUC | 97% |

**Nota:** Reemplacen estos valores por las métricas reales obtenidas en el notebook.

""")

# ==================================================
# ARQUITECTURA
# ==================================================

with st.expander("🏗️ Arquitectura de la Solución"):

    st.markdown("""

```text
Usuario
   ↓
Aplicación Web Streamlit
   ↓
API REST FastAPI
   ↓
Microsoft Azure Container Apps
   ↓
Modelo Deep Learning
   ↓
Clasificación de Madurez
