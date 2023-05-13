# python3 /Users/ruslan/Desktop/Web\ Projects/home-server/smartshuk/_Third-Party\ Data/cities/cbs.gov.il/add_regions_and_cities_to_db.py

import os
import sys
import django
import json

sys.path.append('/Users/ruslan/Desktop/Web Projects/home-server/smartshuk')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartshuk.settings')
django.setup()

from user_ads.models import City, Region

def create_regions_and_cities(regions_and_cities_data):
    from django.db import transaction

    with transaction.atomic():
        for data in regions_and_cities_data:
            region_name = data['region_name']
            city_name = data['city_name']

            region, _ = Region.objects.get_or_create(name=region_name)

            if city_name:
                City.objects.get_or_create(name=city_name, region=region)


def read_regions_and_cities_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    regions_and_cities_data = []

    for item in data:
        district = item.get('District')
        locality_name = item.get('Locality name')

        if district and locality_name and locality_name.strip():
            regions_and_cities_data.append({
                'region_name': district.strip(),
                'city_name': locality_name.strip(),
            })

    return regions_and_cities_data


if __name__ == "__main__":
    file_path = '/Users/ruslan/Desktop/Web Projects/home-server/smartshuk/_Third-Party Data/cities/cbs.gov.il/generated-output.json'
    regions_and_cities_data = read_regions_and_cities_from_json(file_path)

    create_regions_and_cities(regions_and_cities_data)
