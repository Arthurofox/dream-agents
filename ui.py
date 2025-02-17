import streamlit as st

def display_main_view(agents, debug_info):
    st.title("Dreaming Agents Simulation")
    
    st.header("Agents Overview")
    for agent in agents:
        st.subheader(agent.name)
        st.text(f"Goals: {agent.goals}")
        st.text(f"Short-term memory count: {len(agent.short_term_memory)}")
    
    st.sidebar.title("Agent Stats & Memory Inspection")
    for agent in agents:
        st.sidebar.subheader(agent.name)
        st.sidebar.write(f"Memory items: {len(agent.short_term_memory)}")
    
    st.sidebar.title("Dream Cycle Debug Info")
    st.sidebar.write(debug_info)
