#Time taken to write this code- 20-30 minutes

from google.adk.agents import Agent
import requests

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    url = f"https://wttr.in/{city}?format=%C%20%t"    
    response = requests.get(url)
    print("Tool Response", response.text)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    else:
        return f"Could not retrieve weather data for {city}"


def get_stock_info(ticker: str) -> dict:
    """Get Current Information for a Single Ticker/ Stock

    Args:
        ticker (str): The symbol of the stock.

    Returns:
        dict: Stock Info or error msg.
    """
    import yfinance as yf
    try:        
        tickerInfo = yf.Ticker(ticker).info
        if not tickerInfo:
            return {"error":f"Could not retrieve stock data for {ticker}"}
        return tickerInfo
    except Exception as e:
        return {"error": f"Could not retrieve stock data for {ticker}"}


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the weather in a city and stock information."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the  weather in a city and stock information. "
    ),
    tools=[get_weather, get_stock_info],
)

print(get_stock_info("BEL.aNS"))