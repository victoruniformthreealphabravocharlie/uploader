import telegram
import requests

# Set up your Telegram bot API token and chat ID
bot = telegram.Bot('6261956816:AAEToEEo4_aRRMeRi2qPnnTUoQJn3uYHnI8')
chat_id = '-669803670'

def download_and_upload_file(url):
    """Download a file from a URL and upload it to Telegram"""
    # Get the file name from the URL
    file_name = url.split('/')[-1]
    # Send a message to the user that the bot is downloading the file
    bot.send_message(chat_id=chat_id, text=f'Downloading {file_name}...')
    # Download the file from the URL
    response = requests.get(url)
    # Upload the file to Telegram
    if file_name.endswith('.mp3'):
        bot.send_audio(chat_id=chat_id, audio=response.content, filename=file_name)
    elif file_name.endswith('.mp4') or file_name.endswith('.mkv'):
        bot.send_video(chat_id=chat_id, video=response.content, filename=file_name)
    elif file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
        bot.send_photo(chat_id=chat_id, photo=response.content, filename=file_name)
    elif file_name.endswith('.doc') or file_name.endswith('.pdf'):
        bot.send_document(chat_id=chat_id, document=response.content, filename=file_name)
    else:
        bot.send_message(chat_id=chat_id, text=f'Unsupported file type: {file_name}')
    # Send a message to the user that the file has been uploaded
    bot.send_message(chat_id=chat_id, text=f'{file_name} has been uploaded to Telegram!')

# Define the function to handle incoming messages
def handle_message(update, context):
    """Handle an incoming message"""
    # Get the message text and chat ID
    message_text = update.message.text
    chat_id = update.message.chat_id
    # Check if the message contains a valid URL
    if message_text.startswith('http') and any(extension in message_text for extension in ['.mp3', '.mp4', '.mkv', '.jpg', '.jpeg', '.png', '.doc', '.pdf']):
        # Download and upload the file
        download_and_upload_file(message_text)
    else:
        # Send a message to the user that the URL is not valid
        bot.send_message(chat_id=chat_id, text='Please send a valid direct download link for a supported file type.')

# Set up the message handler
updater = telegram.ext.Updater('6261956816:AAEToEEo4_aRRMeRi2qPnnTUoQJn3uYHnI8', use_context=True)
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

# Start the bot
updater.start_polling()
updater.idle()
