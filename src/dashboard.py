import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import rasterio
import matplotlib.pyplot as plt
from pathlib import Path
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ISRO Urban Heat Stress",
    page_icon="🛰",
    layout="wide"
)

# --------------------------------------------------
# PATHS
# --------------------------------------------------

DATA = Path("data/processed")

# --------------------------------------------------
# LOADERS
# --------------------------------------------------

@st.cache_data
def load_csv(name):

    file = DATA / name

    if file.exists():

        return pd.read_csv(file)

    return pd.DataFrame()


@st.cache_data
def raster(path):

    with rasterio.open(path) as src:

        img = src.read(1)

    return img


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

feature = load_csv("feature_stack_ai.csv")

metrics = load_csv("model_metrics.csv")

importance = load_csv("feature_importance.csv")

confidence = load_csv("prediction_confidence.csv")

recommend = load_csv("optimized_scenarios.csv")

budget = load_csv("budget_plans.csv")

implementation = load_csv("implementation_plan.csv")

cooling = load_csv("cooling_scenarios.csv")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title(" ISRO Decision Support System")

page = st.sidebar.radio(

    "Navigation",

    [

        "Home",

        "Satellite",

        "AI Analytics",

        "Recommendations",

        "Scenario",

        "Budget",

        "Novelty",

        "Reports"

    ]

)

st.sidebar.markdown("---")

st.sidebar.info(

    """
Physics Informed AI

Urban Heat Island

Decision Support System

ISRO Hackathon 2026
"""

)

# --------------------------------------------------
# HOME
# --------------------------------------------------

if page == "Home":

    st.title("AI Urban Heat Island Decision Support System")

    st.caption("ISRO Bharatiya Antariksh Hackathon 2026")

    st.markdown("""
### Study Area
**Hyderabad, Telangana, India**

Physics-Informed AI Decision Support Platform
""")

    st.divider()

    st.subheader("Mission Summary")

    c1, c2, c3, c4 = st.columns(4)

    if len(feature) > 0:

        c1.metric(
            "Average LST",
            f"{feature['lst'].mean():.2f} °C"
        )

        c2.metric(
            "Maximum LST",
            f"{feature['lst'].max():.2f} °C"
        )

        c3.metric(
            "Average NDVI",
            f"{feature['ndvi'].mean():.2f}"
        )

        c4.metric(
            "Study Pixels",
            f"{len(feature):,}"
        )

    st.divider()

    left, right = st.columns([2,1])

    with left:

        st.subheader("Land Surface Temperature Distribution")

        if len(feature) > 0:

            fig = px.histogram(
                feature,
                x="lst",
                nbins=40,
                title=""
            )

            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                height=420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with right:

        st.subheader("Mission Information")

        st.info("""
**Satellite**

Sentinel-2 MSI

**Climate Data**

ERA5

**Elevation**

SRTM DEM

**AI Model**

Random Forest Regressor

**Study Area**

Hyderabad

**System Status**

Operational
""")

    st.divider()

    st.subheader("Vegetation vs Temperature")

    if len(feature) > 0:

        fig = px.scatter(

            feature.sample(
                min(5000, len(feature))
            ),

            x="ndvi",

            y="lst",

            color="ndbi",

            title=""

        )

        fig.update_layout(

            plot_bgcolor="white",

            paper_bgcolor="white",

            height=500

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        ),

# --------------------------------------------------
# SATELLITE
# --------------------------------------------------

