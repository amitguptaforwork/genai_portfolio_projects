import os
import datetime
import requests
from dotenv import load_dotenv
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor

#Both these are old libraries, keeping to remind myself
#from langchain.chat_models import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import StructuredTool
from langchain.memory import ConversationBufferMemory


# Load environment variables
load_dotenv()

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# Create the LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o")


def get_stock_info(ticker: str) -> dict:
    """Get Current Information for a Single Ticker/ Stock

    Args:
        ticker (str): The symbol of the stock.

    Returns:
        dict: Stock Info or error msg.
    """
    import yfinance as yf

    #check if ticker provided is valid or not
    # Define the conversation messages:
    from langchain.schema import SystemMessage, HumanMessage
    messages = [
        SystemMessage(content="You are a helpful assistant. You are provided with a stock ticker and you need check if its a valid yfinance ticker. If yes, return the same ticker, if no then get the ticker symbol for the company.  Return only one value."),
        HumanMessage(content=ticker)
    ]

    # Send the messages to the LLM and get a response
    response = llm(messages)
    ticker = response.content


    try:        
        tickerInfo = yf.Ticker(ticker).info
        if not tickerInfo:
            return {"error":f"Could not retrieve stock data for {ticker}"}
        return tickerInfo
    except Exception as e:
        return {"error": f"Could not retrieve stock data for {ticker}"} 


# Define the weather tool
def get_weather(city):
    """Get the current weather for a given city."""
    try:
        url = f"https://wttr.in/{city}?format=%C%20%t"    
        response = requests.get(url)
        print("Tool Response", response.text)
        if response.status_code == 200:
            return f"The weather in {city} is {response.text}"
        else:
            return f"Could not retrieve weather data for {city}"
    except Exception as e:
        return f"Error getting weather: {str(e)}"

# Create structured tools
stock_tool = StructuredTool.from_function(
    func=get_stock_info,
    name="get_stock_info",
    description="Get Current Information for a Single Ticker/ Stock"
)

weather_tool = StructuredTool.from_function(
    func=get_weather,
    name="get_weather",
    description="Useful for getting the current weather in a specific location. Input should be a city name or location."
)

# Set up the tools list
tools = [stock_tool, weather_tool]

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that can tell the stock information for a given stock and check the weather.
    When a user asks about stocks, use the get_stock_info tool.  You can extract the stock ticker from their query.
    If the ticker is not clear, try to clarify with the user.
    When a user asks about the weather, use the get_weather tool, but you must extract the location from their query.
    If the location is not specified for weather queries, ask the user to provide a location.
    Always be friendly and concise in your responses."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)





# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    return_intermediate_steps=True
)

# Function to interact with the agent
def chat_with_agent(user_input):
    response = agent_executor.invoke({"input": user_input})
    return response["output"]

# Example usage
if __name__ == "__main__":
    print("Welcome to the Stock and Weather Assistant!")
    print("Ask me about the current time or weather in any location.")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        response = chat_with_agent(user_input)
        print(f"\nAssistant: {response}")