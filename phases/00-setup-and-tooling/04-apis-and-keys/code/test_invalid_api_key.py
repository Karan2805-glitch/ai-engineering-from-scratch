import json
import urllib.request
import urllib.error

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer invalid_test_key",
    "User-Agent": "ai-engineering-course/1.0",
}

payload = {
    "model": "openai/gpt-oss-20b",
    "messages": [
        {
            "role": "user",
            "content": "Say hello."
        }
    ],
    "max_completion_tokens": 20,
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers=headers,
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        print("Unexpected success:", response.status)

except urllib.error.HTTPError as error:
    print("HTTP status:", error.code)

    details = error.read().decode("utf-8", errors="replace")
    print("Error details:", details[:1000])