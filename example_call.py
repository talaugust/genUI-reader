"""
Run this first to check your Lumen setup:   python example_call.py

1. Lists the models your API key can use (find the exact Gemma ID here).
2. Sends one test message and prints the reply.

Your call_lumen() in app.py makes the same request as step 2.
"""
import os
import requests

API_KEY = os.getenv("LUMEN_API_KEY", "")
BASE_URL = "https://lumen.ncsa.illinois.edu/v1"
MODEL = "gemma-4-31b-it"

if not API_KEY:
    raise SystemExit('LUMEN_API_KEY is not set. Run: export LUMEN_API_KEY="sk_..."')

headers = {"Authorization": f"Bearer {API_KEY}"}

# 1. Which models can this key use?
models = requests.get(f"{BASE_URL}/models", headers=headers)
models.raise_for_status()
print("Models available to your key:")
for m in models.json()["data"]:
    print("  ", m["id"])

# 2. Send one message
body = {
    "model": MODEL,
    "messages": [
        {"role": "user", "content": "Define the word 'temporal' in one sentence."}
    ],
}
response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=body)
if not response.ok:
    print(f"\nRequest failed ({response.status_code}): {response.text}")
    print("If the model wasn't found, change MODEL to one of the IDs listed above.")
    raise SystemExit(1)

data = response.json()
print(f"\nReply from {MODEL}:")
print(data["choices"][0]["message"]["content"])
