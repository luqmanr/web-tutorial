import requests

# go to https://aistudio.google.com/app/apikey
API_KEY = 'ar0w3jf0s9jf0s9jf09sjd09fjsdf'
URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'
headers = {
    'Content-Type': 'application/json'
}
data = {
    "contents": [
        {
            "parts": [
                {
                    "text": "halo, tolong buatin dongeng 50 kata dong"
                }
            ]
        }
    ]
}
response = requests.post(
    URL,
    headers=headers,
    json=data,
    timeout=30)

print('status code:', response.status_code)
print('response:', response.text)
print('response:', response.json()["candidates"][0]["content"]["parts"][0]["text"])
