from dotenv import load_dotenv
import os

from langchain_community.graphs import Neo4jGraph

# Warning control
import warnings
warnings.filterwarnings("ignore")

# Load from environment
load_dotenv('.env', override=True)
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = os.getenv('OPENAI_BASE_URL') + '/embeddings'

# Connect to the knowledge graph instance using LangChain
kg = Neo4jGraph(
    url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE
)


similarity_search_vector_index_params = {
    "vector_index_label": 'movie_tagline_embedding',
    "question": "What movies about love?",
    "top_k": 5, 
    "openAiApiKey":OPENAI_API_KEY, 
    "openAiEndpoint": OPENAI_ENDPOINT
}

kg.query("""
    WITH genai.vector.encode(
        $question, 
        "OpenAI", 
        {
          token: $openAiApiKey,
          endpoint: $openAiEndpoint
        }) AS question_embedding
    CALL db.index.vector.queryNodes(
        $vector_index_label, 
        $top_k, 
        question_embedding
        ) YIELD node AS movie, score
    RETURN movie.title, movie.tagline, score
    """, 
    params=similarity_search_vector_index_params
)