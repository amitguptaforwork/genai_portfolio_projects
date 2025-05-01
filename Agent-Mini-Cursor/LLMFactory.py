import askGemini  
import askOpenAI 
 


def getLLMClientAndModel(llm_name):
    if llm_name == "gemini":
        # Create an OpenAI client with the API key and base URL
        return askGemini.getGeminiClientAndModel()
    elif llm_name == "openai":
        # Create an OpenAI client with the API key and base URL
        return askOpenAI.getOpenAIClientAndModel()
    else:
        raise ValueError("Invalid LLM name. Currently, only 'gemini','openai' and 'ollama' are supported.")
    


def chatLLM(llm_name, system_prompt, query):
    llm_name = llm_name.lower()
    """
    This function takes a system prompt and a query and returns the response from the specified LLM.
    """
    if llm_name == "gemini":
        return askGemini(system_prompt, query)
    elif llm_name == "openai":
        return askOpenAI(system_prompt, query)
    else:
        raise ValueError("Invalid LLM name. Choose 'Gemini', 'OpenAI'.")

 

    
# result = askGemini("You are a helpful assistant.", "What is the capital of France?")
# print(result)

# result = askOpenAI("You are a helpful assistant.", "What is the capital of India?")
# print(result)


