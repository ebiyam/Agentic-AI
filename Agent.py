import requests
import string

# ----------------- Configuration -----------------
# Directly set your OpenWeatherMap API key here
WEATHER_API_KEY = "2b87d1593057691bf16f52aa4e5a847b"

# ----------------- Functions -----------------
def get_weather(location: str) -> dict:
    """Fetch real weather data from OpenWeatherMap."""
    if not WEATHER_API_KEY:
        raise ValueError("Please set your WEATHER_API_KEY!")

    print(f"Agent: Fetching weather data for {location}...")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Agent: Could not fetch data. Using default placeholder.")
        return {"main": {"temp": None}, "weather": [{"description": "unknown"}]}
    
    return response.json()


def interpret_weather(weather_json: dict) -> str:
    """Interpret weather data and give clothing suggestion."""
    temp = weather_json.get("main", {}).get("temp")
    desc = weather_json.get("weather", [{}])[0].get("description", "unknown")
    
    if temp is None:
        return "Agent: Could not fetch weather data."
    
    suggestion = "Agent: Here's what to wear: "
    if temp > 30:
        suggestion += "Hot! Wear light clothes."
    elif temp < 15:
        suggestion += "Cold! Wear a jacket."
    else:
        suggestion += "Moderate weather — normal clothes."
    
    suggestion += f" (Current: {temp}°C, {desc})"
    return suggestion


def agent(prompt: str) -> str:
    """Simple agent: extracts location and gives weather advice."""
    print(f"\nAgent: Received your prompt -> '{prompt}'")
    
    # Extract location: last word of prompt
    location = prompt.strip().split()[-1]
    
    # Clean punctuation
    location = location.strip(string.punctuation)
    
    print(f"Agent: I think the location is '{location}'")
    
    # Fetch weather
    weather = get_weather(location)
    
    # Process and interpret
    suggestion = interpret_weather(weather)
    print("Agent: Processing complete.\n")
    return suggestion


# ----------------- Main -----------------
if __name__ == "__main__":
    print("Welcome to the Weather Advisor Agent!")

    while True:
        user_prompt = input("\nEnter your question (or type 'exit' to quit): ")
        if user_prompt.lower() in ["exit", "quit"]:
            print("Agent: Goodbye! Stay safe and dress appropriately! 😄")
            break
        
        try:
            response = agent(user_prompt)
            print(response)
        except Exception as e:
            print(f"Agent: Error -> {e}")
