import os
import numpy as np
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity


# Load Environment Variables

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


# Initialize Clients

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=GROQ_API_KEY)


# Intent Detection

def detect_intent(query: str):
    query_lower = query.lower()

    if "most" in query_lower or "highest" in query_lower or "top" in query_lower:
        return "aggregation"

    if "compare" in query_lower:
        return "comparison"

    return "vector"



# Graph Aggregation Retrieval

def retrieve_service_aggregation():
    with driver.session() as session:
        result = session.run("""
            MATCH (c:CostRecord)-[:HAS_SERVICE]->(s:Service)
            RETURN s.name AS service,
                   SUM(c.billedCost) AS totalCost
            ORDER BY totalCost DESC
        """)
        return list(result)



# Vector Retrieval

def retrieve_vector(query: str, top_k=3):

    query_embedding = embedding_model.encode(query)

    with driver.session() as session:
        result = session.run("MATCH (c:CostRecord) RETURN c")

        scored_nodes = []

        for record in result:
            node = record["c"]
            node_embedding = np.array(node["embedding"])

            score = cosine_similarity(
                [query_embedding],
                [node_embedding]
            )[0][0]

            scored_nodes.append((node, score))

    scored_nodes.sort(key=lambda x: x[1], reverse=True)

    return scored_nodes[:top_k]



# LLM Generation

def generate_response(query: str):

    intent = detect_intent(query)

    # ---------------- Aggregation ----------------
    if intent == "aggregation":
        records = retrieve_service_aggregation()

        context_text = ""
        for record in records:
            context_text += f"Service: {record['service']} | Total Cost: {record['totalCost']}\n"

    # ---------------- Vector ----------------
    else:
        nodes = retrieve_vector(query)

        context_text = ""
        for node, score in nodes:
            context_text += (
                f"Resource: {node['resourceId']} | "
                f"Cost: {node['billedCost']} | "
                f"Vendor: {node['vendor']} | "
                f"Environment: {node['environment']} | "
                f"Similarity: {score:.3f}\n"
            )

    prompt = f"""
    You are a Cloud FinOps expert.

    Context:
    {context_text}

    Question:
    {query}

    Provide a clear and professional answer using the context.
    """

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content, context_text