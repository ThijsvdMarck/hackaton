#deelvraag2
#hackathon
 
#%% import libaries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import os
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from folium import Marker
 
  
st.set_page_config(
     page_title="Hackaton"
)
 
#%% File location & file reading
# Get the directory where the current script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
 
# Build the path to the CSV file in the subfolder
file_path = os.path.join(current_dir, 'data', 'Sloterdijk_poort_noord.csv')
print(file_path)
 
# Reading the CSV file
Sloterdijk = pd.read_csv(file_path)
 
# print(Sloterdijk.head())
# print(Sloterdijk.info())
 
#%% Streamlit 1 foliumkaart
 
# Step 1: Add the text information about Sloterdijk Poort Noord above the map
st.title('Company Map at Sloterdijk Poort Noord')
st.write('Sloterdijk Poort Noord, located in Amsterdam’s business hub, houses diverse companies with various office sizes. It offers strategic access and connectivity, with postal code 1014 covering the area.')
 
# Step 2: Set the center of the map to the average coordinates of the dataset
center_lat = Sloterdijk['Lat'].mean()
center_long = Sloterdijk['Long'].mean()
 
# Step 3: Create a Folium map centered at the calculated average coordinates
m = folium.Map(location=[center_lat, center_long], zoom_start=15)
 
# Step 4: Add markers for each company with a popup showing company details
for _, row in Sloterdijk.iterrows():
    popup_text = f"""
    <b>Bedrijfsnaam:</b> {row['Bedrijfsnaam']}<br>
    <b>Address:</b> {row['Adress']}<br>
    <b>PostCode:</b> {row['PostCode']}<br>
    <b>Oppervlakte Gebouw (m²):</b> {row['oppervlakte_gebouw_m2']}
    """
    Marker([row['Lat'], row['Long']], popup=popup_text).add_to(m)
 
# Step 5: Display the map using Streamlit
st.write('Click on the pins to see company details.')
st_folium(m, width=925, height=600)
 
 
#%% Streamlit 2 piechart
 
# Filter out rows where Aantal_Zonnepaneel_googlemaps is NaN or 0 for better visualization
Sloterdijk = Sloterdijk[Sloterdijk['Aantal_Zonnepaneel_googlemaps'] > 0]
 
# Prepare the data for the pie chart
labels = Sloterdijk.apply(lambda row: f"{row['Bedrijfsnaam']} ({int(row['Aantal_Zonnepaneel_googlemaps'])} panels)", axis=1)
values = Sloterdijk['Aantal_Zonnepaneel_googlemaps']
 
# Create the pie chart using Plotly
fig = px.pie(
    Sloterdijk,
    values=values,
    names=labels,
    title="Distribution of Solar Panels by Company",
    hole=0.3
)
 
# Customize the chart to show only percentages on the pie and full label in the hover info
fig.update_traces(textinfo='percent', hoverinfo='label+percent')
 
# Display the chart in Streamlit
st.title('Solar Panel Distribution Pie Chart')
st.write('This chart shows the distribution of solar panels across companies.')
st.plotly_chart(fig)
 
 
 
#%% streamlit 3  barchart
 
# Prepare the data for the bar chart
companies = Sloterdijk['Bedrijfsnaam']
workers = Sloterdijk['Schatting_aantaal_werkende']
 
# Define a Vivid color scheme
vivid_colors = px.colors.qualitative.Vivid
 
# Create the horizontal bar chart using Plotly
fig = px.bar(
    Sloterdijk,
    x=workers,
    y=companies,
    title='Estimated Number of Workers by Company',
    labels={'x': 'Estimated Workers', 'y': 'Company Name'},
    orientation='h',  # Horizontal bar chart
    color=companies,   # This will assign a color to each company
    color_discrete_sequence=vivid_colors  # Use the vivid color scheme
)
 
# Adjust the layout to ensure all labels fit
fig.update_layout(
    height=800,  # Adjust height to fit all companies
    margin=dict(l=150)  # Adjust left margin for longer company names
)
 
# Display the chart in Streamlit
st.title('Estimated Number of Workers by Company')
st.write(f"Total number of companies: {len(companies)}")
st.write('This bar chart displays the estimated number of workers for each company.')
st.plotly_chart(fig)
 
#%% streamlit 4 scatterplot
 
# Step 1: Add header information as text above the scatter plot
st.title('Analysis of Building Utilization and Workforce Distribution')
st.write("""
This scatterplot compares Building Area (m²) and Number of Employees, allowing further analysis with variables like occupancy rates, usage hours, and employee density per m².
This provides insights into building utilization and workforce distribution.
""")
 
