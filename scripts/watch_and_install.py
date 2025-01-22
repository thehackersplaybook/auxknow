import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = "../perplexer"


class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None

    def on_any_event(self, event):
        if self.process and self.process.poll() is None:
            print("Update already running, skipping...")
            return  # An update is already running
        print("Change detected, running pip install ...")
        self.process = subprocess.Popen(["pip", "install", "."])


if __name__ == "__main__":
    path = WATCH_FOLDER
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Watching for changes in {path}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Stopped watching for changes.")
