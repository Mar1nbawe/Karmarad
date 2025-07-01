import os

import requests
import json
from dotenv import load_dotenv
from Funcs.json_parser import json_parser





def Display_json_content(bytes_content):
    content = json.loads(bytes_content)
    return content

def Parse_interpretter_name(json_content):

    content = json.loads(json_content['choices'][0]['message']['content'].replace("'", "\""))


    return content

load_dotenv()
link = os.getenv("MOD_URL")
headers = {"Content-Type": "application/json"}


def gossip_endpoint(prompt):
    r = requests.post(link, headers=headers, json={
        "model": "uncategorized",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": -1,
        "stream": False
    })
    if r.status_code == 200:
        decoded_content = r.content.decode("utf-8")
        parsed = json_parser(decoded_content)

        return parsed
    else:
        print(f"Error: {r.status_code}")

def interpretter_endpoint(prompt):
    r = requests.post(link, headers=headers, json={
        "model": "gguf-flan-t5-base",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": -1,
        "stream": False
    })

    if r.status_code == 200:
        decoded_content = r.content.decode("utf-8")
        return Display_json_content(decoded_content)

    else:
        print(f"Error: {r.status_code}")