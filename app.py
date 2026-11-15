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

✅ Despliegue en Azure

✅ API REST

✅ Integración de la Aplicación
""")

st.divider()

# ==================================================
# ESTADO DEL SERVICIO
# ==================================================

st.subheader("☁️ Estado del Servicio")

try:

    health = requests.get(
        API_HEALTH,
        timeout=10
    )

    if health.status_code == 200:

        st.success(
            "✅ API BananaVision AI conectada correctamente en Microsoft Azure."
        )

    else:

        st.warning(
            f"⚠️ La API respondió con código {health.status_code}"
        )

except Exception as e:

    st.error(
        f"❌ Error de conexión: {e}"
    )

st.divider()

# ==================================================
# CLASIFICACIÓN DE IMÁGENES
# ==================================================

st.subheader("📷 Clasificación de Estado de Maduración")

archivo = st.file_uploader(
    "Seleccione una imagen de banano",
    type=["jpg", "jpeg", "png", "webp"]
)

if archivo is not None:

    st.image(
        archivo,
        caption="Imagen seleccionada",
        use_container_width=True
    )

    st.info("""
### ¿Qué hará el sistema?

1. La imagen se enviará a la API desplegada en Microsoft Azure.
2. El modelo MobileNetV2 analizará la fotografía.
3. Se identificará el estado de maduración.
4. Se mostrarán probabilidades y recomendaciones.
""")

    if st.button("🔍 Analizar Imagen", use_container_width=True):

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

                    c1, c2 = st.columns(2)

                    with c1:
                        st.metric(
                            "Clase Detectada",
                            clase
                        )

                    with c2:
                        st.metric(
                            "Confianza",
                            f"{confianza*100:.2f}%"
                        )

                    st.progress(float(confianza))

                    if probabilidades:

                        st.subheader(
                            "📊 Probabilidades por Categoría"
                        )

                        df = pd.DataFrame({
                            "Clase":
                                list(probabilidades.keys()),
                            "Probabilidad (%)":
                                [
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

                    st.subheader(
                        "📝 Interpretación del Resultado"
                    )

                    if clase == "Unripe":

                        st.warning("""
### 🟢 Banano Verde

El fruto aún no ha alcanzado la madurez adecuada.

**Recomendación:**
Conservar algunos días antes de su consumo.
""")

                    elif clase == "Half_Ripe":

                        st.info("""
### 🟡 Banano Semi Maduro

El proceso de maduración continúa.

**Recomendación:**
Consumir en los próximos días.
""")

                    elif clase == "Ripe":

                        st.success("""
### ✅ Banano Maduro

Estado óptimo para consumo.

**Recomendación:**
Consumir inmediatamente.
""")

                    elif clase == "Overripe":

                        st.error("""
### 🟤 Banano Sobremaduro

Maduración avanzada detectada.

**Recomendación:**
Utilizar en batidos, repostería o consumir pronto.
""")

                else:

                    st.error(
                        f"Error de la API: {response.status_code}"
                    )

            except Exception as e:

                st.error(
                    f"Error de conexión: {e}"
                )
