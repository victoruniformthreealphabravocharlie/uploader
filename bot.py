from pyrogram import Client, filters
import pytz
from datetime import datetime

# create a new Pyrogram client instance
app = Client(
    "my_bot",
    api_id=123456,
    api_hash="0123456789abcdef0123456789abcdef",
    bot_token="1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
)

# handler function for the /time command
@app.on_message(filters.command("time"))
def time_command_handler(client, message):
    # get the current time in Kolkata, India
    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(tz)

    # format the time as 12-hour time
    time_str = current_time.strftime("%I:%M %p")

    # send the time back to the user
    client.send_message(chat_id=message.chat.id, text=f"The current time in Kolkata is {time_str}")

# start the bot
app.run()
