import requests
import yfinance as yf
import time

BOT_TOKEN = "8729139885:AAEdK7DAoWK8O1cTkD5h7KTgPNDx2V_DFmw"
CHAT_ID = "6668235005"

SYMBOLS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X"
]

def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

print("AI BOT STARTED")

send_message("🚀 AI BOT STARTED")

while True:

    for symbol in SYMBOLS:

        try:

            data = yf.download(
                symbol,
                period="1d",
                interval="1m",
                progress=False
            )

            closes = list(data["Close"])

            if len(closes) < 2:
                continue

            last_price = float(closes[-1])
            previous_price = float(closes[-2])

            if last_price > previous_price:
                direction = "BUY"
            else:
                direction = "SELL"

            message = f"""
🔥 AI SIGNAL

PAIR: {symbol}

DIRECTION: {direction}

TIMEFRAME: 1 MINUTE
"""

            print(message)

            send_message(message)

        except Exception as e:

            print("ERROR:", e)

    time.sleep(60)