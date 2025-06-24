import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium
import folium

# Create mock grid data
@st.cache_data
def generate_mock_data(rows=5, cols=5):
    base_lat = 56.2   # Approx. latitude for central Denmark
    base_lon = 10.2   # Approx. longitude for central Denmark
    data = []
    for i in range(rows):
        for j in range(cols):
            lat = base_lat + i * 0.001  # smaller grid spacing
            lon = base_lon + j * 0.001
            ph = np.random.uniform(5.5, 7.5)
            nitrogen = np.random.uniform(10, 50)
            phosphorus = np.random.uniform(5, 20)
            potassium = np.random.uniform(20, 80)
            data.append({
                'Latitude': lat,
                'Longitude': lon,
                'pH': ph,
                'Nitrogen (mg/kg)': nitrogen,
                'Phosphorus (mg/kg)': phosphorus,
                'Potassium (mg/kg)': potassium
            })
    return pd.DataFrame(data)

# Load mock data
df = generate_mock_data()

# UI with tabs
st.title("Soil Health Insights")
tab1, tab2, tab3 = st.tabs(["Graphs", "Data", "Map"])

# Graphs Tab
with tab1:
    st.header("Graphs of Soil Health Metrics")
    metric = st.selectbox("Choose a metric to plot:", ["pH", "Nitrogen (mg/kg)", "Phosphorus (mg/kg)", "Potassium (mg/kg)"])
    fig = px.scatter(df, x="Longitude", y="Latitude", color=metric, size=metric, color_continuous_scale="Viridis")
    st.plotly_chart(fig)

# Data Tab
with tab2:
    st.header("Raw Data and Metadata")
    st.dataframe(df)
    st.markdown("**Metadata:** Grid of soil samples from synthetic geographic locations in California. Each point represents a soil sample with nutrient data.")

# Map Tab
with tab3:
    st.header("Map of Sample Locations")
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)
    for _, row in df.iterrows():
        popup_info = f"pH: {row['pH']:.2f}<br>N: {row['Nitrogen (mg/kg)']:.1f}<br>P: {row['Phosphorus (mg/kg)']:.1f}<br>K: {row['Potassium (mg/kg)']:.1f}"
        folium.CircleMarker(location=[row['Latitude'], row['Longitude']],
                            radius=5,
                            popup=popup_info,
                            color='blue',
                            fill=True,
                            fill_color='blue').add_to(m)
    st_folium(m, width=700, height=500)
