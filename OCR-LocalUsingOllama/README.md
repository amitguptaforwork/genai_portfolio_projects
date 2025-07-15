
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

**Architecture** 

### Flow Diagram ###

The flow diagram shows the complete application logic including:

- App initialization and page configuration
- Layout creation with sidebar and main area
- File upload handling
- Image processing workflow
- Ollama API integration
- Error handling
- Session state management
- Clear functionality 

```mermaid
flowchart TD
    A[App Start] --> B[Configure Streamlit Page]
    B --> C[Display Title & Description]
    C --> D[Create Layout: Main + Sidebar]
    D --> E[Add Clear Button]
    E --> F[Sidebar: File Uploader]
    F --> G{File Uploaded?}
    
    G -->|No| H[Show Info Message]
    G -->|Yes| I[Display Image in Sidebar]
    I --> J[Show Extract Text Button]
    J --> K{Extract Button Clicked?}
    
    K -->|No| L[Wait for User Action]
    K -->|Yes| M[Show Spinner: Processing...]
    M --> N[Call Ollama API]
    N --> O[Send Image to llama3.2-vision]
    O --> P[Process with OCR Prompt]
    P --> Q{API Success?}
    
    Q -->|No| R[Display Error Message]
    Q -->|Yes| S[Store Result in Session State]
    S --> T[Display Extracted Text in Main Area]
    
    T --> U[Show Footer]
    R --> U
    H --> U
    L --> U
    
    V[Clear Button Clicked] --> W[Delete Session State]
    W --> X[Rerun App]
    X --> C
    
    style A fill:#e1f5fe
    style N fill:#fff3e0
    style S fill:#e8f5e8
    style R fill:#ffebee
    style T fill:#e8f5e8
```

### Sequence Diagram ###
The sequence diagram illustrates the interactions between different components:

- User interactions: File upload, button clicks
- Streamlit UI: Interface management and display
- Session State: Data persistence across interactions
- PIL: Image processing
- Ollama API: Communication with the vision model
- Llama 3.2 Vision: The actual OCR processing

```mermaid
sequenceDiagram
    participant User
    participant StreamlitUI as Streamlit UI
    participant SessionState as Session State
    participant PIL as PIL Image
    participant Ollama as Ollama API
    participant LlamaVision as Llama 3.2 Vision

    User->>StreamlitUI: Launch App
    StreamlitUI->>StreamlitUI: Configure page settings
    StreamlitUI->>StreamlitUI: Display title and layout
    StreamlitUI->>User: Show file uploader in sidebar
    
    User->>StreamlitUI: Upload image file
    StreamlitUI->>PIL: Open uploaded image
    PIL->>StreamlitUI: Return image object
    StreamlitUI->>User: Display image preview in sidebar
    StreamlitUI->>User: Show "Extract Text" button
    
    User->>StreamlitUI: Click "Extract Text" button
    StreamlitUI->>User: Show spinner "Processing image..."
    
    StreamlitUI->>Ollama: Call ollama.chat()
    Note over Ollama: Model: llama3.2-vision
    Ollama->>LlamaVision: Send image + OCR prompt
    Note over LlamaVision: Analyze image and extract text<br/>Format as structured Markdown
    
    alt Successful Processing
        LlamaVision->>Ollama: Return extracted text
        Ollama->>StreamlitUI: Response with formatted content
        StreamlitUI->>SessionState: Store result in 'ocr_result'
        SessionState->>StreamlitUI: Confirm storage
        StreamlitUI->>User: Display extracted text in main area
    else Error Processing
        LlamaVision->>Ollama: Return error
        Ollama->>StreamlitUI: Exception thrown
        StreamlitUI->>User: Display error message
    end
    
    opt Clear Results
        User->>StreamlitUI: Click "Clear" button
        StreamlitUI->>SessionState: Delete 'ocr_result'
        SessionState->>StreamlitUI: Confirm deletion
        StreamlitUI->>StreamlitUI: Rerun app
        StreamlitUI->>User: Show info message
    end
```


---
