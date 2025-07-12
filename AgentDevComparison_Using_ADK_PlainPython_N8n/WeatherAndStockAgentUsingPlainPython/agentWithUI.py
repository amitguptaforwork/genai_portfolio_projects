from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
import gradio as gr
from gradio import ChatMessage
import time

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

#print("**********",os.getcwd())

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

history=[
    {"role": "system", "content": system_prompt}
]

def llm_response(message, history):
    print("********",(history))
    # if(len(history) ==0):
    #     history=[{"role": "system", "content": system_prompt}]
    history=[{"role": "system", "content": system_prompt}]   
    history.append({"role": "user", "content": message})
    response = ChatMessage(content="", metadata={"title": "_Thinking_ step-by-step", "id": 0, "status": "pending"})
    yield response

    accumulated_thoughts = ""
    start_time = time.time()

    while True:
        llm_response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=history)

        parsed_response = json.loads(llm_response.choices[0].message.content)
        print("________________________________")
        print(parsed_response)
        print("________________________________")

        step = parsed_response.get("step")
        if step == "plan":
            #print(f"🧠brain: {parsed_output['content']}")
            #{'step': 'plan', 'content': 'User is interested in weather data of Hyderabad.'}
            #{'step': 'plan', 'content': 'Fsrom the available tools, I should call get_weather'}
            history.append({"role": "assistant", "content": parsed_response['content']})
            thought = (parsed_response["step"], parsed_response["content"])  
            accumulated_thoughts += f"**{thought[0]}**: {thought[1]}\n"            
            response.content = accumulated_thoughts.strip()            
            yield response            
            continue
        if step == "action":
            #{'step': 'action', 'function': 'get_weather', 'input': 'Hyderabad'}
            history.append({"role": "assistant", "content": json.dumps(parsed_response)})            
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")
            
            if available_tools.get(tool_name, False)!= False:
                output = available_tools[tool_name].get("fn")(tool_input)
                history.append({"role": "assistant", "content": json.dumps({"step":"observe","output":output})})            
                thought = (parsed_response["step"], output)  
                accumulated_thoughts += f"**{thought[0]}**: {thought[1]}\n"            
                response.content = accumulated_thoughts.strip()            
                yield response            
                continue
        if step == "output":
            #print(f"🤖: {parsed_output['content']}")
			#We print how much time it took to get the final result
            response.metadata["status"] = "done"
            response.metadata["duration"] = time.time() - start_time
            yield response

            #And here is the final result
            thought = f"🤖Final Result: {parsed_response['content']}"
            response = [
			        response,
			        ChatMessage(
			            content=thought
			        )
			    ]
            
            yield response
            break
demo = gr.ChatInterface(
    llm_response,
    title="Chain of Thought based LLM Chat Agent 🤔- amitguptaforwork@gmail.com",
    type="messages",
    theme='amitguptaforwork/blue_professional',
    examples=["What is weather of Hyderabad", "What is stock price of NSE.NS", "Who is Obama"],
    
)

demo.launch()





