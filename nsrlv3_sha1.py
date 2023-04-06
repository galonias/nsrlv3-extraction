import argparse
import csv
import sqlite3
import tempfile
import zipfile
import os.path

parser = argparse.ArgumentParser(description='Extract unique SHA1 combinations from an SQLite database inside a zip file.')
parser.add_argument('zip_file', type=str, help='path to the zip file containing the SQLite database')
args = parser.parse_args()

# Open the zip file and retrieve the SQLite database
with zipfile.ZipFile(args.zip_file) as zip_file:
    db_file_name = None
    for file_name in zip_file.namelist():
        if file_name.endswith(".db"):
            db_file_name = file_name
            break
    if db_file_name is None:
        raise ValueError("No SQLite database file found in the zip file")
    with zip_file.open(db_file_name) as db_file:
        # Create a temporary file to store the database contents
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(db_file.read())
        temp_file.close()

        # Connect to the SQLite database
        conn = sqlite3.connect(temp_file.name)
        conn.execute("PRAGMA foreign_keys = ON")
        c = conn.cursor()

        # Retrieve unique combinations of md5 and sha1 values
        unique_values = set()
        for row in c.execute("SELECT sha1 FROM METADATA"):
            unique_values.add((row[0], row[1]))

        # Construct the output file name from the database file name
        output_file_name = os.path.splitext(os.path.basename(db_file_name))[0] + ".csv"

        # Write the unique combinations to the output CSV file
        with open(output_file_name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["SHA1"])  # Write header row
            for md5, sha1 in unique_values:
                writer.writerow([sha1])

        # Close the database connection and delete the temporary file
        c.close()
        conn.close()
        temp_file.unlink()