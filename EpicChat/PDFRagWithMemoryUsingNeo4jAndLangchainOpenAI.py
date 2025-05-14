#%pip install langchain langchain-neo4j langchain-openai

import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader

load_dotenv()
providerLLM = "openai"
providerLLMKey = os.getenv("OPENAI_API_KEY")
llmModel = "gpt-4.1"

#we are not using vector store
#QDRANT_HOST="localhost"
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "reform-william-center"

#The below example will create a connection with a Neo4j database 
# and will populate it with example data about movies and their actors.
from langchain_neo4j import Neo4jGraph

graph = Neo4jGraph()

# Import movie information

movies_query = """
LOAD CSV WITH HEADERS FROM 
'https://raw.githubusercontent.com/tomasonjo/blog-datasets/main/movies/movies_small.csv'
AS row
MERGE (m:Movie {id:row.movieId})
SET m.released = date(row.released),
    m.title = row.title,
    m.imdbRating = toFloat(row.imdbRating)
FOREACH (director in split(row.director, '|') | 
    MERGE (p:Person {name:trim(director)})
    MERGE (p)-[:DIRECTED]->(m))
FOREACH (actor in split(row.actors, '|') | 
    MERGE (p:Person {name:trim(actor)})
    MERGE (p)-[:ACTED_IN]->(m))
FOREACH (genre in split(row.genres, '|') | 
    MERGE (g:Genre {name:trim(genre)})
    MERGE (m)-[:IN_GENRE]->(g))
"""

graph.query(movies_query)


# Graph schema
# In order for an LLM to be able to generate a Cypher statement, 
# it needs information about the graph schema. When you 
# instantiate a graph object, it retrieves the information 
# about the graph schema. If you later make any changes to the graph, 
# you can run the refresh_schema method to refresh the schema information.

# graph.refresh_schema()
# print(graph.schema)

# For more involved schema information, you can use enhanced_schema option.
enhanced_graph = Neo4jGraph(enhanced_schema=True)
print(enhanced_graph.schema)


# Great! We've got a graph database that we can query. 
# Now let's try hooking it up to an LLM.

# LangChain comes with a built-in chain for this workflow that 
# is designed to work with Neo4j

# It is a simple out-of-the-box chain that 
# 1. takes a question, 
# 2. turns it into a Cypher query, 
# 3. executes the query, and 
# 4. uses the result to answer the original question.

from langchain_neo4j import GraphCypherQAChain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model=llmModel, temperature=0)
chain = GraphCypherQAChain.from_llm(
    graph=enhanced_graph, llm=llm, verbose=True, allow_dangerous_requests=True
)
response = chain.invoke({"query": "What was the cast of the Casino?"})
print(response)




