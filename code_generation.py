import json
import requests

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMWY5NDRmODItNjVkZC00YjFmLWI4NzQtMjExN2NhNzNiZTJlIiwidHlwZSI6ImFwaV90b2tlbiJ9.uwum-01WBPp4116uV1YREmZR79hhakjH7lCRL-89ueI"}

url = "https://api.edenai.run/v2/text/code_generation"
def generate_code(prompt, instructions):
    payload = {
        "providers": "openai",
        "prompt": prompt,
        "instruction": instructions,
        "temperature": 0.1,
        "max_tokens": 250,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    result = result['openai']['generated_text']
    return result