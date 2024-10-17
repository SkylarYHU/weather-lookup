from django.shortcuts import render

# Create your views here.
import json
import urllib.request
from urllib.parse import quote
import os


def index(request):
    if request.method == "POST":
        city = request.POST['city']

        formatted_city = quote(city)
        api_key = os.getenv('API_KEY')  # 从环境变量获取 API 密钥
        url = f'https://api.openweathermap.org/data/2.5/weather?units=metric&q={
            formatted_city}&appid={api_key}'

        try:
            response = urllib.request.urlopen(url)
            source = response.read().decode('utf-8')

            list_of_data = json.loads(source)

            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + '°C',
                "pressure": str(list_of_data['main']['pressure']) + ' hPa',
                "humidity": str(list_of_data['main']['humidity']) + '%',
            }

        except Exception as e:
            data = {"error": str(e)}

    else:
        data = {}

    return render(request, "main/index.html", data)
