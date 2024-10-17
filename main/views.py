import os
import json
import urllib.request
from urllib.parse import quote
from django.shortcuts import render


def index(request):
    if request.method == "POST":
        city = request.POST['city']
        formatted_city = quote(city)

        # 从环境变量获取 API 密钥
        api_key = os.environ.get("OPENWEATHER_API_KEY")

        # 确保 API 密钥存在
        if not api_key:
            return render(request, "main/index.html", {"error": "API key is not set."})

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
