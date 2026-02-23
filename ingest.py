import pandas as pd
import os
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_graph():
    df = pd.read_csv("sample_data.csv")

    with driver.session() as session:
        for _, row in df.iterrows():

            text = f"{row.serviceName} {row.vendor} {row.region}"
            embedding = model.encode(text).tolist()

            session.run("""
                MERGE (s:Service {name:$service})
                MERGE (r:Resource {id:$resource})
                MERGE (l:Location {name:$region})
                MERGE (c:CostRecord {resourceId:$resource})
                SET c.billedCost=$cost,
                    c.environment=$env,
                    c.vendor=$vendor,
                    c.embedding=$embedding

                MERGE (c)-[:HAS_SERVICE]->(s)
                MERGE (c)-[:INCURRED_BY]->(r)
                MERGE (r)-[:DEPLOYED_IN]->(l)
            """,
            service=row.serviceName,
            resource=row.resourceId,
            region=row.region,
            cost=row.billedCost,
            env=row.environment,
            vendor=row.vendor,
            embedding=embedding
            )

if __name__ == "__main__":
    create_graph()
    print("Data Loaded Successfully")