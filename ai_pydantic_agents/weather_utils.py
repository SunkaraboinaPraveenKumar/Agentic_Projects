import os
import requests
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from dotenv import load_dotenv

load_dotenv()

class WeatherForeCast(BaseModel):
    location: str
    description: str
    temperature_celsius: float

weather_agent = Agent(
    model="groq:llama-3.3-70b-versatile",
    model_settings=ModelSettings(temperature=0.2),
    output_type=str,
    system_prompt="You are a helpful weather assistant. Use the 'get_weather_forecast' tool to find the weather forecast for a given city. Provide clean and friendly answers."
)

@weather_agent.tool
def get_weather_forecast(ctx: RunContext, city: str) -> WeatherForeCast:
    """
    Returns current weather forecast for a given city using OpenWeatherMap API.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = os.getenv('WEATHER_API_KEY')
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params).json()
    return WeatherForeCast(
        location=response["name"],
        description=response["weather"][0]["description"].capitalize(),
        temperature_celsius=response["main"]["temp"]
    )

def get_weather_response(question: str) -> str:
    result = weather_agent.run_sync(question)
    return result.output