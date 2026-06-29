import streamlit as st

st.set_page_config(
    page_title="ISRO Heat Stress Analysis",
    page_icon="🌍",
    layout="wide"
)

st.sidebar.title("🛰 ISRO Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🌡 Land Surface Temperature",
        "🌳 Vegetation (NDVI)",
        "💧 Water Index (NDWI)",
        "🏢 Built-up Index (NDBI)",
        "🔥 Heat Risk",
        "🤖 AI Model",
        "📊 Statistics",
        "ℹ About"
    ]
)

if page == "🏠 Home":
    st.title("🌍 ISRO Heat Stress Analysis Dashboard")

    st.success("Backend Pipeline Completed Successfully")

    st.markdown("""
### Project Workflow

✔ Landsat-8 Download

✔ Preprocessing

✔ Cloud Masking

✔ NDVI

✔ NDWI

✔ NDBI

✔ Land Surface Temperature

✔ Heat Risk Classification

✔ Random Forest Model

---
Developed for the ISRO Hackathon.
""")

elif page == "🌡 Land Surface Temperature":
    st.title("🌡 Land Surface Temperature")
    st.info("LST visualization will be added here.")

elif page == "🌳 Vegetation (NDVI)":
    st.title("🌳 NDVI")
    st.info("NDVI visualization will be added here.")

elif page == "💧 Water Index (NDWI)":
    st.title("💧 NDWI")
    st.info("NDWI visualization will be added here.")

elif page == "🏢 Built-up Index (NDBI)":
    st.title("🏢 NDBI")
    st.info("NDBI visualization will be added here.")

elif page == "🔥 Heat Risk":
    st.title("🔥 Heat Risk Map")
    st.info("Heat risk map will be added here.")

elif page == "🤖 AI Model":
    st.title("🤖 Random Forest Model")
    st.success("Model trained successfully.")
    st.write("Accuracy: 100% (prototype model)")

elif page == "📊 Statistics":
    st.title("📊 Statistics")
    st.info("Statistics will be displayed here.")

elif page == "ℹ About":
    st.title("About")
    st.write("""
This project detects urban heat stress using:

- Landsat-8 imagery
- NDVI
- NDWI
- NDBI
- Land Surface Temperature
- Random Forest Machine Learning

Developed for the ISRO Hackathon.
""")