import requests

BOT_TOKEN = ""    
CHAT_ID = ""       

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "Hello from test script!"
}

response = requests.post(url, data=data)
print(response.text)
