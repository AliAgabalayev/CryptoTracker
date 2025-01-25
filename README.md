Crypto Price Tracker
This is a cryptocurrency price tracking application built with Python that fetches live price data for multiple cryptocurrencies, compares them with user-defined thresholds, and sends notifications via Telegram and desktop notifications. It also includes a caching system to reduce unnecessary API calls by checking for configuration changes.

Features
Fetches cryptocurrency prices from CoinMarketCap API.
Tracks prices of selected cryptocurrencies.
Sends Telegram and desktop notifications when a price threshold is reached.
Caches configuration data with hash validation to reduce latency and avoid redundant API requests.
Logs all alerts to a local file.
Prerequisites
Before using this project, you need the following:

Python 3.10 or later.
A CoinMarketCap API Key.
A Telegram Bot Token (for sending Telegram notifications).
A Telegram Chat ID (for sending notifications to your personal chat).
Access to a remote config file containing cryptocurrency symbols, price thresholds, and mute settings.
Installation
1. Clone the Repository
Clone the project repository to your local machine:

bash
git clone https://github.com/yourusername/crypto-price-tracker.git
2. Install Dependencies
Navigate to the project directory and install the required Python packages:

bash
cd crypto-price-tracker
pip install -r requirements.txt
3. Set Up Environment Variables
Create a .env file or set the following environment variables:

bash
API_KEY=your_coinmarketcap_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
Alternatively, you can set the environment variables directly in your system.

4. Configure Remote File
Ensure you have a remote config file stored on an accessible URL (e.g., Google Drive, Dropbox, etc.). The file should be a JSON file containing:

crypto_symbols: List of cryptocurrency symbols (e.g., ["BTC", "ETH", "XRP"]).
price_thresholds: Price thresholds for each cryptocurrency (e.g., {"BTC": {"up": 50000, "down": 40000}}).
mute_settings: Mute settings for each cryptocurrency (e.g., {"BTC": false, "ETH": true}).
5. Run the Script
You can run the script directly:

bash
python crypto_price_tracker.py
This will start fetching the cryptocurrency prices, checking for alerts, and sending notifications.

How It Works
Fetching Config: The script checks the remote config file and loads it. If the configuration changes, it updates the local cache and hash files.
Fetching Cryptocurrency Prices: The script fetches live cryptocurrency prices using the CoinMarketCap API.
Checking Alerts: It checks the fetched prices against the configured thresholds and sends notifications (desktop or Telegram) if the price crosses any threshold.
Logging: Alerts are logged into a local alerts.log file.
Caching System
To minimize unnecessary network requests, the project uses a caching system that stores the configuration in config_cache.json and tracks the configuration file’s hash in config_cache_hash.txt. If the configuration file has changed, the system fetches the new data; otherwise, it uses the cached configuration.

Files and Directories
crypto_price_tracker.py: Main script that runs the price tracking logic.
config_cache.json: Cached configuration file.
config_cache_hash.txt: Hash file to track changes in the configuration file.
alerts.log: Logs all alerts sent by the application.
Troubleshooting
Invalid JSON Errors
If the script fails to parse the remote configuration, ensure that the URL is correct and the JSON structure is valid. You can test the URL directly in your browser or using a tool like Postman to confirm the response.

Missing Environment Variables
Ensure that all required environment variables (API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) are set correctly. You can check this by printing the values in the script to ensure they are loaded properly.

Contributing
Feel free to fork this repository and create a pull request. If you encounter any issues or have suggestions, open an issue, and I will try to address it as soon as possible.
