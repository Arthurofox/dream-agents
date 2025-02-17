import uuid
import chromadb
from chromadb.config import Settings

class MemoryDB:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=".chromadb/"
        ))
        # Create or access a collection for agent memories
        self.collection = self.client.get_or_create_collection(name="agent_memories")

    def add_memory(self, agent_name, memory_info):
        """
        Add a summarized memory to the vector DB.
        """
        memory_id = str(uuid.uuid4())
        # Convert memory_info to string (JSON format or plain text)
        memory_text = str(memory_info)
        self.collection.add(
            documents=[memory_text],
            ids=[memory_id],
            metadatas=[{"agent": agent_name}],
        )
        return memory_id

    def query_memory(self, agent_name, query_text, n_results=3):
        """
        Retrieve memories for an agent based on a query.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"agent": agent_name}
        )
        return results
