import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import rasterio
import matplotlib.pyplot as plt
from pathlib import Path

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

st.sidebar.title("🛰 ISRO Dashboard")

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Home",

        "🛰 Satellite",

        "🤖 AI Analytics",

        "🌳 Recommendations",

        "📊 Scenario",

        "💰 Budget",

        "📄 Reports"

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

if page=="🏠 Home":

    st.title("🛰 AI Urban Heat Island Decision Support System")

    st.write(

        "Physics-Informed AI based Decision Support Platform"

    )

    if len(feature)>0:

        c1,c2,c3,c4=st.columns(4)

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

            "Pixels",

            len(feature)

        )

        st.markdown("---")

        fig=px.histogram(

            feature,

            x="lst",

            nbins=40,

            title="Land Surface Temperature"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

        fig=px.scatter(

            feature.sample(

                min(

                    5000,

                    len(feature)

                )

            ),

            x="ndvi",

            y="lst",

            color="ndbi",

            title="NDVI vs LST"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    else:

        st.warning(

            "feature_stack_ai.csv not found"

        )

# --------------------------------------------------
# SATELLITE
# --------------------------------------------------

elif page=="🛰 Satellite":

    st.title("🛰 Satellite Layers")

    layers={

        "NDVI":"ndvi.tif",

        "NDWI":"ndwi.tif",

        "NDBI":"ndbi.tif",

        "LST":"lst.tif",

        "Heat Risk":"heat_risk.tif"

    }

    choice=st.selectbox(

        "Select Layer",

        list(

            layers.keys()

        )

    )

    file=DATA/layers[choice]

    if file.exists():

        image=raster(file)

        fig,ax=plt.subplots(

            figsize=(8,8)

        )

        ax.imshow(

            image,

            cmap="viridis"

        )

        ax.set_title(choice)

        ax.axis("off")

        st.pyplot(fig)

    else:

        st.error(

            "Raster not found"

        )# --------------------------------------------------
# AI ANALYTICS
# --------------------------------------------------

elif page=="🤖 AI Analytics":

    st.title("🤖 AI Analytics")

    if len(metrics)>0:

        st.subheader("Model Performance")

        cols=st.columns(len(metrics))

        for i,row in metrics.iterrows():

            cols[i].metric(

                row["Metric"],

                round(row["Value"],3)

            )

    else:

        st.warning("model_metrics.csv not found")

    st.markdown("---")

    if len(importance)>0:

        st.subheader("Feature Importance")

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

        st.subheader("Prediction Confidence")

        fig=px.histogram(

            confidence,

            x="Confidence (%)",

            nbins=30,

            title="Prediction Confidence Distribution"

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

elif page=="🌳 Recommendations":

    st.title("🌳 AI Recommendations")

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

elif page=="📊 Scenario":

    st.title("📊 Scenario Optimizer")

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

elif page == "💰 Budget":

    st.title("💰 Budget Planner")

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
# REPORTS
# --------------------------------------------------

elif page == "📄 Reports":

    st.title("📄 Reports")

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

### AI Urban Heat Island Decision Support System

This project predicts Urban Heat Island intensity using

- NDVI
- NDWI
- NDBI
- Elevation

The Physics-Informed AI model recommends

- Urban Forest
- Temple Tank Restoration
- Village Pond Restoration
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

<h4>🛰 AI Urban Heat Island Decision Support System</h4>

ISRO Hackathon 2026

<br>

Physics-Informed AI Decision Support Platform

</center>

""",

unsafe_allow_html=True

)