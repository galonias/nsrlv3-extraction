import re
import sys
import os
import csv

# Check if the user provided a command-line argument for the SQL script file
if len(sys.argv) != 2:
    print("Usage: python extract_sha1_to_files.py <path_to_sql_script>")
    sys.exit(1)

# Get the SQL script file path from the command-line argument
sql_script_file = sys.argv[1]

# Check if the SQL script file exists
if not os.path.exists(sql_script_file):
    print(f"Error: The file '{sql_script_file}' does not exist.")
    sys.exit(1)

# Initialize lists to store SHA1 values
sha1_values = []

# Use regular expression to extract SHA1 values line by line
sha1_pattern = r"'([A-Fa-f0-9]{40})'"

with open(sql_script_file, 'r') as file:
    for line in file:
        sha1_matches = re.findall(sha1_pattern, line)
        sha1_values.extend(sha1_matches)

# Generate the text output file name
output_text_file = os.path.splitext(sql_script_file)[0] + "_sha1.txt"

# Generate the CSV output file name
output_csv_file = os.path.splitext(sql_script_file)[0] + "_sha1.csv"

# Write the SHA1 values to the text file
with open(output_text_file, 'w') as textfile:
    for sha1 in sha1_values:
        textfile.write(sha1 + '\n')

# Write the SHA1 values to the CSV file
with open(output_csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['SHA1'])
    for sha1 in sha1_values:
        writer.writerow([sha1])

print(f"Text file '{output_text_file}' and CSV file '{output_csv_file}' have been created with SHA1 values.")
