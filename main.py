import random
import streamlit as st
from agent import Agent
from dream_cycle import process_dream_cycle
from memory import MemoryDB
import ui

# Initialize the vector database
memory_db = MemoryDB()

# Create a few agents with random personality vectors
agents = []
for i in range(4):
    agent = Agent(
        name=f"Agent_{i+1}",
        personality_vector=[random.random() for _ in range(5)],
        goals=["Explore", "Interact", "Learn"]
    )
    agents.append(agent)

def run_simulation():
    st.sidebar.title("Simulation Controls")
    dream_cycle_trigger = st.sidebar.button("Trigger Dream Cycle")
    
    # Simulate basic interactions for each agent
    for agent in agents:
        action = agent.act()
        if action == "talk":
            other = random.choice([a for a in agents if a != agent])
            interaction = agent.interact(other)
            st.write(interaction)
        elif action == "move":
            st.write(f"{agent.name} moves around.")
        elif action == "interact":
            st.write(f"{agent.name} interacts with the environment.")
        
        st.write(f"{agent.name} performed action: {action}")
    
    debug_info = {}
    if dream_cycle_trigger:
        st.write("Dream Cycle Triggered!")
        for agent in agents:
            info = process_dream_cycle(agent, memory_db)
            debug_info[agent.name] = info
        st.write("Dream cycle processing complete.")
    
    ui.display_main_view(agents, debug_info)

if __name__ == "__main__":
    run_simulation()
