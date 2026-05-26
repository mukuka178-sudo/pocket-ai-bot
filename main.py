import requests
import yfinance as yf
import time

# =========================================
# TELEGRAM SETTINGS
# =========================================

BOT_TOKEN = "8729139885:AAEdK7DAoWK8O1cTkD5h7KTgPNDx2V_DFmw"
CHAT_ID = "6668235005"

# =========================================
# BOT SETTINGS
# =========================================

SYMBOLS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X"
]

TIMEFRAME = "1m"

CONFIDENCE_THRESHOLD = 50

# =========================================
# SEND TELEGRAM MESSAGE
# =========================================

def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# =========================================
# MARKET ANALYSIS
# =========================================

def analyze_market(symbol):

    try:

        data = yf.download(
            symbol,
            period="1d",
            interval=TIMEFRAME,
            progress=False
        )

        closes = list(data["Close"])

        if len(closes) < 10:
            return None

        last_price = float(closes[-1])
        previous_price = float(closes[-2])

        confidence = 50

        # =====================================
        # PRICE ACTION
        # =====================================

        if last_price > previous_price:

            direction = "BUY"
            confidence += 20

        else:

            direction = "SELL"
            confidence += 20

        # =====================================
        # MOMENTUM
        # =====================================

        movement = abs(last_price - previous_price)

        if movement > 0:
            confidence += 10

        return direction, confidence

    except Exception as e:

        print(f"{symbol} ERROR:", e)

        return None

# =========================================
# MAIN LOOP
# =========================================

print("AI BOT STARTED")

send_message("🚀 AI BOT STARTED")
send_message("✅ 1 MINUTE SIGNAL MODE ACTIVATED")

while True:

    for symbol in SYMBOLS:

        try:

            result = analyze_market(symbol)

            print(symbol, result)

            if result:

                direction, confidence = result

                if confidence >= CONFIDENCE_THRESHOLD:

                    message = f"""
🔥 AI SIGNAL

PAIR: {symbol}

DIRECTION: {direction}

CONFIDENCE: {confidence}%

TIMEFRAME: 1 MINUTE
"""

                    print(message)

                    send_message(message)

        except Exception as e:

            print("MAIN LOOP ERROR:", e)

    # WAIT 1 MINUTE
    time.sleep(60)