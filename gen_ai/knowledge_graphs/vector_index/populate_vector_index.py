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

# Example of populate vector index params 
populate_vector_index_params = {
    "node_label_variable": "m",
    "node_label": "Movie",
    "attribute_to_embed": "tagline",
    "attribute_embedding": "tagline.Embedding",
    "openAiApiKey": OPENAI_API_KEY, 
    "openAiEndpoint": OPENAI_ENDPOINT
}


# Populate vector index 
kg.query("""
    MATCH ($node_label_variable:$node_label) WHERE $node_label_variable.$attribute_to_embed IS NOT NULL
    WITH $node_label_variable, genai.vector.encode(
        $node_label_variable.$attribute_to_embed, 
        "OpenAI", 
        {
          token: $openAiApiKey,
          endpoint: $openAiEndpoint
        }) AS vector
    CALL db.create.setNodeVectorProperty($node_label_variable, "attribute_embedding", vector)
    """, 
    params=populate_vector_index_params
)
