import platform
import time
import os
import requests
from plyer import notification  # Desktop notifications

API_KEY = os.getenv("API_KEY")
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

CRYPTO_SYMBOLS = ["BTC", "ETH", "SOL", "TRUMP", "XRP", "ENA", "HBAR", "WLD"]

price_thresholds = {
    "BTC": {"up": 110000, "down": 99000},
    "ETH": {"up": 4000, "down": 3000},
    "SOL": {"up": 260, "down": 220},
    "TRUMP": {"up": 50, "down": 20},
    "XRP": {"up": 3.4, "down": 3},
    "ENA": {"up": 0.92, "down": 0.75},
    "HBAR": {"up": 0.39, "down": 0},
    "WLD": {"up": 2.3, "down": 2}
}

# User-specific Telegram bot settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Track previously sent alerts to avoid duplicates
alert_history = {}


mute_settings = {
    "BTC": False,
    "ETH": False,
    "SOL": False,
    "TRUMP": False,
    "XRP": False,
    "ENA": False,
    "HBAR": False,
    "WLD": True
}


def get_crypto_prices():
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    params = {"symbol": ",".join(CRYPTO_SYMBOLS), "convert": "USD"}
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def send_desktop_notification(title, message):
    notification.notify(title=title, message=message, timeout=10)



def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print(f"Telegram Error: {response.status_code}, {response.text}")


def check_alerts(data):
    global alert_history
    alerts = []

    for symbol, info in data.items():
        price = round(info["quote"]["USD"]["price"], 2)

        if price >= price_thresholds[symbol]["up"] and alert_history.get(symbol) != "up":
            alerts.append(f"ALERT: {symbol} price has risen to {price} USD!")
            alert_history[symbol] = "up"
        elif price <= price_thresholds[symbol]["down"] and alert_history.get(symbol) != "down":
            alerts.append(f"ALERT: {symbol} price has dropped to {price} USD!")
            alert_history[symbol] = "down"

    return alerts


def log_alerts(alerts):
    with open("alerts.log", "a") as log_file:
        for alert in alerts:
            log_file.write(alert + "\n")


def main():
    while True:
        print("Fetching cryptocurrency prices...")
        crypto_data = get_crypto_prices()

        if crypto_data:
            alerts = check_alerts(crypto_data)
            if alerts:
                for alert in alerts:
                    symbol = alert.split()[1]
                    if not mute_settings.get(symbol, False):
                        '''send_desktop_notification("Crypto Alert", alert)'''
                        send_telegram_notification(alert)
                log_alerts(alerts)

        print("Waiting for the next update...")
        time.sleep(900)


if __name__ == "__main__":
    main()
