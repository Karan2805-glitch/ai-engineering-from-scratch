import os
import json
import urllib.request
import urllib.error

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# 1. Define the API endpoint
url = "https://api.groq.com/openai/v1/chat/completions"

# 2. Define the HTTP headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "User-Agent": "ai-engineering-course/1.0",
}

# 3. Define the request body
payload = {
    "model": "openai/gpt-oss-20b",
    "messages": [
        {
            "role": "user",
            "content": "What is a neural network? Explain in one sentence."
        }
    ],
    "max_completion_tokens": 256,
}

# 4. Convert the Python dictionary into JSON bytes
data = json.dumps(payload).encode("utf-8")

# 5. Construct the HTTP POST request
request = urllib.request.Request(
    url,
    data=data,
    headers=headers,
    method="POST",
)

try:
    # 6. Send the request and read the response
    with urllib.request.urlopen(request, timeout=30) as http_response:
        response_data = json.loads(http_response.read().decode("utf-8"))

    # 7. Extract the generated answer
    answer = response_data["choices"][0]["message"]["content"]

    print("\n=== Raw HTTP API Response ===")
    print(answer)

    # 8. Display token usage
    usage = response_data.get("usage", {})

    print("\n=== Token Usage ===")
    print(f"Input tokens:  {usage.get('prompt_tokens', 'Unavailable')}")
    print(f"Output tokens: {usage.get('completion_tokens', 'Unavailable')}")
    print(f"Total tokens:  {usage.get('total_tokens', 'Unavailable')}")

except urllib.error.HTTPError as error:
    print(f"HTTP error: {error.code}")

    # Read the server's error message without exposing request headers
    error_body = error.read().decode("utf-8", errors="replace")
    print(f"Details: {error_body[:1000]}")

except urllib.error.URLError as error:
    print(f"Connection error: {error.reason}")

except (json.JSONDecodeError, KeyError, IndexError, TypeError) as error:
    print(f"Could not parse the API response: {error}")