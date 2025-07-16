# GenAI Portfolio Projects

This repository showcases innovative GenAI projects that demonstrate practical applications of artificial intelligence in solving real-world problems. Each project highlights different aspects of AI technologies including autonomous agents, retrieval-augmented generation, and natural language processing.


## [RAG-Powered PDF Chatbot with LanceDB and Streamlit -works completlely offline !](https://github.com/amitguptaforwork/genai_portfolio_projects/blob/master/RAG-MultiPDF/readme.md)
**Python | LanceDB | Streamlit | Docling | Ollama | Gemma3 | Sentence Transformers**

I created a **completely offline** RAG system in this project.  We can upload any kind of documents like PDF, HTML, etc to our system.  A knowledge system is built by first using **Docling** to parse the documents into text and then saving that info in **LanceDB** as vector store.  Then, it can answer any user query by using the knowledge system and **Gemma3 LLM**.  Everything (including the vector store and LLM) is running locally, so total privacy and free operation.



## [RAG-CompanyProductBot: Enterprise Knowledge Assistant](https://github.com/amitguptaforwork/genai_portfolio_projects/blob/master/RAG-CompanyProductBot/readMe.md)
**Python | Open AI | LangChain | QdrantDB | Docker**

A "normal" chatbot cannot answer questions where data may not be publicly availalble.  Also, the chatbots and LLMs have data only upto a certain point in time.  
Here I present a powerful Retrieval-Augmented Generation (RAG) based question-answering system designed to help users explore **their own PDF data, maybe containing proprietary or latest data** using **LLMs** with context-aware responses.



## [Agent-Mini-Cursor: Python-Based Autonomous Agent Framework](https://github.com/amitguptaforwork/genai_portfolio_projects/blob/master/Agent-Mini-Cursor/readme.md)
**Python | Open AI**

This project is a coding-focused AI assistant designed to help users solve programming problems and answer coding-related queries. The assistant follows a structured, step-by-step process—**Start, Plan, Action, Observe, and Output**  (Chain-of-Thought based reasoning) —to ensure clear and logical problem-solving. It can execute terminal commands securely and provide detailed explanations for each step in the process.


## [OCR-LocalUsingOllama and Llama3.2 Vision Model](https://github.com/amitguptaforwork/genai_portfolio_projects/blob/master/OCR-LocalUsingOllama/README.md)
**Python | Llama3.2 Vision LLM | Streamlit |Google Colab | LocalTunnel | Ollama

This project demonstrates how easily we can use an LLM locally.  It uses **Llama 3.2 vision** and **Streamlit** to create a 100% locally running OCR app.  We can give any scanned image to the app and it will try to give us text out of it.
I demonstrate how to set it up completely locally if you have a decent machine or use the free hardware provided by **Gooogle Colab** to still run your code pretty much privately.  We setup **Ollama** in Google Colab and then use **LocalTunnel** to expose the system to the outside world!
