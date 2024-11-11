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

# Example of create vector index params 
create_vector_index_params = {
    "vector_index_label": "movie_tagline_embedding",
    "node_label_variable": "m",
    "node_label": "Movie",
    "attribute_embedding": "tagline.Embedding"
}


# Create Vector index
kg.query("""
  CREATE VECTOR INDEX $vector_index_label IF NOT EXISTS
  FOR ($node_label_variable:$node_label) ON ($node_label_variable.$attribute_embedding)
  OPTIONS { indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }}""",
  params=create_vector_index_params
)

# FOR ($node_label_variable:$node_label) ON ($node_label_variable.$embedding_name) -> 
# it will add an attribute to the node_label that refers to embeddings

# Show all vector indexes
kg.query("""SHOW VECTOR INDEXES""")

