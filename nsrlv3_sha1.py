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

    # Construct the output file name from the database file name
    output_file_name = os.path.splitext(os.path.basename(db_file_name))[0] + ".txt"

    # Determine the output file path
    output_file_path = os.path.join(os.path.dirname(args.zip_file), output_file_name)

    # Check if the output file already exists
    if os.path.exists(output_file_path):
        # Prompt the user for confirmation to overwrite the file
        user_input = input("The output file already exists. Do you want to overwrite it? (y/n): ")
        if user_input.lower() != "y":
            print("Operation canceled. The existing file was not overwritten.")
            exit()

    with zip_file.open(db_file_name) as db_file:
        # Create a temporary file next to the zip file to store the database contents
        temp_file_path = os.path.join(os.path.dirname(args.zip_file), os.path.splitext(os.path.basename(args.zip_file))[0] + ".db")
        temp_file = open(temp_file_path, 'wb')
        chunk_size = 1024 * 1024  # 1 MB
        while True:
            chunk = db_file.read(chunk_size)
            if not chunk:
                break
            temp_file.write(chunk)
        temp_file.close()

        # Connect to the SQLite database
        conn = sqlite3.connect(temp_file_path)
        conn.execute("PRAGMA foreign_keys = ON")
        c = conn.cursor()

        # Retrieve unique combinations of sha1 values
        query = "SELECT DISTINCT sha1 FROM DISTINCT_HASH"
        unique_values = (row[0] for row in c.execute(query))

        # Write the unique combinations to the output text file next to the zip file
        with open(output_file_path, "w") as txtfile:
            for value in unique_values:
                txtfile.write(str(value) + "\n")

        # Close the database connection and delete the temporary file
        c.close()
        conn.close()
        os.remove(temp_file_path)
