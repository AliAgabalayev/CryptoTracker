import hashlib
import json
import os
import time

import requests

API_KEY = os.getenv("API_KEY")
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

CACHE_FILE = "config_cache.json"
CACHE_HASH_FILE = "config_cache_hash.txt"

ALERT_STATE_FILE = "alert_state.json"
ALERT_PERCENTAGE = 0.10

FILE_ID = os.getenv('FILE_ID')
config = {}


# Function to fetch config from a remote location (e.g., cloud storage or external URL)
def fetch_config():
    config_url = f"https://drive.google.com/uc?id={FILE_ID}&export=download"
    response = requests.get(config_url)
    if response.status_code == 200:
        try:
            json_data = response.json()  # Try parsing as JSON
            return json_data, response.text
        except requests.exceptions.JSONDecodeError:
            print("Error: Response is not valid JSON.")
            return None, None
    else:
        print(f"Error fetching config: {response.status_code}")
        return None, None


# Function to calculate a hash of the content to detect changes
def calculate_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


# Function to load the config either from cache or fetch it remotely
def load_config():
    global config

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            cached_config = json.load(file)

        if os.path.exists(CACHE_HASH_FILE):
            with open(CACHE_HASH_FILE, 'r') as hash_file:
                cached_hash = hash_file.read().strip()
        else:
            cached_hash = None

        remote_config, remote_raw_content = fetch_config()

        if remote_config and cached_hash != calculate_hash(remote_raw_content):
            config = remote_config
            with open(CACHE_FILE, 'w') as file:
                json.dump(config, file)
            with open(CACHE_HASH_FILE, 'w') as hash_file:
                hash_file.write(calculate_hash(remote_raw_content))
            print("Config updated from remote source (cache updated).")
            return

        config = cached_config
        print("Loaded config from cache (no changes detected).")
        return

    remote_config, remote_raw_content = fetch_config()
    if remote_config:
        config = remote_config
        with open(CACHE_FILE, 'w') as file:
            json.dump(config, file)
        with open(CACHE_HASH_FILE, 'w') as hash_file:
            hash_file.write(calculate_hash(remote_raw_content))
        print("Config loaded and cached for the first time.")


# Function to get crypto prices
def get_crypto_prices():
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    params = {"symbol": ",".join(config["crypto_symbols"]), "convert": "USD"}
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["data"]
    elif response.status_code == 429:
        print("Rate limited. Retrying in 60 seconds...")
        time.sleep(60)
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


# Function to load previous alert states
def load_alert_state():
    if not os.path.exists(ALERT_STATE_FILE):
        return {}

    try:
        with open(ALERT_STATE_FILE, "r") as file:
            content = file.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        print("Error: alerts_state.json is corrupted. Resetting state.")
        return {}


def save_alert_state(state):
    with open(ALERT_STATE_FILE, "w") as file:
        json.dump(state, file, indent=4)


# Function to send Telegram notifications
def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    payload = {"chat_id": os.getenv("TELEGRAM_CHAT_ID"), "text": message}
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print(f"Telegram Error: {response.status_code}, {response.text}")


# Function to check alerts based on config data
def check_alerts(data):
    global config, ALERT_PERCENTAGE
    alerts = []
    alert_state = load_alert_state()

    for symbol, info in data.items():
        price = round(info["quote"]["USD"]["price"], 2)

        if symbol not in config["price_thresholds"]:
            continue  # Skip if no threshold is defined for this symbol

        up_threshold = config["price_thresholds"][symbol].get("up")
        down_threshold = config["price_thresholds"][symbol].get("down")

        # Load the last state for this symbol
        last_alert_info = alert_state.get(symbol, {})
        last_alert_type = last_alert_info.get("type")
        last_alert_price = last_alert_info.get("price", 0)

        # Check for upward threshold alerts
        if up_threshold and price >= up_threshold:
            if last_alert_type != "up":
                # First time crossing the threshold
                alerts.append(f"ALERT 🚀: {symbol} price has risen to {price} USD!")
                alert_state[symbol] = {"type": "up", "price": price}
            elif price >= last_alert_price * (1 + ALERT_PERCENTAGE):
                # Price increased significantly after last alert
                alerts.append(f"ALERT 📈: {symbol} price has jumped by {ALERT_PERCENTAGE * 100}% to {price} USD!")
                alert_state[symbol]["price"] = price  # Update last alert price

        # Check for downward threshold alerts
        elif down_threshold and price <= down_threshold:
            if last_alert_type != "down":
                # First time crossing downward threshold
                alerts.append(f"ALERT 🔻: {symbol} price has dropped to {price} USD!")
                alert_state[symbol] = {"type": "down", "price": price}
            elif price <= last_alert_price * (1 - ALERT_PERCENTAGE):
                # Price dropped significantly after last alert
                alerts.append(f"ALERT 📉: {symbol} price has fallen by {ALERT_PERCENTAGE * 100}% to {price} USD!")
                alert_state[symbol]["price"] = price  # Update last alert price

        # If the price stabilizes within a normal range, reset alert state
        else:
            if symbol in alert_state:
                del alert_state[symbol]

    # Save updated alert state
    save_alert_state(alert_state)

    return alerts


# Function to log alerts to a file
def log_alerts(alerts):
    with open("alerts_log.txt", "a", encoding="utf-8") as log_file:
        for alert in alerts:
            log_file.write(alert + "\n")


# Main function that runs the script
def main():
    load_config()

    while True:
        print("Fetching cryptocurrency prices...")
        crypto_data = get_crypto_prices()

        if crypto_data:
            alerts = check_alerts(crypto_data)
            if alerts:
                for alert in alerts:
                    symbol = alert.split()[1]
                    if not config["mute_settings"].get(symbol, False):
                        send_telegram_notification(alert)
                log_alerts(alerts)

        print("Waiting for the next update...")
        time.sleep(900)


if __name__ == "__main__":
    main()
