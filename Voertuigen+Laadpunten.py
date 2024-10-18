import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os
 
# Constants
DEFAULT_NUM_SOLAR_PANELS = 12000
DEFAULT_ANNUAL_OUTPUT_PER_PANEL_KWH = 250

# Streamlit UI
st.title("Laadpunten Capaciteit Berekening")
st.sidebar.header("Instellingen")
 
# User inputs
num_solar_panels = st.sidebar.number_input("Aantal Zonnepanelen", min_value=1000, max_value=20000, value=DEFAULT_NUM_SOLAR_PANELS)
annual_output_per_panel_kwh = st.sidebar.number_input("Jaarlijkse Opbrengst per Zonnepaneel (kWh)", min_value=100, max_value=400, value=DEFAULT_ANNUAL_OUTPUT_PER_PANEL_KWH)
battery_capacity_busje = st.sidebar.number_input("Batterijcapaciteit Bestelbusje (kWh)", min_value=10, max_value=200, value=60)
battery_capacity_truck = st.sidebar.number_input("Batterijcapaciteit Truck (kWh)", min_value=100, max_value=1000, value=300)
energy_distribution = st.sidebar.slider("Energieverdeling tussen Bestelbusjes en Trucks (%)", min_value=0, max_value=100, value=50)
 
# Charger settings
charger_power_normal = st.sidebar.number_input("Vermogen Normale Lader (kW)", min_value=1, max_value=50, value=22)
charger_power_fast = st.sidebar.number_input("Vermogen Snellader (kW)", min_value=50, max_value=350, value=150)
charger_distribution = st.sidebar.slider("Verhouding Normale Laders en Snelladers (%)", min_value=0, max_value=100, value=50)
 
# Calculate total energy production
total_annual_energy_production_kwh = num_solar_panels * annual_output_per_panel_kwh
daily_energy_production_kwh = total_annual_energy_production_kwh / 365
 
# Calculate energy allocation
energy_for_busjes = daily_energy_production_kwh * (energy_distribution / 100)
energy_for_trucks = daily_energy_production_kwh * ((100 - energy_distribution) / 100)
 
 
# Function to calculate the number of vehicles that can be charged daily
def calculate_vehicles_charged(daily_energy_production, battery_capacity):
    return daily_energy_production / battery_capacity
 
# Function to calculate the number of charging points needed
def calculate_charging_points(daily_energy_production, usage_hours_per_day, charger_power_kw):
    energy_per_charger_per_day = charger_power_kw * usage_hours_per_day
    return daily_energy_production / energy_per_charger_per_day
 
# Function to calculate the charging time for vehicles
def calculate_charging_time(battery_capacity, charger_power_kw):
    return battery_capacity / charger_power_kw
 
# Calculations for vehicles charged
num_busjes_charged = calculate_vehicles_charged(energy_for_busjes, battery_capacity_busje)
num_trucks_charged = calculate_vehicles_charged(energy_for_trucks, battery_capacity_truck)
 
# # Plotting bar chart for vehicles charged
# fig, ax = plt.subplots()
# vehicles = ['Bestelbusjes', 'Trucks']
# num_vehicles_charged = [num_busjes_charged, num_trucks_charged]
# ax.bar(vehicles, num_vehicles_charged, color=['blue', 'green'])
# ax.set_ylabel('Aantal Voertuigen Opgeladen per Dag')
# ax.set_title('Aantal Voertuigen dat Dagelijks kan worden Opgeladen met Zonne-energie')
 
# Data to plot 
vehicles = ['Bestelbusjes', 'Trucks']
num_vehicles_charged = [num_busjes_charged, num_trucks_charged]
colors = ['blue', 'green']

# Function to display both percentage and number
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n({val:d})'
    return my_format

# Plotting the pie chart
fig, ax = plt.subplots()
ax.pie(num_vehicles_charged, labels=vehicles, colors=colors, autopct=autopct_format(num_vehicles_charged), startangle=140)

# Adding title and displaying the chart
ax.set_title('Aantal Voertuigen dat Dagelijks kan worden Opgeladen met Zonne-energie')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the plot with Streamlit
st.pyplot(fig)
st.write(f"Met {num_solar_panels} zonnepanelen kunnen dagelijks ongeveer {int(num_busjes_charged)} elektrische bestelbusjes en {int(num_trucks_charged)} elektrische trucks volledig worden opgeladen.")
 
