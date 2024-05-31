from flask import Flask, request, render_template, jsonify, send_from_directory
import requests
from urllib.parse import unquote

app = Flask(__name__)

def get_aqi(city):
    base_url = "https://api.weatherbit.io/v2.0/forecast/daily"
    api_key = "21e152f862684d209d90a27afd293dfe"
    params = {"city": city, "key": api_key}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" in data and data["data"]:
            city = data["city_name"]
            weather_data = data["data"][0]
            date = weather_data.get("valid_date")
            temp = weather_data.get("temp")
            max_temp = weather_data.get("max_temp")
            min_temp = weather_data.get("min_temp")
            pop = weather_data.get("pop")
            snow = weather_data.get("snow")
            
            result = f"Weather forecast for {city} on {date}:<br>Temperature(°C): Average - {temp}, High - {max_temp}, Low - {min_temp}<br>Probability of rain: {pop}%<br>Accumulated snowfall: {snow}mm"
            return result

        else:
            return f"City not found: {city}"

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_aqi_by_coordinates(latitude, longitude):
    base_url = "https://api.weatherbit.io/v2.0/forecast/daily"
    api_key = "21e152f862684d209d90a27afd293dfe"
    params = {"lat": latitude, "lon": longitude, "key": api_key}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" in data and data["data"]:
            city = data["city_name"]
            weather_data = data["data"][0]
            date = weather_data.get("valid_date")
            temp = weather_data.get("temp")
            max_temp = weather_data.get("max_temp")
            min_temp = weather_data.get("min_temp")
            pop = weather_data.get("pop")
            snow = weather_data.get("snow")
            
            result = f"Weather forecast for {city} on {date}:<br>Temperature(°C): Average - {temp}, High - {max_temp}, Low - {min_temp}<br>Probability of rain: {pop}%<br>Accumulated snowfall: {snow}mm"
            return result
        
        else:
            return f"Invalid coordinates: ({latitude}, {longitude})"

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_aqi', methods=['GET'])
def api_get_aqi():
    city = request.args.get('city')
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')

    if city:
        result = get_aqi(city.lower())
    elif latitude and longitude:
        latitude = unquote(latitude)
        longitude = unquote(longitude)
        result = get_aqi_by_coordinates(latitude, longitude)
    else:
        result = "Invalid request. Provide either city or coordinates."

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)