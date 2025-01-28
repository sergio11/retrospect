import requests
import os
from datetime import datetime
from retrospect.utils.logger import appLogger

class SnapshotDownloader:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def download_snapshot(self, archive_url: str, directory: str):
        """
        Download the content of a Wayback Machine snapshot and save it to a file.

        Args:
            archive_url (str): URL of the snapshot on Wayback Machine.
            directory (str): Directory where the snapshot will be saved.
        """
        try:
            if not os.path.isdir(directory):
                appLogger.error(f"❌ The specified path is not a directory: {directory}")
                return
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = os.path.join(directory, f"snapshot_{timestamp}.html")
            response = requests.get(archive_url, headers={"User-Agent": self.user_agent})
            if response.status_code == 200:
                os.makedirs(directory, exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(response.text)
        except requests.exceptions.RequestException as e:
            # Catch any exception that occurs during the request
            appLogger.error(f"❌ Failed to download snapshot from {archive_url}. Error: {e}")