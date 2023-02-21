from pyrogram import Client, filters
import urllib.request
import datetime

app = Client(
    "my_bot",
    api_id=10816184,  # Replace with your API ID
    api_hash="54fcbe09fa0ea55509bf88bd04a9aff0",  # Replace with your API hash
    bot_token="5568157345:AAHs36IOywVMJ3RB1DOoXHLW3yO5LnOQg9k"  # Replace with your bot token
)

# Function to get the time in Kolkata in 12 hour format
def get_time():
    current_time = datetime.datetime.now(datetime.timezone.utc)
    india_time = current_time.astimezone(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    time_str = india_time.strftime("%I:%M %p")
    return time_str

@app.on_message(filters.command(["time"]))
def send_time(bot, message):
    time_str = get_time()
    bot.send_message(chat_id=message.chat.id, text=f"The time in Kolkata, India is {time_str}")

@app.on_message(filters.text & ~filters.command)
def download_and_upload(bot, message):
    # Respond to user
    bot.send_message(chat_id=message.chat.id, text="Received your message, boss")
    
    # Check if message contains a URL
    if message.entities and message.entities[0].type == "url":
        url = message.text
        file_ext = url.split(".")[-1]
        allowed_extensions = ["mp3", "mp4", "mkv", "avi", "pdf", "doc", "jpg", "jpeg", "png", "gif"]
        
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
