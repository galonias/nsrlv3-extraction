import argparse
import csv
import sqlite3
import tempfile
import zipfile
import os

parser = argparse.ArgumentParser(description='Extract unique MD5 and SHA1 combinations from an SQLite database inside a zip file.')
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
        # Create a temporary file next to the zip file to store the database contents
        temp_file_name = os.path.join(os.path.dirname(args.zip_file), "temp.db")
        with open(temp_file_name, 'wb') as temp_file:
            chunk_size = 1024 * 1024  # 1 MB
            while True:
                chunk = db_file.read(chunk_size)
                if not chunk:
                    break
                temp_file.write(chunk)

        # Connect to the SQLite database
        conn = sqlite3.connect(temp_file_name)
        conn.execute("PRAGMA foreign_keys = ON")
        c = conn.cursor()

        # Retrieve unique combinations of sha1 values
        unique_values = set()
        for row in c.execute("SELECT sha1 FROM FILE"):
            unique_values.add((row[0], row[1]))

        # Construct the output file name from the database file name
        output_file_name = os.path.splitext(os.path.basename(db_file_name))[0] + ".csv"
        output_file_path = os.path.join(os.path.dirname(args.zip_file), output_file_name)

        # Write the unique combinations to the output CSV file
        with open(output_file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["sha1"])  # Write header row
            for md5 in unique_values:
                writer.writerow([sha1])

        # Close the database connection and delete the temporary file
        c.close()
        conn.close()
        os.remove(temp_file_name)
