import json
import os
from dotenv import load_dotenv
import openai
from memory import MemoryDB

# Load environment variables from .env and set the OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_important_information(context_text):
    """
    Use GPT-4 to extract key points from the provided context text.
    Returns a JSON object.
    """
    prompt = (
        "Extract the key points from the following text and output in JSON format:\n\n"
        f"{context_text}\n"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a summarization assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    # Use the attribute access for message content as per the latest API style.
    summary_text = response.choices[0].message.content
    try:
        summary_json = json.loads(summary_text)
    except json.JSONDecodeError:
        summary_json = {"summary": summary_text}
    return summary_json

def process_dream_cycle(agent, memory_db: MemoryDB):
    """
    Process the agent's daily memory:
    1. Combine short-term memory.
    2. Extract important info via GPT-4.
    3. Store the summary in the vector DB.
    4. Clear the agent's short-term memory.
    """
    context = "\n".join(agent.short_term_memory)
    if not context.strip():
        return None

    important_info = extract_important_information(context)
    memory_db.add_memory(agent.name, important_info)
    agent.short_term_memory = []  # Clear daily memory after processing

    return important_info
