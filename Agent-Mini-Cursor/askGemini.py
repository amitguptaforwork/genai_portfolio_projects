#I want to create a function that i can then expose from this file to be used in other files
#I will create a function that takes a query and returns the response from Gemini


from openai import OpenAI
from dotenv import load_dotenv
import os

LLM_MODEL="gemini-2.0-flash"

def getGeminiClientAndModel():
    """
    This function loads the environment variables and returns an OpenAI client.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the API key from environment variables
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Create an OpenAI client with the API key and base URL
    client = OpenAI(api_key=api_key,
             base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    return client,LLM_MODEL


def askGemini(system_prompt, query):
    """
    This function takes a system prompt and a query and returns the response from Gemini.
    """
    client = getGeminiClientAndModel()[0]
    
    # Prepare the messages for the chat completion
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": query})
    
    # Get the response from Gemini
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages
    )
    
    return response.choices[0].message.content  
 

