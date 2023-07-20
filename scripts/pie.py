import requests
import dotenv
import os

dotenv.load_dotenv()

BASE_URI = "https://24hourcharts.p.rapidapi.com/v1/charts/png"

API_KEYS = [ # multiple so I'm not restricted to only 10 a day
    os.getenv("API_KEY_1"),
    os.getenv("API_KEY_2"),
    os.getenv("API_KEY_3"),
]

def request_chart(size: int, percent_open: float):
    chart_data = {
        "type": 'pie',
        "title": ' ', # f'Lifts: {int(percent_open * 100)}% Open',
        "showLegend": False,
        "datasets": [{ 'values': [f'{percent_open}', f'{1 - percent_open}'] }],
        "output": {
            "width": size,
            "height": size
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
            return response.content
        else:
            print(f'ERROR CODE: { response.status_code }')

            # if checked last api key
            if (i == len(API_KEYS) - 1):
                raise RuntimeError('No valid api keys')
            
if __name__ == '__main__':
    chart_img = request_chart(500, .82)
    with open('data/image.png', 'wb') as f:
        f.write(chart_img)