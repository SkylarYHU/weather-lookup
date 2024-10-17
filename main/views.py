from django.shortcuts import render
import json
import urllib.request
from urllib.parse import quote


def index(request):
    data = {}  # Initialize data dictionary
    url = None  # Initialize url variable

    if request.method == "POST":
        city = request.POST['city']
        formatted_city = quote(city)
        url = f'https://api.openweathermap.org/data/2.5/weather?units=metric&q={
            formatted_city}&appid=dfcf9128c9382120e3d3e37a6f731405'

        try:
            # Fetch the data from OpenWeatherMap API
            response = urllib.request.urlopen(url)
            source = response.read().decode('utf-8')  # Decode bytes to string

            # Load the JSON data from the response string
            list_of_data = json.loads(source)

            # Prepare the data to pass to the template
            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + '°C',
                "pressure": str(list_of_data['main']['pressure']) + ' hPa',
                "humidity": str(list_of_data['main']['humidity']) + '%',
            }

        except Exception as e:
            # Handle exceptions (like if the city is not found)
            data = {"error": str(e)}

    # Render the template with the data
    return render(request, "main/index.html", data)
