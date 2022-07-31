import time
import logging
import requests
import argparse
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# URL of the remote server
url = None


def report_file(path: str):
    """Sends file content to the designated server"""
    try:
        with open(path, "rb") as f:
            requests.post(url, files={"upload_file": f})
    except:
        logging.warning(f"Error opening and sending the modified file: {path}")


class ActionMonitorHandler(FileSystemEventHandler):
    """Logs and sends all shell files in the chosen directory."""

    def __init__(self, logger=None):
        super().__init__()

    def on_moved(self, event):
        super().on_moved(event)

    def on_created(self, event):
        super().on_created(event)

    def on_deleted(self, event):
        super().on_deleted(event)

    def on_modified(self, event):
        super().on_modified(event)

        what = "directory" if event.is_directory else "file"
        logging.info("Modified %s: %s", what, event.src_path)
        if event.src_path.endswith(".sh"):
            logging.info("About to send the file contents")
            report_file(event.src_path)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", required=True, help="Directory to monitor")
    parser.add_argument("-u", "--url", required=True, help="URL of the remote server")
    args = parser.parse_args()

    url = args.url

    if not os.path.exists(args.directory) or not os.path.isdir(args.directory):
        logging.error("The given path doesn't exist, or isn't a directory")
        exit(1)

    logging.info(f"Starting to monitor the directory: {args.directory}")
    event_handler = ActionMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, args.directory, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
