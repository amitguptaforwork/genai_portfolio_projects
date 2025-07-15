
# LLama3.2-OCR

This project leverages Llama 3.2 vision and Streamlit to create a 100% locally running OCR app.  We can give any scanned image to the app and it will try to give us text out of it.  

Unlike traditional OCR software like Tesseract, this app utilizes the more powerful system - an LLM to do the same.  The results are much better in most cases.  Also the LLM is going to run locally in our system, thereby ensuring privacy as well as no charges !

## Installation and setup

**Setup Ollama**:
   1. Install Docker Desktop (on Windows)
   2. Install ollama image
   `docker pull ollama/ollama `
   ![pllama](images/ollama_install.png)
   3. Start ollama container. This can be easily done using docker desktop.  If you want to start from command line then use 
   `docker run -d --name ollama -p 11434:11434 ollama/ollama `
   4. Go to terminal in the ollama container
   ![terminal](images/ollama_terminal.png)
   5. Pull llama 3.2 vision model
   `ollama pull llama3.2-vision`
   ![pull](images/ollama_pull.png)
   6. You can see the models available
   ![list](images/ollama_list.png)


**Install Dependencies**:
   Ensure you have Python 3.11 or later installed.
   ```bash
   pip install streamlit ollama
   ```

---
