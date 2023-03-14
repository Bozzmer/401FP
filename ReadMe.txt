##GPS Occurrences Analysis##
This Python script analyzes GPS occurrence data from multiple CSV files, filtering by user-defined GPS ranges, and grouping occurrences into subsections that are 0.05 by 0.05 degrees. The script then creates bar graphs for each subsection that show the number of occurrences in each month for each CSV file.

#Required Libraries#
- pandas
- matplotlib
- os
- numpy

#Usage#
1. Place all CSV files to be analyzed in the same directory as this Python script.
2. Run the script.
3. When prompted, enter the number of GPS ranges to analyze.
4. For each GPS range, enter the latitude and longitude range, the number of CSV files to use, and the file paths for those CSV files.
5. The script will output bar graphs for each subsection that contains occurrences from all CSV files.

#Output#
The script outputs bar graphs for each subsection that contains occurrences from all CSV files. Each bar graph shows the number of occurrences in each month for each CSV file. The bar graphs are titled with the GPS range of the subsection.

#Note#
- The script assumes that each CSV file contains the columns 'gbifID', 'decimalLatitude', 'decimalLongitude', and 'eventDate', separated by tabs.
- The script filters out subsections that contain no occurrences.