elif page == "Satellite":

    st.title("Satellite Analysis")
    st.caption("Study Area: Hyderabad, Telangana, India")
    st.divider()
    st.info("""
    📍 Study Area: Hyderabad, Telangana, India

     Satellite Data:
    • Sentinel-2 MSI
    • ERA5 Climate Data
    • SRTM DEM
     """)

    layer = st.selectbox(
        "Select Layer",
        ["NDVI", "NDWI", "NDBI", "LST", "Heat Risk" , "Elevation"]
    )

    image_paths = {
        "NDVI": "outputs/maps/ndvi_Final.png",
        "NDWI": "outputs/maps/ndwi_Final.png",
        "NDBI": "outputs/maps/ndbi_Final.png",
        "LST": "outputs/maps/lst_Final.png",
        "Heat Risk": "outputs/maps/heat_risk_Final.png",
        "Elevation":"outputs/maps/hyderabad_dem_Final.png"
   }

    img = image_paths[layer]

    st.write("Current directory:", os.getcwd())
    st.write("Image path:", img)
    st.write("Exists:", os.path.exists(img))

    if os.path.exists(img):
        st.image(img, use_container_width=True)
        st.markdown("---")

        layer_info = {
           "NDVI": "Normalized Difference Vegetation Index used to assess vegetation density and health.",
           "NDWI": "Normalized Difference Water Index used to identify water bodies and surface moisture.",
           "NDBI": "Normalized Difference Built-up Index used to identify urban and built-up areas.",
           "LST": "Land Surface Temperature derived from satellite observations for thermal analysis.",
           "Heat Risk": "AI-generated heat risk map combining satellite indices and climate variables.",
           "Elevation": "Digital Elevation Model (SRTM) representing terrain elevation."
         }

        st.subheader("Layer Description")
        st.write(layer_info[layer])
    else:
        st.error(f"Image not found: {img}")
# --------------------------------------------------
# AI ANALYTICS
# --------------------------------------------------

