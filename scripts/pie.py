from PIL import Image
import requests
import dotenv
import os

dotenv.load_dotenv()

BASE_URI = "https://24hourcharts.p.rapidapi.com/v1/charts/png"

CHART_SIZE = (500, 500)

API_KEYS = [ # multiple so I'm not restricted to only 10 a day
    os.getenv("API_KEY_1"),
    os.getenv("API_KEY_2"),
    os.getenv("API_KEY_3"),
]

def request_chart(percent_open: float, file: str):
    chart_data = {
        "type": 'pie',
        "title": ' ', # f'Lifts: {int(percent_open * 100)}% Open',
        "showLegend": False,
        "datasets": [{ 'values': [f'{percent_open}', f'{1 - percent_open}'] }],
        "output": {
            "width": CHART_SIZE[0],
            "height": CHART_SIZE[1]
        }
    }

    for i in range(len(API_KEYS)):
        headers = {
            "content-type": 'application/json',
            "X-RapidAPI-Key": API_KEYS[i],
            "X-RapidAPI-Host": '24hourcharts.p.rapidapi.com'
        }

        response = requests.post(BASE_URI, json=chart_data, headers=headers)

        if response.status_code == 200:
            with open(file_location, 'wb') as f:
                f.write(response.content)
                return
        else:
            print(f'ERROR CODE: { response.status_code }')

            # if checked last api key
            if (i == len(API_KEYS) - 1):
                raise RuntimeError('No valid api keys')

def format_chart(size: tuple[int, int], file_location):
    pil_image = Image.open(file_location)

    # icky hard coding, but necessary cuz the formatting of the returned image is weird
    trim_sides = 80
    pil_image = pil_image.crop((trim_sides, 120, CHART_SIZE[0]-trim_sides, CHART_SIZE[1]-40))

    # make transparent
    pil_image = pil_image.convert("RGBA")
    datas = pil_image.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    pil_image.putdata(newData)

    pil_image = pil_image.resize((size))
    pil_image.save(file_location, bitmap_format='png')

if __name__ == '__main__':
    file_location = 'data/image.png'
    request_chart(.32, file_location)
    format_chart((130, 130), file_location)