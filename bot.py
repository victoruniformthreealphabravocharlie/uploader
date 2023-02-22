import pyrogram
import requests
import os
import time


def download_progress(url, file_name, message):
    with open(file_name, "wb") as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get("content-length")

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            start_time = time.time()
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                downloaded_mb = round(dl / (1024 * 1024), 2)
                total_mb = round(total_length / (1024 * 1024), 2)
                speed = round(dl / (1024 * 1024 * (time.time() - start_time) + 0.001), 2)
                progress = "[" + "=" * done + " " * (50 - done) + "]"
                percentage = round(dl / total_length * 100, 2)
                message.edit_text(f"Downloading {file_name} {progress} {percentage}% {downloaded_mb}MB/{total_mb}MB ({speed}MB/s)")

    return file_name


app = pyrogram.Client("zyrup_bot", api_id=10816184, api_hash="54fcbe09fa0ea55509bf88bd04a9aff0", bot_token="5528793402:AAEJ0hz_f6rYVUHwZuUCgJGQYCV4MOBQhsw")

my_username = "synzc"


@app.on_message(pyrogram.filters.command("start"))
def start(client, message):
    message.reply_text("Hello! Send me a direct download link of a file and I'll upload it to Telegram for you.")

@app.on_message(pyrogram.filters.command("about"))
def about(client, message):
    message.reply_text("You can send me a direct download link of a file and I'll download and upload it for you here. I'm a bot developed solely by @synzc")

@app.on_message(pyrogram.filters.command("status"))
def start(client, message):
    message.reply_text("I'm online and runnning.."))

@app.on_message(pyrogram.filters.command("help"))
def start(client, message):
    message.reply_text("/start, /help, /about, /status"))
 

@app.on_message(pyrogram.filters.text)
def download(client, message):
    url = message.text
    if url.endswith((".mp3", ".mp4", ".mkv", ".avi", ".pdf", ".doc", ".jpg", ".jpeg", ".png", ".gif")):
        file_name = url.split("/")[-1]
        sent_message = message.reply_text("Received your message. Starting to download now...")
        file_path = download_progress(url, file_name, sent_message)
        sent_message.edit_text(f"Starting to upload {file_name} now...")
        client.send_document(message.chat.id, file_path, caption=f"Here's your file: {file_name}")
        os.remove(file_path)
        sent_message.edit_text(f"Uploaded {file_name} successfully!! Deleted the file from server now.")
    else:
        message.reply_text("Sorry, send me a direct download link only of these files! ((.mp3, .mp4, .mkv, .avi, .pdf, .doc, .jpg, .jpeg, .png, .gif))")


app.run()
