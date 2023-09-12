# Extract NSRL hashes

Please note that this script is entirely written by ChatGPT and should be used with caution.

## About

Since the official method is time consuming and requires a lot of manual labor and intervention to extract the hashes, there must be a better way. So why don't ask a little help of the friend ChatGPT? So I did, and this is the result.

## Usage for extracting full sql downloads

Copy/move the zip-file in the same folders as the python script and extract the hashes by following the examples below.

### Examples

#### Extract MD5 and SHA1

python nsrlv3.py RDS_2023.03.1_ios.zip

#### Extract MD5 only

python nsrlv3_md5.py RDS_2023.03.1_ios.zip

#### Extract SHA1 only

python nsrlv3_sha1.py RDS_2023.03.1_ios.zip

## Usage for extracting delta sql downloads

Extract the file ending with _delta.sql to the same folder as the python script. Extract the hashes by following the examples below.

### Examples

#### Extract SHA1 to text and csv

python3 nsrlv3_delta_sha1.py RDS_2023.09.1_android_minimal_delta.sql

#### Extract MD5 to text and csv

python3 nsrlv3_delta_md5.py RDS_2023.09.1_android_minimal_delta.sql