# User input for number of vehicles and usage hours per day
num_busjes = st.number_input("Aantal Bestelbusjes", min_value=0, value=10)
num_trucks = st.number_input("Aantal Trucks", min_value=0, value=5)
usage_hours_per_day = st.number_input("Gebruik per Dag per Laadpunt (uren)", min_value=1, max_value=24, value=8)
 
# Calculate total energy required for the given number of vehicles
total_energy_required_busjes = num_busjes * battery_capacity_busje
total_energy_required_trucks = num_trucks * battery_capacity_truck
total_energy_required = total_energy_required_busjes + total_energy_required_trucks
 
# Assuming these functions are defined elsewhere in the code
def calculate_charging_points(energy_required, usage_hours, charger_power):
    return energy_required / (usage_hours * charger_power)

def calculate_charging_time(battery_capacity, charger_power):
    return battery_capacity / charger_power

# Calculate the number of charging points needed for the given number of vehicles with normal and fast chargers
charging_points_normal_busjes = calculate_charging_points(total_energy_required_busjes * (charger_distribution / 100), usage_hours_per_day, charger_power_normal)
charging_points_fast_busjes = calculate_charging_points(total_energy_required_busjes * ((100 - charger_distribution) / 100), usage_hours_per_day, charger_power_fast)

charging_points_normal_trucks = calculate_charging_points(total_energy_required_trucks * (charger_distribution / 100), usage_hours_per_day, charger_power_normal)
charging_points_fast_trucks = calculate_charging_points(total_energy_required_trucks * ((100 - charger_distribution) / 100), usage_hours_per_day, charger_power_fast)

# Calculate the charging time for vehicles with normal and fast chargers
charging_time_normal_busje = calculate_charging_time(battery_capacity_busje, charger_power_normal)
charging_time_fast_busje = calculate_charging_time(battery_capacity_busje, charger_power_fast)

charging_time_normal_truck = calculate_charging_time(battery_capacity_truck, charger_power_normal)
charging_time_fast_truck = calculate_charging_time(battery_capacity_truck, charger_power_fast)
 
# Check if the total energy required is within the daily energy production limit
if total_energy_required <= daily_energy_production_kwh:
    st.success("De opgegeven aantallen voertuigen kunnen volledig worden opgeladen met de beschikbare zonne-energie.")
else:
    energy_deficit = total_energy_required - daily_energy_production_kwh
    st.error(f"De opgegeven aantallen voertuigen kunnen niet volledig worden opgeladen met de beschikbare zonne-energie. Er ontbreekt {energy_deficit:.2f} kWh aan zonne-energie. Overweeg om het aantal voertuigen te verminderen of de batterijcapaciteit aan te passen.")

# Display the number of charging points needed and charging time for normal and fast chargers
st.subheader("Benodigde Laadpunten")
st.write(f"Aantal benodigde normale laadpunten voor bestelbusjes: **{int(charging_points_normal_busjes)}**")
st.write(f"Aantal benodigde snellaadpunten voor bestelbusjes: **{int(charging_points_fast_busjes)}**")
st.write(f"Aantal benodigde normale laadpunten voor trucks: **{int(charging_points_normal_trucks)}**")
st.write(f"Aantal benodigde snellaadpunten voor trucks: **{int(charging_points_fast_trucks)}**")

st.subheader("Laadtijd")
st.write(f"Laadtijd voor een bestelbusje met normale lader: **{charging_time_normal_busje:.2f} uur**")
st.write(f"Laadtijd voor een bestelbusje met snellader: **{charging_time_fast_busje:.2f} uur**")
st.write(f"Laadtijd voor een truck met normale lader: **{charging_time_normal_truck:.2f} uur**")
st.write(f"Laadtijd voor een truck met snellader: **{charging_time_fast_truck:.2f} uur**")

 
# Laad het CSV-bestand in een DataFrame


# Get the directory where the current script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
 
# Build the path to the CSV file in the subfolder
file_path = os.path.join(current_dir, 'zon-2023-uur-data.csv')
print(file_path)
 
