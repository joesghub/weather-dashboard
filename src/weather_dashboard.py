import os # Used for interacting with the operating system, such as accessing environment variables.
import json # Used for working with JSON data, including serializing and deserializing data.
import boto3 # AWS SDK for Python, used here to interact with S3.
import requests # Library for making HTTP requests to external APIs.
from datetime import datetime # Used to get and format timestamps.
from dotenv import load_dotenv # Loads environment variables from a .env file into the script.
import random  # Provides functions to generate random values, used to create a unique suffix for the bucket name.
import string  # Provides a sequence of characters, such as lowercase letters and digits, used for generating a random string.
import time  # Provides time-related functions, such as sleeping for a specific duration, used here to ensure the bucket is created before proceeding.


# Load environment variables
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        # __init__ method is a constructor in Python. It is automatically called when an instance (or object) of a class is created. 
        # Its primary purpose is to initialize the attributes (variables) of the class for that specific instance.

        # Dynamically generate a unique bucket name
        prefix = os.getenv('AWS_BUCKET_PREFIX', 'weather-dashboard')
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        #random.choices(population, k)
        # population: The sequence to choose from (string.ascii_lowercase + string.digits in this case).
        # string.ascii_lowercase: Provides all lowercase letters ('abcdefghijklmnopqrstuvwxyz').
        # string.digits: Provides all digits ('0123456789').
        # Combined, this creates 'abcdefghijklmnopqrstuvwxyz0123456789'.
        # k: Number of random elements to pick (6 in this case).
        # random.choices selects 6 random characters from 'abcdefghijklmnopqrstuvwxyz0123456789'.
        # ''.join(): converts the list of characters into a single string.

        self.bucket_name = f"{prefix}-{random_suffix}"
        print(f"Generated bucket name: {self.bucket_name}")

        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        # Expects the API key for the OpenWeather API to be set as an environment variable (OPENWEATHER_API_KEY) via the .env file or the system environment.
        self.s3_client = boto3.client('s3', region_name='us-west-1')
        # Creates an instance of the S3 client from the boto3 library. 
        # This client is used to interact with Amazon S3 (e.g., to create buckets or upload data).
        # "region_name='us-west-1'" ensures the S3 client is set to use us-west-1

    def create_bucket_if_not_exists(self):
    # """Create S3 bucket in us-west-1 if it doesn't exist."""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} already exists.")
            # Bucket Exists:
            # head_bucket() will succeed without returning anything, and the message "Bucket {self.bucket_name} already exists." is printed.
            # Bucket Doesn't Exist:
            # head_bucket() call will raise an exception (e.g., botocore.exceptions.ClientError), and the except block will execute, indicating the bucket needs to be created.

        except:
            print(f"Bucket {self.bucket_name} does not exist. Creating...")
            try:
                # Add a region-specific configuration for bucket creation in us-west-1
                self.s3_client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': 'us-west-1'
                    }
                )
                print(f"Successfully created bucket {self.bucket_name} in us-west-1.")

                # Sleep for a few seconds to ensure the bucket creation is complete
                time.sleep(10)  # Sleep for 10 seconds

            except Exception as e:
                print(f"Error creating bucket: {e}")

    def fetch_weather(self, city):
    # """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def save_to_s3(self, weather_data, city):
    # """Save weather data to S3 bucket"""
        if not weather_data:
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"
        
        try:
            weather_data['timestamp'] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved data for {city} to S3")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False

def main():
    dashboard = WeatherDashboard()
    # This line creates an instance of the WeatherDashboard class and assigns it to the variable dashboard.
    # The __init__ method of the WeatherDashboard class is executed, which:
    # Loads the API key (OPENWEATHER_API_KEY) and bucket name (AWS_BUCKET_NAME) from the .env file.
    # Initializes an S3 client using the boto3 library.

    # The dashboard instance is now ready to call methods like create_bucket_if_not_exists, fetch_weather, and save_to_s3 with the preloaded attributes (API key, bucket name, S3 client).
    
    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()
    
    cities = ["Philadelphia", "Seattle", "New York"]
    
    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            
            print(f"Temperature: {temp}°F")
            print(f"Feels like: {feels_like}°F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")
            
            # Save to S3
            success = dashboard.save_to_s3(weather_data, city)
            if success:
                print(f"Weather data for {city} saved to S3!")
        else:
            print(f"Failed to fetch weather data for {city}")

if __name__ == "__main__":
    main()
