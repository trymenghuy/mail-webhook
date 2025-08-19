import logging
import os
from datetime import datetime

import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_telegram_message():
    """Send a single message to Telegram (for cron job)"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        logger.error("Missing Telegram credentials")
        return False
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"<b>Cron Job Test</b>\n\nHello from Render Cron! 👋\n\n<i>📅 {timestamp}</i>"
        
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info("✅ Message sent successfully")
            return True
        else:
            logger.error(f"❌ Failed: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Cron job starting...")
    success = send_telegram_message()
    logger.info("✅ Cron job completed" if success else "❌ Cron job failed")
    exit(0 if success else 1)