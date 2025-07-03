# Binance P2P Fetcher for Crypto Awaz

A Python script that fetches real-time Binance P2P trading rates for USDT/PKR and sends them to Discord via webhook. This tool provides a clean, professional dashboard showing current buy/sell offers, market summary, and spread calculations.

## ✨ Features

- **Real-time Data**: Fetches live USDT/PKR rates from Binance P2P
- **Professional Dashboard**: Beautiful Discord embed with market summary
- **Top 5 Offers**: Shows best buy and sell offers with trader verification badges
- **Market Analysis**: Displays average buy/sell prices and spread
- **Error Handling**: Robust error handling with timeout protection
- **Clean Formatting**: Professional presentation with emojis and structured layout

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- `requests` library
- Discord webhook URL

### Installation

1. **Clone or download the project**
   ```bash
   git clone https://github.com/0xnomy/binance-p2p-rate)
   cd binance-p2p-rate
   ```

2. **Install dependencies**
   ```bash
   pip install requests
   ```

3. **Configure your Discord webhook**
   - Go to your Discord server settings
   - Navigate to Integrations → Webhooks
   - Create a new webhook or use an existing one
   - Copy the webhook URL

4. **Update the webhook URL**
   - Open `app.py`
   - Replace the `DISCORD_WEBHOOK_URL` with your own webhook URL:
   ```python
   DISCORD_WEBHOOK_URL = 'YOUR_WEBHOOK_URL_HERE'
   ```

5. **Run the script**
   ```bash
   python app.py
   ```

## 📊 What You'll See

The script sends a professional Discord embed containing:

- **Market Summary**: Average buy/sell prices and spread
- **Top Buy Offers**: 5 best buy offers with trader names and verification badges
- **Top Sell Offers**: 5 best sell offers with trader names and verification badges
- **Market Info**: Asset, exchange, and fiat currency details
- **Timestamp**: Current UTC time

## ⚙️ Customization

### Change Trading Pair
To fetch different trading pairs, modify the `get_payload` function:

```python
def get_payload(trade_type):
    return {
        "fiat": "PKR",        # Change to your desired fiat
        "asset": "USDT",      # Change to your desired crypto
        # ... other parameters
    }
```

### Modify Number of Offers
Change the number of offers displayed by modifying the slice in `format_ads`:

```python
for i, ad in enumerate(ads[:5], 1):  # Change 5 to desired number
```

### Update Branding
- Change the title in the `build_embed` function
- Modify the footer text and icon URL
- Update the thumbnail URL

## 🔧 Technical Details

### API Endpoint
- **URL**: `https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search`
- **Method**: POST
- **Timeout**: 10 seconds
- **Error Handling**: Automatic retry with clear error messages

### Data Filtering
- Excludes featured/privileged ads (privilegeType != 4)
- Shows only merchant ads
- Filters by mass, profession, and fiat trade classifications

## 🛠️ Troubleshooting

### Common Issues

1. **Webhook URL Invalid**
   - Ensure your webhook URL is correct and active
   - Check if the webhook has proper permissions

2. **Network Timeout**
   - The script has a 10-second timeout for API calls
   - Check your internet connection
   - Verify Binance P2P API is accessible

3. **No Data Returned**
   - Check if there are active P2P offers for USDT/PKR
   - Verify the API response format hasn't changed

### Error Messages
- The script will send error embeds to Discord if something goes wrong
- Check the console output for detailed error information

## 📝 Usage Examples

### Single Execution
```bash
python app.py
```
Sends current rates once and exits.

### Scheduled Execution
You can set up a cron job or task scheduler to run the script periodically:

```bash
# Run every 10 minutes
*/10 * * * * /usr/bin/python3 /path/to/app.py
```

## 🤝 Contributing

This project was created for Crypto Awaz. Feel free to fork and modify for your own use, but please:

- Use your own Discord webhook
- Respect Binance API rate limits
- Test thoroughly before deployment

## 📄 License

This project is provided as-is for educational and personal use. Please ensure compliance with Binance's terms of service and Discord's developer policies.

## 🔗 Links

- [Binance P2P](https://p2p.binance.com/)
- [Crypto Awaz](https://cryptoawaz.com)

---

**Made for crypto awaz** 