# Step 2: Dropdown for selecting the X-axis variable (including new options)
x_axis_options = {
    'Building Area (m²)': 'oppervlakte_gebouw_m2',
    'Workers per m²': 'werkende_per_m2',
    'Uur in Gebruik Dag': 'uur_in_gebruik_dag',
    'Uur in Gebruik Week': 'uur_in_gebruik_week',
    'Bezettingsgraad Dag Percentage': 'bezittingsgraad_dag_percentage',
    'Bezettingsgraad Week Percentage': 'bezittingsgraad_week_percentage'
}
 
selected_x_axis = st.selectbox('Select X-axis variable', list(x_axis_options.keys()))
 
# Step 3: Get the corresponding column name for the selected x-axis variable
x_axis_column = x_axis_options[selected_x_axis]
 
# Step 4: Scatter Plot - Selected X-axis variable vs. Number of Employees (Schatting_aantaal_werkende)
st.subheader(f"Scatterplot for {selected_x_axis} vs. Number of Employees")
 
# Create the scatter plot and color by company (Bedrijfsnaam)
fig = px.scatter(
    Sloterdijk,
    x=x_axis_column,
    y='Schatting_aantaal_werkende',
    title=f'{selected_x_axis} vs. Number of Employees',
    labels={
        x_axis_column: selected_x_axis,
        'Schatting_aantaal_werkende': 'Number of Employees'
    },
    hover_data=['Bedrijfsnaam'],  # Show company names on hover
    opacity=0.7,
    color='Bedrijfsnaam'  # Assign a unique color to each company
)
 
# Step 5: Display the scatter plot
st.plotly_chart(fig)
 
 
#%% Streamlit 5
 
# Step 1: Add header information as text above the bar chart and data
st.title('Sector Energy Cost Analysis')
st.write("""
The data presents key metrics for two sectors, focusing on Natural Gas Usage (m³) and Electricity Usage (kWh), along with the associated costs.
A bar chart visually compares Total Gas Cost (€) and Total Electricity Cost (€), highlighting the energy expenses for each sector and providing
insight into potential areas for cost optimization.
""")
 
# Step 2: Define the two sectors for filtering
sectors = {
    'Groothandel': 'Groothandel',
    'Vervoer en Opslag': 'Vervoer en opslag'
}
 
# Step 3: Create dropdown for sector selection
selected_sector = st.selectbox('Select Sector', list(sectors.keys()))
 
# Step 4: Filter the dataset based on the selected sector
filtered_data = Sloterdijk[Sloterdijk['Sector'] == sectors[selected_sector]]  # Assuming 'Sector' column exists
 
# Step 5: Calculate the key metrics for each company
filtered_data['Total Natural Gas Cost (€)'] = filtered_data['prijs_aardgas_m3'] * filtered_data['gemiddelde_aardgasverbruik_[m3]']
filtered_data['Total Electricity Cost (€)'] = filtered_data['prijs_kwh'] * filtered_data['gemiddelde_elektriciteitverbruik_[kwh]']
 
# Display headers
col1, col2, col3, col4, col5 = st.columns(5)
col1.markdown("**Company**")
col2.markdown("**Natural Gas Usage (m³)**")
col3.markdown("**Electricity Usage (kWh)**")
col4.markdown("**Total Gas Cost (€)**")
col5.markdown("**Total Electricity Cost (€)**")
 
# Display key metrics for each company in a nice layout
for index, row in filtered_data.iterrows():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Adjust font size and display the data
    col1.markdown(f"<p style='font-size:12px;'>{row['Bedrijfsnaam']}</p>", unsafe_allow_html=True)
    col2.markdown(f"<p style='font-size:12px;'>{row['gemiddelde_aardgasverbruik_[m3]']}</p>", unsafe_allow_html=True)
    col3.markdown(f"<p style='font-size:12px;'>{row['gemiddelde_elektriciteitverbruik_[kwh]']}</p>", unsafe_allow_html=True)
    col4.markdown(f"<p style='font-size:12px;'>{row['Total Natural Gas Cost (€)']:.2f}</p>", unsafe_allow_html=True)
    col5.markdown(f"<p style='font-size:12px;'>{row['Total Electricity Cost (€)']:.2f}</p>", unsafe_allow_html=True)
 
# Step 6: Create a stacked bar chart using Plotly
fig = px.bar(
    filtered_data,
    x='Bedrijfsnaam',
    y=['Total Natural Gas Cost (€)', 'Total Electricity Cost (€)'],
    title=f'Total Costs for {selected_sector}',
    labels={'value': 'Cost (€)', 'variable': 'Cost Type'},
    barmode='stack'  # Stack the bars for natural gas and electricity costs
)
 
# Step 7: Display the bar chart in Streamlit
st.plotly_chart(fig)
 
