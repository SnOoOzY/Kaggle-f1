import pandas as pd
import numpy as np
import zipfile

# Define paths
data = 'C:/Users/lewis/Downloads/f1data.zip'
qualifying_csv_filename = 'qualifying.csv'
races_csv_filename = 'races.csv'

# Load qualifying data
with zipfile.ZipFile(data, 'r') as zip_archive:
    with zip_archive.open(qualifying_csv_filename) as csv_file:
        qualifying_data = pd.read_csv(csv_file)

# Load races data
with zipfile.ZipFile(data, 'r') as zip_archive:
    with zip_archive.open(races_csv_filename) as csv_file:
        races_data = pd.read_csv(csv_file)

# Get the race IDs for the Italian Grand Prix
monza_races = races_data[races_data['name'] == 'Italian Grand Prix']
monza_race_ids = monza_races['raceId'].unique()

# Filter qualifying data for Monza races
monza_qualifying = qualifying_data[qualifying_data['raceId'].isin(monza_race_ids)].copy()  # Make a copy

# Replace '\N' with NaN
monza_qualifying['q1'] = monza_qualifying['q1'].replace('\\N', np.nan)
monza_qualifying['q2'] = monza_qualifying['q2'].replace('\\N', np.nan)
monza_qualifying['q3'] = monza_qualifying['q3'].replace('\\N', np.nan)

# Print the unique times to check the format before conversion
print("Unique Q1 times:", monza_qualifying['q1'].unique())
print("Unique Q2 times:", monza_qualifying['q2'].unique())
print("Unique Q3 times:", monza_qualifying['q3'].unique())

# Convert time columns to timedelta, handling errors
monza_qualifying.loc[:, 'q1'] = pd.to_timedelta(monza_qualifying['q1'], errors='coerce')
monza_qualifying.loc[:, 'q2'] = pd.to_timedelta(monza_qualifying['q2'], errors='coerce')
monza_qualifying.loc[:, 'q3'] = pd.to_timedelta(monza_qualifying['q3'], errors='coerce')

# Check data types to confirm conversion
print(monza_qualifying[['q1', 'q2', 'q3']].dtypes)

# Print the number of NaT values
print(monza_qualifying[['q1', 'q2', 'q3']].isna().sum())

# Find the fastest times
fastest_q1 = monza_qualifying['q1'].min()
fastest_q2 = monza_qualifying['q2'].min()
fastest_q3 = monza_qualifying['q3'].min()

# Display the fastest times
print(f'Fastest Q1 time: {fastest_q1}')
print(f'Fastest Q2 time: {fastest_q2}')
print(f'Fastest Q3 time: {fastest_q3}')
