# Crypto Price Tracker

This is a cryptocurrency price tracking application built with Python that fetches live price data for multiple cryptocurrencies, compares them with user-defined thresholds, and sends notifications via Telegram and desktop notifications. It also includes a caching system to reduce unnecessary API calls by checking for configuration changes.

## Features
- Fetches cryptocurrency prices from CoinMarketCap API.
- Tracks prices of selected cryptocurrencies.
- Sends Telegram and desktop notifications when a price threshold is reached.
- Prevents duplicate alerts by enforcing a **10% incremental threshold** before triggering another alert.
- Caches configuration data with hash validation to reduce latency and avoid redundant API requests.
- Logs all alerts to a local file.

## Prerequisites
Before using this project, you need the following:
- Python 3.10 or later.
- A CoinMarketCap API Key.
- A Telegram Bot Token (for sending Telegram notifications).
- A Telegram Chat ID (for sending notifications to your personal chat).
- Access to a remote config file containing cryptocurrency symbols, price thresholds, and mute settings.

## Installation
### 1. Clone the Repository
Clone the project repository to your local machine:
```bash
git clone https://github.com/yourusername/crypto-price-tracker.git
```
### 2. Install Dependencies
Navigate to the project directory and install the required dependencies:
```bash
cd crypto-price-tracker
pip install -r requirements.txt
```
### 3. Set Up Environment Variables

You need to set up environment variables for the API key and Telegram bot information. Create a `.env` file in the root directory and add the following:
```bash
API_KEY=your_coinmarketcap_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```
### 4. Update Configuration

You can fetch configuration from an external source or use the default `config.json` file. If you want to use an external URL for the config file, modify the URL in the `fetch_config()` function.

## Usage

Once the setup is complete, you can run the script:
```bash
python crypto_price_tracker.py
```
The script will run indefinitely, fetching cryptocurrency prices every 15 minutes, checking for price changes, and sending notifications if any alerts are triggered.

### Configuration File (`config.json`)

The configuration file contains the following:

-   **crypto_symbols**: A list of cryptocurrency symbols (e.g., `BTC`, `ETH`, etc.).
-   **price_thresholds**: Defines price alert thresholds for each cryptocurrency.
-   **mute_settings**: Allows you to mute notifications for specific cryptocurrencies.

Example `config.json`:
```json
{
  "crypto_symbols": ["BTC", "ETH", "SOL", "XRP"],
  "price_thresholds": {
    "BTC": { "up": 50000, "down": 45000 },
    "ETH": { "up": 4000, "down": 3500 }
  },
  "mute_settings": {
    "SOL": true,
    "XRP": false
  }
}
```
## How It Works

-   The script fetches cryptocurrency prices every 15 minutes from the **CoinMarketCap API**.
-   It compares the fetched prices against the configured thresholds and triggers alerts if prices exceed or drop below the specified values.
-   Notifications are sent via **Telegram**.
-   **Prevents duplicate alerts** by enforcing a **10% increase/decrease rule** before sending a new notification.

## Incremental Alert System

To prevent excessive alerts, the script follows this rule:

1. If a cryptocurrency reaches the configured threshold for the **first time**, an alert is triggered.
2. A **new alert is only sent if the price increases/decreases by 10%** from the last alert price.
3. If the price goes back below the threshold and rises again, the system resets and waits for the next alert trigger.

## Cache Mechanism

-   The script uses caching to store the configuration in `config_cache.json` and its hash in `config_cache_hash.txt`.
-   It checks if the configuration has changed by comparing the hash value. If there is a change, the new configuration is fetched and stored locally.

## Telegram Notifications

Telegram notifications are sent using the Telegram Bot API. To receive these notifications, you need to create a bot via BotFather and get your **chat ID**. Then, set up the `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in your `.env` file.

## Future Improvements

-   Add more customizable alert options.
-   Integrate with other APIs for more cryptocurrency data.
-   Improve error handling for API requests.

