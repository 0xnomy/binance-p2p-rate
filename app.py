import requests
import time
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# :wrench: Your Discord Webhook URL (use environment variable for security)
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# Validate webhook URL
if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is required. Please set it in your .env file or environment.")

# :receipt: Binance P2P request payload
def get_payload(trade_type):
    return {
        "fiat": "PKR",
        "page": 1,
        "rows": 10,
        "tradeType": trade_type,
        "asset": "USDT",
        "proMerchantAds": False,
        "shieldMerchantAds": False,
        "filterType": "all",
        "publisherType": "merchant",
        "classifies": ["mass", "profession", "fiat_trade"],
        "tradedWith": False,
        "followed": False
    }

# :mag: Fetch ads, filter out featured
def fetch_ads(trade_type):
    response = requests.post(
        'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
        json=get_payload(trade_type),
        timeout=10
    )
    if response.status_code != 200:
        raise Exception(f"Binance API request failed with status {response.status_code}: {response.text}")
    all_ads = response.json().get("data", [])
    return [ad for ad in all_ads if ad.get("privilegeType") != 4]

# :art: Build embed payload with enhanced design
def build_embed(buy_ads, sell_ads):
    def format_ads(ads, trade_type):
        if not ads:
            return f"```\nNo {trade_type.lower()} offers available\n```"
        
        formatted_ads = []
        for i, ad in enumerate(ads[:5], 1):  # Limit to top 5 offers
            price = ad['adv']['price']
            nickname = ad['advertiser']['nickName']
            
            # Add verification badge if user is verified
            verified_badge = "✅" if ad['advertiser'].get('userGrade') == 1 else ""
            
            formatted_ads.append(
                f"**{nickname}** {verified_badge}\n"
                f"   💰 `{price} PKR`"
            )
        
        return "\n\n".join(formatted_ads)
    
    # Get current time in PK timezone
    current_time = datetime.now().strftime("%d %b %Y • %I:%M %p")
    
    # Calculate average prices for summary
    buy_prices = [float(ad['adv']['price']) for ad in buy_ads[:3]] if buy_ads else []
    sell_prices = [float(ad['adv']['price']) for ad in sell_ads[:3]] if sell_ads else []
    
    avg_buy = sum(buy_prices) / len(buy_prices) if buy_prices else 0
    avg_sell = sum(sell_prices) / len(sell_prices) if sell_prices else 0
    spread = avg_sell - avg_buy if avg_buy and avg_sell else 0
    
    embed = {
        "title": "**Binance P2P Fetcher for Crypto Awaz**",
        "description": f"📊 **USDT/PKR Market Rates** • Updated {current_time}",
        "color": 0x1E1E1E,  # Dark theme
        "thumbnail": {
            "url": "https://cryptologos.cc/logos/tether-usdt-logo.png"
        },
        "fields": [
            {
                "name": "📈 **Market Summary**",
                "value": f"```\n🟢 Avg Buy:  {avg_buy:.2f} PKR\n🔴 Avg Sell: {avg_sell:.2f} PKR\n📊 Spread:   {spread:.2f} PKR\n```",
                "inline": False
            },
            {
                "name": "🟢 **Top Buy Offers**",
                "value": format_ads(buy_ads, "BUY"),
                "inline": True
            },
            {
                "name": "🔴 **Top Sell Offers**", 
                "value": format_ads(sell_ads, "SELL"),
                "inline": True
            },
            {
                "name": "ℹ️ **Market Info**",
                "value": "```\nAsset: USDT/Tether\nExchange: Binance P2P\nFiat: Pakistani Rupee\n```",
                "inline": False
            }
        ],
        "footer": {
            "text": "🌐 cryptoawaz.com",
            "icon_url": "https://cryptologos.cc/logos/binance-coin-bnb-logo.png"
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return {"embeds": [embed]}

# :outbox_tray: Send embed to Discord
def send_embed(payload):
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

# :rocket: Main execution
if __name__ == "__main__":
    try:
        buy_ads = fetch_ads("BUY")
        sell_ads = fetch_ads("SELL")
        embed = build_embed(buy_ads, sell_ads)
        send_embed(embed)
        print("✅ Sent enhanced P2P dashboard to Discord")
    except Exception as e:
        print(f"❌ Error: {e}")
        error_embed = {
            "embeds": [{
                "title": "⚠️ **P2P Dashboard Error**",
                "description": f"Failed to fetch Binance P2P rates\n\n**Error:** {str(e)}",
                "color": 0xFF6B6B,
                "footer": {
                    "text": "🌐 cryptoawaz.com"
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }]
        }
        send_embed(error_embed)