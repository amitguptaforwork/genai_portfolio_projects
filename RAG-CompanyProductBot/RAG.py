from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

from langchain_qdrant import QdrantVectorStore
import os
from openai import OpenAI


google_api_key = os.getenv("GEMINI_API_KEY")

filename = "shafer-actuation-solutions-en-5922766.pdf"
pdf_path = Path(__file__).parent / filename
collection_name=filename.replace(".pdf", "").replace("-", "")

def RAG_application(query):
    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )

    split_docs = text_splitter.split_documents(documents=documents)

    #You can choose which provider to use for embedding creation
    #Sometimes Gemini is unavailable
    
    # embeddings = GoogleGenerativeAIEmbeddings(
    #     model="models/text-embedding-004",
    #     google_api_key=google_api_key
    # )
    embeddings= OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key = os.getenv("OPENAI_API_KEY"))


   

    # Use LangChain's QdrantVectorStore to handle the collection
    try:
        # Try to load the existing collection
        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            url='http://localhost:6333',
            collection_name=collection_name
        )
        print(f"Collection '{collection_name}' already exists. Using the existing collection.")
    except Exception as e:
        # If the collection doesn't exist, create it
        print(f"Collection '{collection_name}' does not exist. Creating it now.")
        vector_store = QdrantVectorStore.from_documents(
            documents=split_docs,
            embedding=embeddings,
            url='http://localhost:6333',
            collection_name=collection_name
        )
        print(f"Collection '{collection_name}' created successfully.")

    print("📝📝📝📝📝📝📝📝-----RAG processed-----📝📝📝📝📝📝📝")

    retriever = vector_store.from_existing_collection(
        embedding=embeddings,
        url='http://localhost:6333',
        collection_name= collection_name
    )

    RAG_search_result = retriever.similarity_search(
        query=query
    )

    context_text = " ".join(
        [f"Page {doc.metadata['page']}: {doc.page_content}" for doc in RAG_search_result]
    )

    # print("Search results:")
    # for doc in RAG_search_result:
    #     print(doc.metadata["page_label"],doc.metadata["_id"])
    # print("_"*20)
    return context_text
