import streamlit as st
import requests
import csv
import pandas as pd

api_key = "84db8030d18aa6b48a0f1959501aaf69"

st.set_page_config(layout="wide")
st.title("Weather App")

# Create sidebar
st.sidebar.title("Menu")
menu_selection = st.sidebar.selectbox("Select an option", ["City Weather", "Temperature Conversion", "Weather Forecast", "Weather Comparison", "History"], index=0, key="menu_selection")

if menu_selection == "City Weather":
    # Collect user details
    name = st.text_input("Enter your name:", key="name_input")
    mobile_number = st.text_input("Enter your mobile number:", key="mobile_input")
    email = st.text_input("Enter your email:", key="email_input")
    current_city = st.text_input("Enter your current city:", key="city_input", autocomplete="on")

    # Save user details to a CSV file if conditions are met
    if len(name) > 0 and len(mobile_number) > 0 and len(email) > 0 and len(current_city) > 0 and len(mobile_number) == 10 and email.endswith("@gmail.com"):
        with open("user_details.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, mobile_number, email, current_city])

    current_location = st.checkbox("Use current location")
    if current_location:
        # Get user's current location using a geolocation API
        # Code for getting current location goes here
        current_city = "Surat"
    if st.button("Get Weather"):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={current_city}&appid={api_key}"
        
        response = requests.get(url)
        
        data = response.json()

        if data["cod"] == "404":
            st.error("City not found.")
        else:
            weather = data["weather"][0]["main"]
            temperature = data["main"]["temp"] - 273.15  # Convert temperature to Celsius
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            st.subheader(f"Weather in {current_city}:")
            st.write(f" - Condition: {weather}")
            st.write(f" - Temperature: {temperature} °C")  # Display temperature in Celsius
            st.write(f" - Humidity: {humidity}%")
            st.write(f" - Wind Speed: {wind_speed} m/s")

            # Display weather condition image/icon
            if weather == "Clear":
                st.image("ritam-baishya-ROVBDer29PQ-unsplash.jpg", caption="Clear Sky")
            elif weather == "Clouds":
                st.image("jose-g-ortega-castro-tS4Pl_8F3fY-unsplash.jpg", caption="Cloudy Weather")
            elif weather == "Rain":
                st.image("kirill-HU_iSmQqpK4-unsplash.jpg", caption="Rainy Weather")
            elif weather == "Snow":
                st.image("ritam-baishya-ROVBDer29PQ-unsplash.jpg", caption="Snowy Weather")
            elif weather == "Thunderstorm":
                st.image("tasos-mansour-_hGPdpyMV-8-unsplash.jpg.jpg", caption="Thunderstorm")
            elif weather == "Mist":
                st.image("ritam-baishya-ROVBDer29PQ-unsplash.jpg", caption="Misty Weather")
            elif weather == "Smoke":
                st.image("corey-agopian-XGOzlCNeP1I-unsplash.jpg", caption="Smoky Weather")
            

            map_link = f"https://www.google.com/maps/place/{current_city}"
            st.markdown(f"Map Link: [{current_city}]({map_link})")

elif menu_selection == "Temperature Conversion":
    temperature_unit_from = st.selectbox("Select temperature unit to convert from", ["Celsius", "Fahrenheit", "Kelvin"], index=0, key="temperature_unit_from")
    temperature_unit_to = st.selectbox("Select temperature unit to convert to", ["Celsius", "Fahrenheit", "Kelvin"], index=1, key="temperature_unit_to")
    temperature = st.number_input(f"Enter {temperature_unit_from} temperature:", key="temperature_input")
    
    if st.button("Convert"):
        if temperature_unit_from == "Celsius":
            if temperature_unit_to == "Celsius":
                converted_temperature = temperature
            elif temperature_unit_to == "Fahrenheit":
                converted_temperature = (temperature * 9/5) + 32
            elif temperature_unit_to == "Kelvin":
                converted_temperature = temperature + 273.15
        elif temperature_unit_from == "Fahrenheit":
            if temperature_unit_to == "Celsius":
                converted_temperature = (temperature - 32) * 5/9
            elif temperature_unit_to == "Fahrenheit":
                converted_temperature = temperature
            elif temperature_unit_to == "Kelvin":
                converted_temperature = (temperature + 459.67) * 5/9
        elif temperature_unit_from == "Kelvin":
            if temperature_unit_to == "Celsius":
                converted_temperature = temperature - 273.15
            elif temperature_unit_to == "Fahrenheit":
                converted_temperature = (temperature * 9/5) - 459.67
            elif temperature_unit_to == "Kelvin":
                converted_temperature = temperature
        
        st.write(f"Converted temperature: {converted_temperature} {temperature_unit_to}")

elif menu_selection == "Weather Forecast":
    current_city = st.text_input("Enter a city:", key="forecast_city_input", autocomplete="on")
    if st.button("Get Forecast"):
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={current_city}&appid={api_key}"
        
        response = requests.get(url)
        
        data = response.json()

        if data["cod"] == "404":
            st.error("City not found.")
        else:
            forecast_list = data["list"]
            st.subheader(f"Weather Forecast for {current_city}:")
            for forecast in forecast_list:
                date_time = forecast["dt_txt"]
                weather = forecast["weather"][0]["main"]
                temperature = forecast["main"]["temp"] - 273.15  # Convert temperature to Celsius
                humidity = forecast["main"]["humidity"]
                wind_speed = forecast["wind"]["speed"]

                st.write(f" - Date/Time: {date_time}")
                st.write(f" - Condition: {weather}")
                st.write(f" - Temperature: {temperature} °C")  # Display temperature in Celsius
                st.write(f" - Humidity: {humidity}%")
                st.write(f" - Wind Speed: {wind_speed} m/s")
                st.write("---")

elif menu_selection == "Weather Comparison":
    city1 = st.text_input("Enter city 1:", key="city1_input")
    city2 = st.text_input("Enter city 2:", key="city2_input")
    city_list = [city1, city2]
    
    if st.button("Compare"):
        for city in city_list:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            
            response = requests.get(url)
            
            data = response.json()

            if data["cod"] == "404":
                st.error(f"Weather data not found for {city}.")
            else:
                weather = data["weather"][0]["main"]
                temperature = data["main"]["temp"] - 273.15  # Convert temperature to Celsius
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]

                st.subheader(f"Weather in {city}:")
                st.write(f" - Condition: {weather}")
                st.write(f" - Temperature: {temperature} °C")  # Display temperature in Celsius
                st.write(f" - Humidity: {humidity}%")
                st.write(f" - Wind Speed: {wind_speed} m/s")
                st.write("---")

elif menu_selection == "History":
    st.write(pd.read_csv("user_details.csv"))
