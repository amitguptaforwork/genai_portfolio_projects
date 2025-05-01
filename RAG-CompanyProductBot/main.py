from LLM_Calling import LLM_calling
from RAG import RAG_application, filename

print(f"\n\nHi I am your friendly AI Assistant.  I have been provided with the following PDF file: {filename}. You may ask me any question and I will help you answer it based on my reading of this file !\n")
print("-"*40)
try:
    while True:
        query = input(f"🤖 Enter your question from {filename}: ")
        context_text = RAG_application(query)
        result = LLM_calling(query=query, context_text=context_text)
        print(result)

except KeyboardInterrupt:
    print("\nOperation cancelled by user. Have a great day!")