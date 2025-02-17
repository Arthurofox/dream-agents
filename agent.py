from typing import Dict, List, Optional
import datetime
import chromadb
from chromadb.config import Settings
import openai
from dataclasses import dataclass
import streamlit as st

@dataclass
class Memory:
    """A single memory unit that can be stored in the agent's memory stream."""
    content: str
    created_at: datetime.datetime
    memory_type: str  # 'experience', 'reflection', or 'dream'
    importance: float
    embedding: Optional[List[float]] = None
    
class DreamingAgent:
    def __init__(self, name: str, chroma_client=None):
        """Initialize a new agent with memory capabilities and dream states."""
        self.name = name
        self.memories: List[Memory] = []
        
        # Initialize ChromaDB for vector storage
        if chroma_client is None:
            self.chroma_client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=f"db_{name}"
            ))
        else:
            self.chroma_client = chroma_client
            
        # Create collections for different types of memories
        self.memory_collection = self.chroma_client.get_or_create_collection(
            name=f"{name}_memories"
        )
        
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI's API."""
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']
    
    def add_memory(self, content: str, memory_type: str = 'experience'):
        """Add a new memory to both the list and vector store."""
        # Create memory object
        memory = Memory(
            content=content,
            created_at=datetime.datetime.now(),
            memory_type=memory_type,
            importance=self._calculate_importance(content),
            embedding=self._get_embedding(content)
        )
        
        # Add to local memory list
        self.memories.append(memory)
        
        # Add to vector store
        self.memory_collection.add(
            documents=[content],
            embeddings=[memory.embedding],
            metadatas=[{
                "created_at": memory.created_at.isoformat(),
                "memory_type": memory_type,
                "importance": memory.importance
            }],
            ids=[f"{memory_type}_{len(self.memories)}"]
        )
        
    def _calculate_importance(self, content: str) -> float:
        """Calculate importance score for a memory using OpenAI."""
        prompt = f"""Rate the importance of this memory on a scale of 0.0 to 1.0:
        Memory: {content}
        
        Return only the numeric score, nothing else."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            return float(response.choices[0].message.content.strip())
        except:
            return 0.5
            
    def dream(self):
        """Generate a dream based on recent memories."""
        if not self.memories:
            return "No memories to dream about..."
            
        # Get recent important memories
        recent_memories = sorted(
            self.memories, 
            key=lambda x: x.importance * (1 if x.memory_type == 'experience' else 0.5), 
            reverse=True
        )[:5]
        
        memory_context = "\n".join([m.content for m in recent_memories])
        
        prompt = f"""Based on these recent memories:
        {memory_context}
        
        Generate a dream-like reflection that connects these experiences in an 
        abstract or metaphorical way. The dream should reveal deeper patterns
        or insights about these experiences.

        Dream:"""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        dream_content = response.choices[0].message.content
        self.add_memory(dream_content, memory_type='dream')
        return dream_content
        
    def reflect(self) -> str:
        """Generate a reflection based on recent memories and dreams."""
        if not self.memories:
            return "No memories to reflect on..."
            
        # Get recent memories of all types
        recent_memories = sorted(
            self.memories,
            key=lambda x: x.created_at,
            reverse=True
        )[:10]
        
        memory_context = "\n".join(
            [f"{m.memory_type}: {m.content}" for m in recent_memories]
        )
        
        prompt = f"""Based on these recent memories and dreams:
        {memory_context}
        
        Generate a thoughtful reflection that:
        1. Identifies patterns or themes
        2. Draws insights or conclusions
        3. Suggests potential areas for growth or learning

        Reflection:"""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        reflection = response.choices[0].message.content
        self.add_memory(reflection, memory_type='reflection')
        return reflection

    def retrieve_similar_memories(self, query: str, n_results: int = 5):
        """Retrieve memories similar to the query."""
        query_embedding = self._get_embedding(query)
        results = self.memory_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results