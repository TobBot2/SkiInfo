import requests
import json
import datetime
import dotenv
import os

dotenv.load_dotenv()
session = requests.Session()

RESORTS_FILE = 'data/test.json'

# base_uri: just add the 'slug' value to the end of the string for a specific resort. resort_info_base_uri might work too though even without an api key...
#           Or use as-is to get a list of the resorts (paginate through)
BASE_URI = "https://ski-resorts-and-conditions.p.rapidapi.com/v1/resort/"
RESORT_INFO_BASE_URI = "https://api.skiapi.com/v1/resort/"

API_KEYS = [ # multiple so I'm not restricted to only 10 a day
    os.getenv("API_KEY_1"),
    os.getenv("API_KEY_2"),
    os.getenv("API_KEY_3"),
]

def basic_api_request():
    headers = {
        "X-RapidAPI-Key": API_KEYS[0],
        "X-RapidAPI-Host": "ski-resorts-and-conditions.p.rapidapi.com"
    }

    print(session.get(BASE_URI, headers=headers))

def load_resorts_page(page_number: int = 1):
    page = None

    for i in range(len(API_KEYS)):
        headers = {
            "X-RapidAPI-Key": API_KEYS[i],
            "X-RapidAPI-Host": "ski-resorts-and-conditions.p.rapidapi.com"
        }

        response = session.get(BASE_URI,  params={'page': page_number}, headers=headers)

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

if __name__ == "__main__":
    write_resorts_list_to_json()
    print("Done.")