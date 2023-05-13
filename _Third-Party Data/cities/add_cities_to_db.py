#  python3 /Users/ruslan/Desktop/Web\ Projects/home-server/smartshuk/_Third-Party\ Data/cities/add_cities_to_db.py

import os
import sys
import django

sys.path.append(
    '/Users/ruslan/Desktop/Web Projects/home-server/smartshuk')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartshuk.settings')
django.setup()

from user_ads.models import City, Region

def create_cities(city_data):
    from django.db import transaction

    cities_to_create = [
        City(name=data['name'], region=data['region']) for data in city_data]

    with transaction.atomic():
        City.objects.bulk_create(cities_to_create)


def read_cities_from_file(file_path):
    with open(file_path, 'r') as file:
        cities = [city.strip() for city in file.readlines()]
    return cities


if __name__ == "__main__":
    region_name_to_instance = {
        region.name: region for region in Region.objects.all()}

    # city_data = [
    #     {'name': 'City 1', 'region': region_name_to_instance['IL']},
    #     {'name': 'City 2', 'region': region_name_to_instance['IL']},
    #     # ...
    # ]

    file_path = '/Users/ruslan/Desktop/Web Projects/home-server/smartshuk/_Third-Party Data/cities/generated-output.txt'
    city_names = read_cities_from_file(file_path)
    city_data = [{'name': city, 'region': region_name_to_instance['IL']}
                 for city in city_names]  # Replace 'Region 1' with the desired region name

    create_cities(city_data)