elif page=="AI Analytics":

    st.title("AI Decision Engine")
    st.caption("Physics-Informed AI for Urban Heat Assessment")
    st.divider()
    st.caption("Study Area: Hyderabad, Telangana, India")
    if len(metrics)>0:

        st.subheader("Model Evaluation Metrics")

        cols=st.columns(len(metrics))

        for i,row in metrics.iterrows():

            cols[i].metric(

                row["Metric"],

                round(row["Value"],3)

            )
            st.markdown("---")

            st.subheader("AI Model Summary")

            st.info("""

            ### Model Used
            Random Forest Regressor

            ### Input Features
            • NDVI (Vegetation Index)

            • NDWI (Water Index)

            • NDBI (Built-up Index)

            • Elevation (SRTM DEM)

            ### Prediction Target
            Land Surface Temperature (LST)

            ### Decision Support
            The Physics-Informed AI model combines satellite-derived indices with terrain information to estimate urban heat and recommend suitable mitigation strategies.

             """)
            st.markdown("---")

            st.subheader("AI Decision Process")

            st.success("""

            The AI recommends mitigation strategies based on:

            • High Land Surface Temperature (LST)

            • Low Vegetation (NDVI)

            • High Built-up Density (NDBI)

            • Water Availability (NDWI)

            • Terrain Elevation (DEM)

            The recommendation engine prioritizes solutions using:

            • Estimated Cooling Effect

            • Implementation Cost

            • Feasibility

            • Urban Suitability

             """) 

    else:

        st.warning("model_metrics.csv not found")

    st.markdown("---")

    if len(importance)>0:

        st.subheader("Model Feature Importance")

        fig=px.bar(

            importance,

            x="Importance",

            y="Feature",

            orientation="h",

            color="Importance",

            title="Feature Importance"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    else:

        st.warning("feature_importance.csv not found")

    st.markdown("---")

    if len(confidence)>0:

        st.subheader("Prediction Confidence Analysis")

        fig=px.histogram(

            confidence,

            x="Confidence (%)",

            nbins=30,

            title="Prediction Confidence Analysis Distribution"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    else:

        st.warning("prediction_confidence.csv not found")

# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

elif page=="Recommendations":

    st.title("AI Recommendations")
    st.caption("Recommendations generated for Hyderabad Urban Heat Island mitigation.")
    if len(recommend)>0:

        st.dataframe(

            recommend,

            use_container_width=True,

            hide_index=True

        )

        st.markdown("---")

        top5=recommend.head(5)

        fig=px.bar(

            top5,

            x="Technique",

            y="Optimization Score",

            color="Category",

            title="Top Recommended Strategies"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    else:

        st.warning("optimized_scenarios.csv not found")

# --------------------------------------------------
# SCENARIO OPTIMIZER
# --------------------------------------------------

elif page=="Scenario":

    st.title("Scenario Optimizer")
    st.caption("Scenario analysis for Hyderabad metropolitan region.")
    if len(cooling)>0:

        st.dataframe(

            cooling,

            use_container_width=True,

            hide_index=True

        )

        st.markdown("---")

        plot=cooling.copy()

        plot["Bubble Size"]=plot["Estimated Cooling (°C)"].abs()+1

        fig=px.scatter(

            plot,

            x="Estimated Cost (₹)",

            y="Estimated Cooling (°C)",

            size="Bubble Size",

            color="Category",

            hover_name="Technique",

            title="Cooling vs Cost"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

        fig=px.bar(

            plot,

            x="Technique",

            y="Overall Score",

            color="Category",

            title="Overall Ranking"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    else:

        st.warning(

            "cooling_scenarios.csv not found"

        )# --------------------------------------------------
# BUDGET PLANNER
# --------------------------------------------------

elif page == "Budget":

    st.title("Budget Planner")
    st.caption("Estimated implementation budget for Hyderabad.")
    if len(budget) > 0:

        st.subheader("Budget Plans")

        st.dataframe(
            budget,
            use_container_width=True,
            hide_index=True
        )

        numeric_cols = budget.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:

            col = st.selectbox(
                "Select Budget Column",
                numeric_cols
            )

            fig = px.bar(
                budget,
                x=budget.columns[0],
                y=col,
                color=col,
                title="Budget Analysis"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.warning("budget_plans.csv not found")

    st.markdown("---")

    if len(implementation) > 0:

        st.subheader("Implementation Plan")

        st.dataframe(
            implementation,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning("implementation_plan.csv not found")
# --------------------------------------------------
# NOVELTY
# --------------------------------------------------

elif page == "Novelty":

    st.title("Project Novelty")

    st.success("""
### What makes our system unique?

✅ Physics-Informed AI for Urban Heat Prediction

✅ Multi-source Satellite Data Fusion
(Sentinel-2 + ERA5 + SRTM DEM)

✅ Explainable AI
(Reason + Recommended Action)

✅ Temperature-Triggered Recommendations

✅ Cost & Feasibility Based Decision Support

✅ Urban Planning Focused Recommendations

✅ AI Scenario Optimizer for Heat Mitigation

✅ Publication-quality GIS Maps

""")

    st.markdown("---")

    st.subheader("Innovation Highlights")

    st.write("""
Instead of only predicting Urban Heat Islands,
our system recommends practical mitigation
strategies based on:

- AI Prediction
- Land Surface Temperature
- Vegetation
- Water Availability
- Built-up Density
- Terrain Elevation
- Cost
- Feasibility

making it a complete **Decision Support System**
rather than just a prediction model.
""")
# --------------------------------------------------
# REPORTS
# --------------------------------------------------

elif page == "Reports":

    st.title("Reports")
    st.caption("Generated reports for Hyderabad Urban Heat Island Decision Support System.")
    reports = [

        "model_metrics.csv",

        "feature_importance.csv",

        "prediction_confidence.csv",

        "cooling_scenarios.csv",

        "optimized_scenarios.csv",

        "budget_plans.csv",

        "implementation_plan.csv",

        "cost_benefit_analysis.csv",

        "city_action_plan.csv"

    ]

    st.subheader("Generated Reports")

    for report in reports:

        file = DATA / report

        c1, c2 = st.columns([3,1])

        c1.write(report)

        if file.exists():

            with open(file, "rb") as f:

                c2.download_button(

                    "⬇ Download",

                    f,

                    file_name=report,

                    key=report

                )

        else:

            c2.write("❌ Missing")

    st.markdown("---")

    st.subheader("Project Summary")

    st.write("""

### ISRO BHARATIYA ANTARIKSH HACKATHON 2026

  AI Urban Heat Island Decision Support System

 Study Area
 Hyderabad, Telangana, India

This project predicts Urban Heat Island intensity using

- NDVI
- NDWI
- NDBI
- Elevation

The Physics-Informed AI model recommends

- Urban Forest
- Urban Waterbody Restoration
- Pond Restoration
- Cool Roof
- White Lime Roof
- Green Roof

The Scenario Optimizer ranks solutions based on

- Cooling Performance
- Cost
- Feasibility

Generated automatically for the

**ISRO Hackathon 2026**

""")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(

"""

<center>

<h4>AI Urban Heat Island Decision Support System</h4>

ISRO Hackathon 2026

<br>

Physics-Informed AI Decision Support Platform

</center>

""",

unsafe_allow_html=True

)