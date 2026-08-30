import os
import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://uae.ibraqperfumes.com/en/blue-oud/p1521501490"

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Safari/604.1"
}

response = requests.get(PRODUCT_URL, headers=headers, timeout=30)
response.raise_for_status()

html = response.text
soup = BeautifulSoup(html, "html.parser")

text = soup.get_text(" ", strip=True).lower()

out_of_stock = "out of stock" in text

in_stock = (
    "add to cart" in text
    or "add to bag" in text
    or "buy now" in text
)

state_file = "stock_state.txt"

if os.path.exists(state_file):
    previous_state = open(state_file).read().strip()
else:
    previous_state = "unknown"

if out_of_stock and not in_stock:
    current_state = "out"
else:
    current_state = "in"

print("Previous:", previous_state)
print("Current:", current_state)

with open(state_file, "w") as f:
    f.write(current_state)

if previous_state == "out" and current_state == "in":

    message = (
        "🚨🚨 BLUE OUD IS BACK IN STOCK! 🚨🚨\n\n"
        "Ibrahim Al Qurashi Blue Oud 100ml\n\n"
        f"BUY NOW:\n{PRODUCT_URL}"
    )

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )

    print("RESTOCK ALERT SENT!")
