import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(self.url, auth=(self.user, self.password))
            print("Connected to Neo4j service")
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query,parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response



load_dotenv()

conn = Neo4jConnection(url=os.getenv("DB_URI"), user=os.getenv("DB_USER"), password=os.getenv("DB_PWD"))

driver = conn.driver
