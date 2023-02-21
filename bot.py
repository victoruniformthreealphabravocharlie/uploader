from pyrogram import Client, filters
import urllib.request

app = Client(
    "my_bot",
    api_id=10816184,
    api_hash="54fcbe09fa0ea55509bf88bd04a9aff0",
    bot_token="6261956816:AAEToEEo4_aRRMeRi2qPnnTUoQJn3uYHnI8"
)

@app.on_message(filters.private)
def download_and_upload(bot, message):
    # Check if message contains a URL
    if message.entities and message.entities[0].type == "url":
        url = message.text
        file_ext = url.split(".")[-1]
        allowed_extensions = ["mp3", "mp4", "mkv", "jpg", "doc", "pdf", "png", "jpeg"]
        
        # Check if URL points to a valid file
        if file_ext in allowed_extensions:
            try:
                # Download file from URL
                file_name, _ = urllib.request.urlretrieve(url)
                
                # Upload file to Telegram
                bot.send_document(
                    chat_id=message.chat.id,
                    document=file_name,
                    caption=f"Here's your {file_ext} file!"
                )
            except Exception as e:
                print(f"Error downloading or uploading file: {e}")
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="Invalid file type. Only files with extensions: " + ", ".join(allowed_extensions) + " are allowed."
            )

app.run()
