import requests
import yfinance as yf
import time

# =========================
# TELEGRAM SETTINGS
# =========================

BOT_TOKEN = "8729139885:AAEdK7DAoWK8O1cTkD5h7KTgPNDx2V_DFmw"
CHAT_ID = "451786776"

# =========================
# SETTINGS
# =========================

SYMBOLS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X"
]

TIMEFRAME = "5m"

# =========================
# SEND TELEGRAM MESSAGE
# =========================

def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# =========================
# SIMPLE EMA
# =========================

def ema(values, period):

    multiplier = 2 / (period + 1)

    ema_value = values[0]

    for price in values[1:]:
        ema_value = (price - ema_value) * multiplier + ema_value

    return ema_value

# =========================
# RSI
# =========================

def calculate_rsi(closes, period=14):

    gains = []
    losses = []

    for i in range(1, len(closes)):

        diff = closes[i] - closes[i - 1]

        if diff >= 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains[-period:]) / period if gains else 0.1
    avg_loss = sum(losses[-period:]) / period if losses else 0.1

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

# =========================
# MARKET ANALYSIS
# =========================

def analyze_market(symbol):

    data = yf.download(
        symbol,
        period="1d",
        interval=TIMEFRAME
    )

    closes = list(data["Close"])

    if len(closes) < 30:
        return None

    ema_fast = ema(closes[-10:], 9)
    ema_slow = ema(closes[-22:], 21)

    rsi = calculate_rsi(closes)

    direction = None
    confidence = 0

    # EMA TREND
    if ema_fast > ema_slow:
        direction = "BUY"
        confidence += 50

    elif ema_fast < ema_slow:
        direction = "SELL"
        confidence += 50

    # RSI FILTER
    if direction == "BUY" and rsi < 70:
        confidence += 30

    elif direction == "SELL" and rsi > 30:
        confidence += 30

    # CANDLE CONFIRMATION
    if closes[-1] > closes[-2] and direction == "BUY":
        confidence += 20

    elif closes[-1] < closes[-2] and direction == "SELL":
        confidence += 20

    return direction, confidence

# =========================
# MAIN LOOP
# =========================

print("AI BOT STARTED")

send_message("🚀 AI BOT STARTED")

while True:

    for symbol in SYMBOLS:

        try:

            result = analyze_market(symbol)

            if result:

                direction, confidence = result

                if confidence >= 70:

                    message = f'''
🔥 AI SIGNAL

PAIR: {symbol}

DIRECTION: {direction}

CONFIDENCE: {confidence}%

TIMEFRAME: 5 MINUTES
'''

                    print(message)

                    send_message(message)

        except Exception as e:
            print("ERROR:", e)

    time.sleep(300)