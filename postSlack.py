import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Slackの設定
SLACK_TOKEN = ''
SLACK_CHANNEL = ''

client = WebClient(token=SLACK_TOKEN)

class Watcher:
    DIRECTORY_TO_WATCH = "C:\\test\\"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        else:
            # ファイルが作成されたときに実行される処理

            fname = event.src_path.split("\\")[-1]

            try:
                response = client.chat_postMessage(
                    channel=SLACK_CHANNEL,
                    text=f"3Dプリントが開始されました : {fname}"
                )
            except SlackApiError as e:
                print(f"Slack API Error: {e.response['error']}")

if __name__ == '__main__':
    w = Watcher()
    w.run()
