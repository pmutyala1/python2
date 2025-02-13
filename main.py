import os
import json
import time
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

# Define response structure
class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")

# Initialize Groq API client
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

# Hardcoded list of NASA facts for testing (if not using API)
nasa_facts = [
    "NASA stands for National Aeronautics and Space Administration.",
    "It was founded in 1958.",
    "NASA led the Apollo program, which landed humans on the Moon in 1969.",
    "It operates the International Space Station (ISS).",
    "NASA has sent robotic missions to Mars, including Perseverance and Curiosity.",
    "The Hubble Space Telescope is one of NASA's most famous space observatories.",
    "NASA's Artemis program aims to return humans to the Moon.",
    "NASA developed the Space Shuttle program, which ran from 1981 to 2011.",
    "The Voyager spacecraft, launched by NASA, have traveled beyond our solar system.",
    "NASA's Jet Propulsion Laboratory (JPL) specializes in robotic space exploration.",
    "NASA's Kennedy Space Center is located in Florida.",
    "NASA collaborates with SpaceX, Blue Origin, and other private companies."
]

# Function to fetch a fact using the API
def get_groq_response():
    try:
        resp = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": "Tell me an interesting fact about NASA"}],
            response_model=Character,
        )
        if resp.fact:
            return resp.fact[0]  # Return only one fact
    except Exception as e:
        print(f"Error: {e}")
        return None

# Main loop for user interaction
def chat_with_groq():
    print("Welcome to the NASA Facts Chat! Type 'quit' to exit.")
    
    fact_index = 0
    use_api = False  # Change to True to use Groq API

    while True:
        user_input = input("\nPress ENTER to get a NASA fact, or type 'quit' to exit: ")
        
        if user_input.lower() == "quit":
            print("\nExiting chat. Goodbye!")
            break

        # Get a fact from API or hardcoded list
        if use_api:
            fact = get_groq_response()
        else:
            fact = nasa_facts[fact_index] if fact_index < len(nasa_facts) else "No more facts available!"

        print(f"\n🚀 NASA Fact: {fact}")

        fact_index += 1
        if fact_index >= len(nasa_facts):  # Loop back to the first fact
            fact_index = 0

        time.sleep(1)  # Small delay for readability

# Run the chat
if __name__ == "__main__":
    chat_with_groq()