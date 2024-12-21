import os
import requests
from .models import Trip
import time
def load_env_file(filepath):
    with open(filepath) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value.strip().strip("'").strip('"')

# Load environment variables from .env file
load_env_file(os.path.join(os.path.dirname(__file__), '../../.env'))

def fetch_image_url_for_trip(place):
    time.sleep(1)
    api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    search_engine_id = os.getenv('SEARCH_ENGINE_ID')

    search_url = "https://www.googleapis.com/customsearch/v1"
    query = f"{place}"
    params = {
        "q": query,
        "cx": search_engine_id,
        "key": api_key,
        "searchType": "image",
        "num": 1,
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json()
        print("Fetch Image URL for Trip Response:", results)
        if "items" in results:
            return results["items"][0]["link"]
        return None
    except requests.exceptions.RequestException as e:
        print("Error fetching image URL for trip:", e)
        raise

def fetch_image_url(place_name, trip_id):
    time.sleep(1)
    api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    search_engine_id = os.getenv('SEARCH_ENGINE_ID')
    
    # Fetch the trip's place (city)
    try:
        trip = Trip.objects.get(id=trip_id)
        city = trip.place
    except Trip.DoesNotExist:
        city = ""

    search_url = "https://www.googleapis.com/customsearch/v1"
    query = f"{place_name} in {city}"
    params = {
        "q": query,
        "cx": search_engine_id,
        "key": api_key,
        "searchType": "image",
        "num": 1,
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    results = response.json()
    if "items" in results:
        return results["items"][0]["link"]
    return None