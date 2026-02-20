import requests

BOT_TOKEN = "8497745425:AAFodfrWggaVqB6lrymkoJ1swMooMZ9f_mY"    
CHAT_ID = "6507511401"       

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "Hello from test script!"
}

response = requests.post(url, data=data)
print(response.text)
