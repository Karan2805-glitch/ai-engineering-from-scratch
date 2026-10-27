import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

# Read the API key securely
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Check your .env file."
    )

# Create a Groq client
client = Groq(api_key=api_key)

try:
    # Send a message to the language model
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": "What is a neural network? Explain in one sentence."
            }
        ],
        max_completion_tokens=256
    )

    # Extract the generated response
    answer = response.choices[0].message.content

    print("\n=== Groq API Response ===")
    print(answer)

    # Display token usage
    print("\n=== Token Usage ===")
    print(f"Input tokens:  {response.usage.prompt_tokens}")
    print(f"Output tokens: {response.usage.completion_tokens}")
    print(f"Total tokens:  {response.usage.total_tokens}")

except Exception as error:
    print(f"\nAPI call failed: {error}")