# Reading the CSV file
df = pd.read_csv(file_path)

# df = pd.read_csv('C:\\Users\\robva\\Desktop\\HACKATON\\hackathon\\pages\\zon-2023-uur-data.csv')
 
# Zet de 'validfrom (UTC)' kolom om naar datetime
df['validfrom (UTC)'] = pd.to_datetime(df['validfrom (UTC)'])
 
# Filter de data om alleen 2023 te houden
df = df[df['validfrom (UTC)'].dt.year == 2023]

# Groepeer per dag en bereken de totale capaciteit (kW) per dag
daily_capacity = df.groupby(df['validfrom (UTC)'].dt.date)['capacity (kW)'].sum().reset_index()
daily_capacity.columns = ['date', 'total_capacity_kW']
 
# Voeg de dagelijkse capaciteit terug aan de originele DataFrame
df = df.merge(daily_capacity, left_on=df['validfrom (UTC)'].dt.date, right_on='date')
 
# Bereken het percentage van de capaciteit per uur ten opzichte van de dagelijkse totale capaciteit
df['capacity_percentage'] = (df['capacity (kW)'] / df['total_capacity_kW']) * 100
 
# Zet de 'validfrom (UTC)' kolom om naar alleen de datum en het uur
df['date'] = df['validfrom (UTC)'].dt.date
df['hour'] = df['validfrom (UTC)'].dt.hour
df['month'] = df['validfrom (UTC)'].dt.month
df['quarter'] = df['validfrom (UTC)'].dt.to_period('Q')
 
# Streamlit app
st.title("Capaciteitspercentage Analyse")
 
# Selectie voor maand of kwartaal
option = st.selectbox("Selecteer een optie:", ["Maand", "Kwartaal"])  # Dag is verwijderd
 
if option == "Maand":
    selected_month = st.selectbox("Selecteer een maand:", range(1, 13))
    monthly_data = df[df['month'] == selected_month]
   
    # Bereken het gemiddelde percentage per uur voor de geselecteerde maand
    hourly_percentage = monthly_data.groupby('hour')['capacity_percentage'].mean().reset_index()
 
    # Plotly grafiek met vloeiende lijnen
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hourly_percentage['hour'],
                              y=hourly_percentage['capacity_percentage'],
                              mode='lines+markers',
                              name='Gemiddeld Capaciteitspercentage',
                              line=dict(shape='spline', smoothing=1.3)))  # Vloeiende lijn
    fig.update_layout(title=f'Gemiddeld Capaciteitspercentage per uur in maand {selected_month}',
                      xaxis_title='Uur van de dag',
                      yaxis_title='Gemiddeld Capaciteitspercentage (%)',
                      xaxis=dict(tickmode='array', tickvals=list(range(0, 24)), ticktext=[str(i) for i in range(0, 25)]))  # Uren van 0 tot 24
    st.plotly_chart(fig)
 
elif option == "Kwartaal":
    selected_quarter = st.selectbox("Selecteer een kwartaal:", ['Q1', 'Q2', 'Q3', 'Q4'])
    quarterly_data = df[df['quarter'].astype(str) == f'2023{selected_quarter}']
   
    # Bereken het gemiddelde percentage per uur voor de geselecteerde kwartaal
    hourly_percentage = quarterly_data.groupby('hour')['capacity_percentage'].mean().reset_index()
 
    # Plotly grafiek met vloeiende lijnen
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hourly_percentage['hour'],
                              y=hourly_percentage['capacity_percentage'],
                              mode='lines+markers',
                              name='Gemiddeld Capaciteitspercentage',
                              line=dict(shape='spline', smoothing=1.3)))  # Vloeiende lijn
    fig.update_layout(title=f'Gemiddeld Capaciteitspercentage per uur in kwartaal {selected_quarter}',
                      xaxis_title='Uur van de dag',
                      yaxis_title='Gemiddeld Capaciteitspercentage (%)',
                      xaxis=dict(tickmode='array', tickvals=list(range(0, 24)), ticktext=[str(i) for i in range(0, 25)]))  # Uren van 0 tot 24
    st.plotly_chart(fig)