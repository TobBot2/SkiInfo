import requests
import os
import dotenv

dotenv.load_dotenv()

BASE_URI = "https://maptoolkit.p.rapidapi.com/staticmap"

API_KEYS = [ # multiple so I'm not restricted to only 10 a day
    os.getenv("API_KEY_1"),
    os.getenv("API_KEY_2"),
    os.getenv("API_KEY_3"),
]

def request_map_image(latitude: int, longitude: int, img_width: int, img_height: int):
    #set parameters
    params = {
        "center":f'{latitude},{longitude}',
        "zoom":'3',
        "size":f'{img_width}x{img_height}',
        "maptype":'toursprung-terrainwinter',
        "format":'png',
        "marker":'center:-90,0|shadow:true' # hide marker
    }

    # request
    for i in range(len(API_KEYS)):
        headers = {
            "X-RapidAPI-Key": API_KEYS[0],
            "X-RapidAPI-Host": 'maptoolkit.p.rapidapi.com'
        }

        response = requests.get(BASE_URI,  params=params, headers=headers)

        if response.status_code == 200:
            return response.content
        else:
            print(f'ERROR CODE: { response.status_code }')

            # if checked last api key
            if (i == len(API_KEYS) - 1):
                raise RuntimeError('No valid api keys')

    return response.content
        
if __name__ == '__main__':
    lat = 50.10693
    lon = -122.922073

    map_img = request_map_image(lat, lon, 480, 480)
    with open('data/image.png', 'wb') as f:
        f.write(map_img)

