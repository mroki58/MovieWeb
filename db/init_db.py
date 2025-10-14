from neo4j import GraphDatabase
from config import Config

_driver = GraphDatabase.driver(
    Config.NEO4J_URI,
    auth=(Config.NEO4J_USER,Config.NEO4J_PASSWORD)
)

def get_driver():
    return _driver

def close_driver():
    return _driver.close()
