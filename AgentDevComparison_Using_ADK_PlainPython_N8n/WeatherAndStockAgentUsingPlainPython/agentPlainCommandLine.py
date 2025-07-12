from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY") 
# client = OpenAI(api_key=api_key)
client = OpenAI()

def get_weather(city):
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

 

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Get the weather of a city",
        "params": {
            "city": {
                "type": "string",
                "description": "City name to get the weather for"
            }
        }
    },
    "get_stock_info": {
        "fn": get_stock_info,
        "description": "Get Current Information for a Single Ticker/ Stock",
        "params": {
            "ticker": {
                "type": "string",
                "description": "The symbol of the stock."
            }
        }
    }
}

#Lets give hand and feet to our agent
system_prompt = """
You are a helpful AI assistant who is expert in resolving user queries
You work on start, plan, action, observe mode.
For the given user query and available tools, plan the step by step execution.

Based on the planning, select the relevant tool from the available tools 
And based on the selected tool, perform the action to call the tool

Based on the observation of the tool output, provide the final output to the user.

Rules:
- Follow the output json format
- Always perform one step at a time and wait for next input
- Carefully analyse the user query

Output JSON format:
{{"step":"string",
  "content":"string",
  "function":"The name of the function if step is an action",
  "input":"The input parameter for the function"
}}

Available tools:
- get_weather: Get the weather of a city
- get_stock_info: Get Current Information for a Single Ticker/ Stock


Example:
User Query: What is the weather of New York?
Output: {{ "step": "plan", "content": "User is interested in weather data of New York." }}
Output: {{ "step": "plan", "content": "From the available tools, I should call get_weather" }}
Output: {{ "step": "action", "function": "get_weather", "input":"New York." }}
Output: {{ "step": "observe", "output":"12 degree celcius" }}
Output: {{ "step": "output", "content":"The weather of New York seems to be 12 degree celcius" }}

"""

messages=[
    {"role": "system", "content": system_prompt}
]

while True:
    query= input("> ")
    messages.append({"role": "user", "content": query})
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        #print("Parsed Output", parsed_output)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})
        step = parsed_output.get("step")
        if step == "plan":
            print(f"🧠brain: {parsed_output['content']}")
            continue
        if step == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")
            if available_tools.get(tool_name, False)!= False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step":"observe","output":output})})
        if step == "output":
            print(f"🤖: {parsed_output['content']}")
            break        


