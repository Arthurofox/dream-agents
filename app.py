import streamlit as st
from agent import DreamingAgent
import openai
import os

# Initialize OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize or get agent from session state
if 'agent' not in st.session_state:
    st.session_state.agent = DreamingAgent("TestAgent")

st.title("Dreaming Agent Demo")

# Input section for new memories
st.header("Add New Memory")
new_memory = st.text_area("Enter a new memory or experience:")
if st.button("Add Memory"):
    if new_memory:
        st.session_state.agent.add_memory(new_memory, memory_type='experience')
        st.success("Memory added!")

# Dreaming section
st.header("Generate Dream")
if st.button("Generate Dream"):
    dream = st.session_state.agent.dream()
    st.write("Dream:")
    st.write(dream)

# Reflection section
st.header("Generate Reflection")
if st.button("Generate Reflection"):
    reflection = st.session_state.agent.reflect()
    st.write("Reflection:")
    st.write(reflection)

# Memory retrieval section
st.header("Search Memories")
search_query = st.text_input("Enter search query:")
if st.button("Search"):
    if search_query:
        results = st.session_state.agent.retrieve_similar_memories(search_query)
        st.write("Similar memories:")
        for doc in results['documents'][0]:
            st.write(doc)

# View all memories
st.header("All Memories")
if st.checkbox("Show all memories"):
    for memory in st.session_state.agent.memories:
        st.write(f"Type: {memory.memory_type}")
        st.write(f"Created: {memory.created_at}")
        st.write(f"Importance: {memory.importance}")
        st.write(f"Content: {memory.content}")
        st.write("---")