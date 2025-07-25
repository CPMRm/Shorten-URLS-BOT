import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 替换为你的Telegram Bot API令牌
TELEGRAM_BOT_TOKEN = os.getenv('8275608088:AAFvAH-0koZJWI7ZYCLWMjwD4idXXLQRLF0')

# 替换为你的Bitly API访问令牌
BITLY_ACCESS_TOKEN = os.getenv('cf963a04d292c02f8b523088ff31f2124330cadd')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('歡迎使用網址縮短機器人！請發送一個網址给我，我將為你缩短它。')

def shorten_url(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    headers = {
        'Authorization': f'Bearer {BITLY_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    data = {'long_url': url}
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, json=data)

    if response.status_code == 200:
        shortened_url = response.json().get('link')
        update.message.reply_text(f'缩短後的網址是：{shortened_url}')
    else:
        update.message.reply_text('抱歉，缩短網址時出錯。')

def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, shorten_url))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    