import pyrogram
import requests
import os
import time


def download_progress(url, file_name):
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
                message = f"Downloading {file_name} {progress} {percentage}% {downloaded_mb}MB/{total_mb}MB ({speed}MB/s)"
                print(message)

    return file_name


app = pyrogram.Client("zyrup_bot", api_id=10816184, api_hash="54fcbe09fa0ea55509bf88bd04a9aff0", bot_token="5568157345:AAHs36IOywVMJ3RB1DOoXHLW3yO5LnOQg9k")


@app.on_message(pyrogram.filters.command("start"))
def start(client, message):
    message.reply_text("Hello! Send me a direct download link of a file and I'll upload it to Telegram for you.")


@app.on_message(pyrogram.filters.text & ~pyrogram.filters.command)
def download(client, message):
    url = message.text
    if url.endswith((".mp3", ".mp4", ".mkv", ".avi", ".pdf", ".doc", ".jpg", ".jpeg", ".png", ".gif")):
        file_name = url.split("/")[-1]
        message.reply_text("Received your message, boss. Downloading...")
        file_path = download_progress(url, file_name)
        message.reply_text(f"Uploading {file_name}...")
        client.send_document(message.chat.id, file_path, caption=f"Here's your file: {file_name}")
        os.remove(file_path)
        message.reply_text(f"Done! Deleted {file_name} from the server.")
    else:
        message.reply_text("Sorry, I only support downloading these file formats: .mp3, .mp4, .mkv, .avi, .pdf, .doc, .jpg, .jpeg, .png, .gif")


app.run()
