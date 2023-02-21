import pyrogram
import urllib.request
import datetime
import os

app = pyrogram.Client(
    "my_bot",
    api_id="YOUR_API_ID",
    api_hash="YOUR_API_HASH",
    bot_token="YOUR_BOT_TOKEN"
)


@app.on_message(pyrogram.filters.command("time"))
def get_time(client, message):
    # Get the current time in Kolkata, India
    time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%I:%M %p")
    
    # Reply to the user with the current time
    message.reply(f"The current time in Kolkata is {time}")

@app.on_message(pyrogram.filters.text & ~pyrogram.filters.command)
def download_and_upload(client, message):
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
                client.send_document(
                    chat_id=message.chat.id,
                    document=file_name,
                    caption=f"Here's your {file_ext} file!"
                )
                
                # Delete the downloaded file
                os.remove(file_name)
            except Exception as e:
                print(f"Error downloading or uploading file: {e}")
        else:
            message.reply_text(
                f"Invalid file type. Only files with extensions: {', '.join(allowed_extensions)} are allowed."
            )

    # Send a response to the user
    message.reply_text("Received your message, boss!")


app.run()
