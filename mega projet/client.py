import requests

API_KEY = "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"  # Replace with your actual key
URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "max_tokens": 50
}

response = requests.post(URL, headers=headers, json=data)

if response.status_code == 200:
    print(response.json()["choices"][0]["message"]["content"])
else:
    print(f"Error {response.status_code}: {response.text}")
