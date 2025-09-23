# 🚀 Oracle 23ai: AI + Vector Search Inside the Database

# ;tldr Explain in Plain english
I recently tried Oracle 23ai — and it’s a game-changer.



- Imagine a table with 10 business columns. 
- Until now, you couldn’t search them in plain English or semantically. For example, if you stored cities like Hyderabad, Mumbai, Delhi, Paris, London — the DB couldn’t select rows for you if you said `search all rows for me from India`.
    - Note- you dont want to hardcode which cities are in India
- Oracle 23ai fixes this using machine learning. It now can know that Hyderabad, Mumbai, and Delhi are “related”. 
 

The best part?

 👉 This AI-powered search happens inside the database — no need for a separate vector DB. That means less complexity, better security, and real-time results on live data.



 # I have time. Explain me properly

- If you are new to Generative AI, then understand that computers are being trained to understand meanings of words humans speak.  This is the focus of the field of NLP.   
- Machine learning models called LLMs have since been designed to do this task.
- Now that these models are trained and available for use for us, I can essentially give a word and search for all words that are similiar to that word.  
- This, in technical jargon is called a Vector search because the "words" or tokens are stored as mathematical numbers in an array-like structure (aka Vector) internally by the database 
- But how may this be useful.   
  - Imagine a table with 10 business columns. Until now, you couldn’t search it using plain English or semantically. 
  - What does **semantic** mean here.  Example, if you stored cities like Hyderabad, Mumbai, Delhi, Paris, London — the DB couldn’t select rows for you if you said `search all rows for me from India`.
    - Note- you dont want to hardcode which cities are in India
    - You are just interested in finding out rows that belong to India.  Thats it.
  - Now the challenge is, the table does not know what is India.  It CANNOT search these rows for you.  
  - The DB architect in you would be jumping and shouting - wrong question or trick question. Why did we not anticipate that user may ask based on country and hence lets store a country column.
  - Answer: You are missing a point here.  In this new world, the user can ask anything.  Like, `get me all rows where the city has temperature average of 10 degrees celcius`.  
  - So you see the issue, you cannot (and need not) anticipate all queries from user.  If its general knowledge, then the machine learning LLM model can do it for you (its a genie in a bottle and acts like a smart worker for you)
- **Oracle 23ai fixes - using some cool maths and a inbuild machine learning model, it can do the math for you to know Hyderabad, Mumbai, and Delhi are “related”.**
  - You need to create what are called Vector Embeddings.  
    - How? You choose the columns, the DB generates embeddings (A very crude analogy of what exactly is a embedding here is to imagine it as a composite primary key with all columns)
  - And you can run natural language queries directly on your Oracle DB.  How cool is that.


### Geeky definition: 
Oracle Database **23ai** introduces cutting-edge **AI integration** and **vector search** capabilities, enabling semantic queries and Retrieval Augmented Generation (RAG) — all *inside the database*.

This README summarizes key concepts, technical details, and practical insights based on research notes and slides.

---

## 📌 Why It Matters

Traditionally, running semantic or similarity search required moving business data to an external vector database.  
With Oracle 23ai, you can now:

- Run **AI-powered vector similarity searches directly in Oracle**  
- Avoid costly **data movement**  
- Ensure **security and compliance** by keeping data in place  
- Query **live and current business data**  

---

## 🧩 Key Concepts

### 🔹 Vector Embeddings
- Convert unstructured data into numerical vectors.
- Enable semantic search (e.g., knowing *Hyderabad, Mumbai, Delhi* are “related”).  
<img src="images/SampleEmbeddingSpace.jpeg" width="300" alt="Description">
- Created using **neural networks** (typically transformer-based models).

**Examples of embedding models:**

| Model | Type | Dimensions |
|-------|------|------------|
| Cohere `embed-english-v3.0` | Text | 1024 |
| OpenAI `text-embedding-3-large` | Text | 3072 |
| HuggingFace `all-MiniLM-L6-v2` | Text | 384 |
| ResNet | Image | varies |
| Spectrogram + CNN | Audio | varies |

---

### 🔹 Oracle VECTOR Data Type
Oracle 23ai has introduced a new data type to support embeddings - `VECTOR` :

- Homogeneous array of numerical values (`int8`, `binary`, `float32`, `float64`)  
- Arbitrary dimensions supported  
- Designed for **AI/ML similarity search operations**  

👉 [Oracle AI Vector Search Guide](https://python-oracledb.readthedocs.io/en/latest/user_guide/vector_data_type.html)

---

### 🔹 You can build your RAG (Retrieval Augmented Generation) with Oracle serving both as your "normal" enterprise DB as well as vector db
- Combines **vector search** with **LLM-powered responses**  
- Mitigates hallucinations by grounding answers in database results  
- Can be enhanced with **reranking** to improve quality  

---

## 📊 Architecture Insights

Vector databases use advanced indexing techniques

- **HSNW (in-memory)** → ultra-fast search 
- **IVF (on-disk)** → scalable search  
- Oracle added a new Hybrid Vector index too which is a combination of Oracle Text Index and Vector index on your unstructured data

---

## 📽️ Resources & References

- Oracle official AI demos:  
  - [Intro to Vector Search](https://youtu.be/F6hyI1wvd4w)  
  - [RAG with SQL Example](https://youtu.be/irOsuF7Mtjs)  

---

## 🖼️ Visuals

Below are extracted diagrams and slide illustrations from the research notes:

![Illustration 1](images/image_1.png)
![Illustration 2](images/image_2.png)
![Illustration 3](images/image_3.png)
![Illustration 4](images/image_4.png)
![Illustration 5](images/image_5.png)
![Illustration 6](images/image_6.png)
![Illustration 7](images/image_7.png)
![Illustration 8](images/image_8.png)
![Illustration 9](images/image_9.png)
![Illustration 10](images/image_10.png)
![Illustration 11](images/image_11.png)
![Illustration 12](images/image_12.png)
![Illustration 13](images/image_13.png)
![Illustration 14](images/image_14.png)
![Illustration 15](images/image_15.png)
![Illustration 16](images/image_16.png)
![Illustration 17](images/image_17.png)
![Illustration 18](images/image_18.png)
![Illustration 19](images/image_19.png)
![Illustration 20](images/image_20.png)
![Illustration 21](images/image_21.png)
![Illustration 22](images/image_22.png)
![Illustration 23](images/image_23.png)
![Illustration 24](images/image_24.png)
![Illustration 25](images/image_25.png)
![Illustration 26](images/image_26.png)
![Illustration 27](images/image_27.png)
