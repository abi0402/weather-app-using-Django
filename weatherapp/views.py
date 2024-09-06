from django.shortcuts import render
import requests
import datetime
from django.contrib import messages

def home(request):
    # Get the city from POST request or use 'indore' as default
    city = request.POST.get('city', 'indore')

    # OpenWeatherMap API setup
    api_key = 'fa21d315616fc08fb22679462d4cc30f'
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    # Google Custom Search API setup
    API_KEY = 'AIzaSyAtAGtEmQtpuxiJSoLBAJinPWUI9Vq_oo0'
    SEARCH_ENGINE_ID = 'c45d6bc5a4ddd4cdd'
    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    try:
        # Make the HTTP request to the OpenWeatherMap API
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()  # Check for HTTP request errors
        weather_data = weather_response.json()

        # Extract weather information
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        # Make the HTTP request to Google Custom Search API
        image_response = requests.get(city_url)
        image_response.raise_for_status()  # Check for HTTP request errors
        image_data = image_response.json()

        search_items = image_data.get("items")
        image_url = search_items[1]['link'] if search_items else None

        # Render the response with the weather data
        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except requests.exceptions.RequestException as e:
        # Handle any HTTP request errors (like connection errors)
        messages.error(request, 'Error fetching data. Please try again.')
        print(f"Error fetching data: {e}")

    except KeyError as e:
        # Handle case where expected data is not present in the API response
        messages.error(request, 'City not found or API response error.')
        print(f"KeyError in response: {e}")

    # Fallback data if an error occurs
    exception_occurred = True
    day = datetime.date.today()
    return render(request, 'weatherapp/index.html', {
        'description': 'clear sky',
        'icon': '01d',
        'temp': 25,
        'day': day,
        'city': 'indore',
        'exception_occurred': exception_occurred,
        'image_url': 'https://example.com/default-image.jpg'  # Provide a default background image URL
    })
