from dotenv import load_dotenv
import os

from langchain_community.graphs import Neo4jGraph

load_dotenv("./env")

AURA_INSTANCENAME = os.getenv('AURA_INSTANCENAME')
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE')
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

# Instantiate connection to Neo4j
kg = Neo4jGraph(
    url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE
)

# Calculate number of nodes
cypher = """
  MATCH (n) 
  RETURN count(n) AS NumOfNodes
  """

result = kg.query(cypher)
print(f"There are {result[0]['NumOfNodes']} nodes in this graph.")

# Calculate Number of countries
cypher = """
  MATCH (n:Country) 
  RETURN count(n) AS NumOfCountries
  """

result = kg.query(cypher)
print(f"There are {result[0]['NumOfCountries']} nodes in this graph labelled as country.")

cypher = """
  MATCH (albert:Person {name: "Albert Einstein"}) 
  RETURN albert
  """
result = kg.query(cypher)
print(result)





