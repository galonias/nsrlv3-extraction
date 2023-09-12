import re
import sys
import os
import csv

# Check if the user provided a command-line argument for the SQL script file
if len(sys.argv) != 2:
    print("Usage: python extract_md5_to_files.py <path_to_sql_script>")
    sys.exit(1)

# Get the SQL script file path from the command-line argument
sql_script_file = sys.argv[1]

# Check if the SQL script file exists
if not os.path.exists(sql_script_file):
    print(f"Error: The file '{sql_script_file}' does not exist.")
    sys.exit(1)

# Initialize lists to store MD5 values
md5_values = []

# Use regular expression to extract MD5 values line by line
md5_pattern = r"'([A-Fa-f0-9]{32})'"

with open(sql_script_file, 'r') as file:
    for line in file:
        md5_matches = re.findall(md5_pattern, line)
        md5_values.extend(md5_matches)

# Generate the text output file name
output_text_file = os.path.splitext(sql_script_file)[0] + "_md5.txt"

# Generate the CSV output file name
output_csv_file = os.path.splitext(sql_script_file)[0] + "_md5.csv"

# Write the MD5 values to the text file
with open(output_text_file, 'w') as textfile:
    for md5 in md5_values:
        textfile.write(md5 + '\n')

# Write the MD5 values to the CSV file
with open(output_csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['MD5'])
    for md5 in md5_values:
        writer.writerow([md5])

print(f"Text file '{output_text_file}' and CSV file '{output_csv_file}' have been created with MD5 values.")
