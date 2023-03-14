# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Task complete text
print("Import Libraries complete")

# Ask user for number of GPS ranges
num_ranges = int(input("Enter number of GPS ranges: "))

# Initialize empty dataframe to store filtered occurrences
occurrences = pd.DataFrame(columns=['gbifID', 'decimalLatitude', 'decimalLongitude', 'eventDate', 'file_path'])

# Loop through each GPS range
for i in range(num_ranges):
    # Ask user for latitude and longitude range
    lat_range = input("Enter latitude range (min,max): ")
    lon_range = input("Enter longitude range (min,max): ")
    lat_min, lat_max = [float(x) for x in lat_range.split(',')]
    lon_min, lon_max = [float(x) for x in lon_range.split(',')]

    # Ask user for number of CSVs to use and their file paths
    num_csvs = int(input("Enter number of CSVs: "))
    file_names = []
    for j in range(num_csvs):
        csv_num = j + 1
        file_path = input(f"Enter CSV file path for CSV {csv_num}: ")
        file_name = os.path.basename(file_path)
        file_names.append(file_name)
        print(f"{file_name} added.")

    # Loop through each CSV file
    for file_name in file_names:
        print(f"Filtering {file_name} to GPS range")
        # Get the full file path for the current CSV file
        file_path = os.path.join(os.getcwd(), file_name)

        # Read in CSV and extract relevant columns
        data = pd.read_csv(file_path, usecols=['gbifID', 'decimalLatitude', 'decimalLongitude', 'eventDate'], delimiter='\t')

        # Filter occurrences by GPS range
        filtered = data.loc[(data['decimalLatitude'] >= lat_min) & (data['decimalLatitude'] <= lat_max) &
                            (data['decimalLongitude'] >= lon_min) & (data['decimalLongitude'] <= lon_max)]

        # Parse eventDate column into Year and Month columns
        filtered['Year'] = pd.to_datetime(filtered['eventDate']).dt.year
        filtered['Month'] = pd.to_datetime(filtered['eventDate']).dt.month_name().str.slice(stop=3)
        filtered = filtered.drop(columns=['eventDate'])
        filtered['file_path'] = file_path  # add file_path column

        # Add filtered occurrences to overall dataframe
        occurrences = occurrences.append(filtered, ignore_index=True)
        
    # Task complete text
    print("Complete")

    # Create subsections of GPS ranges that are 0.05 by 0.05
    print("Craeting GPS subsections")
    lat_bins = pd.cut(occurrences['decimalLatitude'], bins=int((lat_max-lat_min)/0.05), precision=2)
    lon_bins = pd.cut(occurrences['decimalLongitude'], bins=int((lon_max-lon_min)/0.05), precision=2)

    # Task complete text
    print("Complete")

    # Count occurrences in each subsection and filter out empty subsections
    print("Counting occurrences in subsections")
    subsections = occurrences.groupby([lat_bins, lon_bins]).size().reset_index(name='count')
    subsections = subsections.loc[subsections['count'] > 0]
    subsections = subsections.rename(columns={'decimalLatitude': 'lat', 'decimalLongitude': 'lon'})

    # Task complete text
    print("Complete")

    # Loop through each subsection
    print("Creating figures")
    for i, subsection in subsections.iterrows():
        # Get the occurrences in the current subsection
        lat_range = subsection['lat'].mid
        lon_range = subsection['lon'].mid
        filtered = occurrences.loc[(lat_bins == subsection['lat']) & (lon_bins == subsection['lon'])]

        # Group occurrences by month and CSV file
        group = filtered.groupby(['Month', 'file_path']).size().reset_index(name='count')

        # Filter out months with no occurrences in all CSVs
        months = group['Month'].unique()
        for month in months:
            if (group.loc[group['Month'] == month, 'file_path'].nunique() < len(file_names)):
                group = group.loc[group['Month'] != month]

        # Plot bar graph if there are months with occurrences from all CSVs
        if len(group) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            for file_path, file_group in group.groupby('file_path'):
                ax.bar(file_group['Month'], file_group['count'], label=os.path.basename(file_path))
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of Occurrences')
            ax.set_title(f"GPS Range: {lat_range:.2f},{lon_range:.2f}")
            plt.xticks(rotation=45)
            ax.legend()
            plt.tight_layout()
            plt.show()
        
# Script complete text
print("Script finished")