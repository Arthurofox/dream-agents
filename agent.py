import numpy as np

class Agent:
    def __init__(self, name, personality_vector, goals=None):
        self.name = name
        self.personality_vector = personality_vector  # e.g., a list of floats
        self.short_term_memory = []  # Stores daily interactions
        self.goals = goals if goals is not None else []
        self.position = (0, 0)  # Placeholder for spatial positioning

    def act(self):
        """
        Randomly decide an action from the agent's basic action space.
        """
        action = np.random.choice(["talk", "move", "interact"])
        return action

    def interact(self, other_agent):
        """
        Simulate an interaction with another agent.
        """
        interaction = f"{self.name} interacts with {other_agent.name}"
        self.short_term_memory.append(interaction)
        other_agent.short_term_memory.append(interaction)
        return interaction

    def add_memory(self, memory_item):
        """
        Manually add a memory item.
        """
        self.short_term_memory.append(memory_item)
