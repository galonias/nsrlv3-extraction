# Extract NSRL hashes

Please note that this script is entirely written by ChatGPT and should be used with caution.

## About

Since the official method is time consuming and requires a lot of manual labor and intervention to extract the hashes, there must be a better way. So why don't ask a little help of the friend ChatGPT? So I did, and this is the result.

## Usage for extracting full sql downloads

python nsrlv3.py dbname.zip

### Examples

#### Extract MD5 and SHA1 from 

python nsrlv3.py RDS_2023.03.1_ios.zip

#### Extract MD5 only

python nsrlv3_md5.py RDS_2023.03.1_ios.zip

#### Extract SHA1 only

python nsrlv3_sha1.py RDS_2023.03.1_ios.zip

