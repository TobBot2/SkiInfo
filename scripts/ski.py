import requests
import json
import datetime
import dotenv
import os

dotenv.load_dotenv()
session = requests.Session()

RESORTS_FILE = 'data/test.json'

RESORTS_URI = "https://ski-resorts-and-conditions.p.rapidapi.com/v1/resort/" # + resort name for resort info
RESORT_INFO_BASE_URI = "https://api.skiapi.com/v1/resort/" # + resort name for resort info
WEATHER_URI = "https://world-weather-online-api1.p.rapidapi.com/ski.ashx"

API_KEYS = [ # multiple so I get more calls per day
    os.getenv("API_KEY_1"),
    os.getenv("API_KEY_2"),
    os.getenv("API_KEY_3"),
]

def load_resorts_page(page_number: int = 1):
    page = None

    for i in range(len(API_KEYS)):
        headers = {
            "X-RapidAPI-Key": API_KEYS[i],
            "X-RapidAPI-Host": "ski-resorts-and-conditions.p.rapidapi.com"
        }

        response = session.get(RESORTS_URI,  params={'page': page_number}, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'ERROR CODE: { response.status_code }')

            # if checked last api key
            if (i == len(API_KEYS) - 1):
                raise RuntimeError("No valid api keys")


def get_resorts_pages():
    first_page = load_resorts_page()

    yield first_page
    
    num_pages = first_page['total_pages']

    for page_number in range(2, num_pages + 1):
        next_page = load_resorts_page(page_number)
        yield next_page

def request_list_of_resorts() -> list:
    resorts_list = []
    for page in get_resorts_pages():
        resorts_list.extend(page['data'])

    return resorts_list

def write_resorts_list_to_json():
    resorts_with_timestamp = {
        "time": datetime.datetime.now().isoformat(),
        "resorts": request_list_of_resorts()
    }
    with open(RESORTS_FILE, "w") as f:
        json.dumps(resorts_with_timestamp, f)

def check_if_resorts_list_needs_refresh():
    with open(RESORTS_FILE, "r") as f:
        pass

def request_resort_info(resort: str):
    for i in range(len(API_KEYS)):
        headers = {
            "X-RapidAPI-Key": API_KEYS[i],
            "X-RapidAPI-Host": "ski-resorts-and-conditions.p.rapidapi.com"
        }

        response = session.get(RESORT_INFO_BASE_URI + resort, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'ERROR CODE: { response.status_code }')

            # if checked last api key
            if (i == len(API_KEYS) - 1):
                raise RuntimeError("No valid api keys")
            
def request_weather(lat: int, lon: int):
    params = {"q":f'{lat},{lon}',"num_of_days":"1","lang":"en"}
    for i in range(len(API_KEYS)):
        headers = {
            "X-RapidAPI-Key": API_KEYS[i],
            "X-RapidAPI-Host": "world-weather-online-api1.p.rapidapi.com"
        }

        response = session.get(WEATHER_URI,  params=params, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'ERROR CODE: { response.status_code }')

            # if checked last api key
            if (i == len(API_KEYS) - 1):
                raise RuntimeError("No valid api keys")

def request_resort_all(resort: str):
    info_json = request_resort_info(resort)

    lat = info_json["data"]["location"]["latitude"],
    lon = info_json["data"]["location"]["longitude"],

    temp_json = request_weather(lat, lon)

    return {
        "lat":lat,
        "lon":lon,
        "snowfall_48hrs": info_json["data"]["conditions"]["fourtyeight_hours"],
        "snowfall_season": info_json["data"]["conditions"]["season_hours"],
        "lifts_percent": info_json["data"]["lifts"]["stats"]["percentage"]["open"],
        "temp_base_min": temp_json["data"]["weather"][0]["bottom"]["mintempF"],
        "temp_base_max": temp_json["data"]["weather"][0]["bottom"]["maxtempF"],
        "temp_peak_min": temp_json["data"]["weather"][0]["top"]["mintempF"],
        "temp_peak_max": temp_json["data"]["weather"][0]["top"]["maxtempF"],
    }

if __name__ == "__main__":
    write_resorts_list_to_json()
    print("Done.")