import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os

bot_token = '6261956816:AAEToEEo4_aRRMeRi2qPnnTUoQJn3uYHnI8'
bot = telegram.Bot(token=bot_token)


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Hello! Send me a direct download link and I will upload the file to this chat.')


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)
    return local_filename


def upload_file(file_path, chat_id):
    bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
    os.remove(file_path)


def handle_message(update, context):
    chat_id = update.message.chat_id
    url = update.message.text
    try:
        filename = download_file(url)
        upload_file(filename, chat_id)
        context.bot.send_message(chat_id=chat_id, text='File uploaded successfully!')
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text='Error: {}'.format(e))


if __name__ == '__main__':
    updater = Updater(bot_token, use_context=False)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()
