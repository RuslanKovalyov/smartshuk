# python3 /Users/ruslan/Desktop/Web\ Projects/home-server/smartshuk/_Third-Party\ Data/cities/cbs.gov.il/data-parser-xlsx-to-json.py

# pip install openpyxl
# pip install pandas
import os
import pandas as pd
import json

# Get the path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set up the paths to the input and output files relative to the script directory
input_file_path = os.path.join(script_dir, "cbs.gov.il-he.xlsx")
output_file_path = os.path.join(script_dir, "generated-output.json")

# Load the data from the input file into a Pandas DataFrame
df = pd.read_excel(input_file_path, header=11, usecols="A:G")

# Extract the relevant columns and store them as a list of dictionaries
data = []
for row in df.itertuples():
    record = {
        "Locality Code": row[1],
        "Locality name": row[2],
        "District": row[3],
        "Sub-district": row[4],
        "Type of locality": row[5],
        "Municipal status": row[6],
        "Natural region": row[7]
    }
    data.append(record)

# Write the data to the output file in JSON format
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
