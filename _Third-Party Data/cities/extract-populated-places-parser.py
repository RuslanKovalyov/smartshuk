import json

# Set up the path to the GeoNames file
# Replace with the actual path to your file
file_path = '/Users/ruslankovalev/Desktop/Web Projects/home-server/smartshuk/_Third-Party Data/cities/IL.txt'

print('path: ', file_path)
# Open the file and extract the list of populated places
with open(file_path, "r", encoding="utf-8") as file:
    populated_places = []
    for line in file:
        fields = line.split("\t")
        name = fields[1]
        feature_code = fields[7]


        if feature_code in ("PPL", "PPLA", "PPLA2", "PPLA3", "PPLA4", "PPLC", "PPLF", "PPLG", "PPLL", "PPLQ", "PPLR", "PPLS", "STLMT", "LCTY"):
            populated_places.append(name)

            # if "Tel Aviv" in name:
            #         print("Debug line: ", line)
            #         print(name)

# Print the list of populated places
for place in populated_places:
    print(place)
print(len(populated_places))


# Set up the path to the output file
# Replace with the actual path to your file
output_file_path = '/Users/ruslankovalev/Desktop/Web Projects/home-server/smartshuk/_Third-Party Data/cities/generated-output.txt'

# Write the list of place names to the output file
with open(output_file_path, 'w') as file:
    for place in populated_places:
        file.write(place + '\n')

    
