# python3 /Users/ruslan/Desktop/Web\ Projects/home-server/smartshuk/_Third-Party\ Data/cities/cbs.gov.il/data-parser-xlsx-to-text.py
# pip install openpyxl
# pip install pandas
import os
import pandas as pd

# Get the path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set up the paths to the input and output files relative to the script directory
input_file_path = os.path.join(script_dir, "cbs.gov.il-en.xlsx")
output_file_path = os.path.join(script_dir, "generated-output.txt")

# Load the data from the input file into a Pandas DataFrame
df = pd.read_excel(input_file_path, header=None, skiprows=12, usecols=[1])

# Extract the names of the localities and write them to the output file
with open(output_file_path, "w", encoding="utf-8") as f:
    for name in df[1]:
        f.write(name + "\n")
