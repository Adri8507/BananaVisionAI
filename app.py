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
font-size:70px;
font-weight:800;
color:#D97706;
}

.sub-title{
text-align:center;
font-size:24px;
color:#444;
}

.footer{
text-align:center;
color:#444;
padding-top:20px;
}

div[data-testid="stMetric"]{
background:white;
padding:15px;
border-radius:12px;
box-shadow:0px 2px 10px rgba(0,0,0,0.1);
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

<br>

Proyecto Final de Visión por Computador

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

✅ Obtener predicciones en tiempo real.

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
- Nivel de confianza
- Probabilidades por categoría
- Interpretación automática

### Categorías

🟢 Unripe

🟡 Half_Ripe

✅ Ripe

🟤 Overripe

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

    st.info("""
Reemplazar estos valores por las métricas reales obtenidas en el notebook final.
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
