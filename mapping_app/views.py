import requests
from django.http import JsonResponse
from django.core.cache import cache
from datetime import datetime, timedelta
from django.http import HttpResponse


from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import cache_page

def geocode_proxy(request):
    query = request.GET.get('query', '')
    cache_key = f'geocode_{query}'

    # Get the last request timestamp from the cache
    last_request_timestamp_key = f'last_request_timestamp'
    last_request_timestamp = cache.get(last_request_timestamp_key)

    # Check if the last request was more than one second ago
    if last_request_timestamp and (datetime.now() - last_request_timestamp) < timedelta(seconds=1):
        return HttpResponse(status=429)  # Too Many Requests

    # Store the current request timestamp in the cache
    cache.set(last_request_timestamp_key, datetime.now())

    # Check if the result is already cached
    cached_result = cache.get(cache_key)
    if cached_result:
        # print(f"\n\nReturning cached result for key {cache_key}\n\n")
        return JsonResponse(cached_result, safe=False)

    # If not, make a request to Nominatim
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': query,
        'format': 'json',
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Add this line to log the response from Nominatim
    # print(f"\n\nNominatim response: {data}\n\n")

    # Cache the result for a certain period
    cache.set(cache_key, data, settings.CACHE_TTL_LEAFLET_MAP)

    return JsonResponse(data, safe=False)

    
def map_popup(request):
    city = request.GET.get('city', u'')
    address = request.GET.get('address', u'')

    if city and address:
        full_address = f"{address}, {city}"
    else:
        full_address = ''

    # Create a custom cache key based on city and address
    cache_key = f"map_popup_{full_address}"
    cached_response = cache.get(cache_key)

    if cached_response:
        return cached_response

    context = {
        'address': full_address,
    }

    response = render(request, 'mapping_app/map_popup.html', context)

    # Cache the response for a certain period (e.g. 10 day)
    cache.set(cache_key, response, settings.CACHE_TTL_LEAFLET_MAP)

    return response
