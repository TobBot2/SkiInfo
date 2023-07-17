import requests
import json

session = requests.Session()

# base_uri: just add the 'slug' value to the end of the string for a specific resort. resort_info_base_uri might work too though even without an api key...
#           Or use as-is to get a list of the resorts (paginate through)
base_uri = "https://ski-resorts-and-conditions.p.rapidapi.com/v1/resort/"
resort_info_base_uri = "https://api.skiapi.com/v1/resort/"

api_keys = [ # multiple so I'm not restricted to only 10 a day
    "3f2e941106mshfc26bbce9cabcffp1db775jsn5c04bed9bd06", # trevoroblack
    "4bef95cc94msh2959b33cc4c7c8cp144964jsnd795651f317b", # devtrevblack
    "a971033fa4msh39eb626c1cee60bp195de6jsn12e7accb2b2f"  # pythonbot
]

accepted_api_errors = [
    'You have exceeded the DAILY quota for Requests on your current plan, BASIC. Upgrade your plan at https://rapidapi.com/random-shapes-random-shapes-default/api/ski-resorts-and-conditions',
    'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.',
    'Too many requests'
]

def basic_api_request():
    headers = {
        "X-RapidAPI-Key": "3f2e941106mshfc26bbce9cabcffp1db775jsn5c04bed9bd06",
        "X-RapidAPI-Host": "ski-resorts-and-conditions.p.rapidapi.com"
    }

    print(session.get(base_uri, headers=headers))

def load_resorts_page(page_number: int = 1):
    page = None

    for i in range(len(api_keys)):
        headers = {
            "X-RapidAPI-Key": api_keys[i],
            "X-RapidAPI-Host": "ski-resorts-and-conditions.p.rapidapi.com"
        }

        page = session.get(base_uri,  params={'page': page_number}, headers=headers).json()

        # message key in received json signifies an error
        if 'message' in page:
            if (page['message'] not in accepted_api_errors):
                print("New error message found...")
                print(page['message'])

            # if checked last api key
            if (i == len(api_keys) - 1):
                raise RuntimeError("No valid api keys")
        else:
            return page


def get_resorts_pages():
    first_page = load_resorts_page()

    yield first_page
    
    num_pages = first_page['total_pages']

    for page_number in range(2, num_pages + 1):
        next_page = load_resorts_page(page_number)
        yield next_page

def request_list_of_resorts():
    resorts_list = []
    for page in get_resorts_pages():
        resorts_list.extend(page['data'])

    return resorts_list

def write_resorts_list_to_json(file_path: str):
    with open(file_path, "w") as f:
        json.dumps(request_list_of_resorts(), f)


if __name__ == "__main__":
    write_resorts_list_to_json("../data/test.json")
    print("Done.")