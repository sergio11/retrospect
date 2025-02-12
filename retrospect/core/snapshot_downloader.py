import requests
import os
from datetime import datetime
from retrospect.utils.logger import appLogger

class SnapshotDownloader:
    """
    The SnapshotDownloader class is responsible for downloading historical snapshots from the Wayback Machine 
    and saving them to a specified local directory. The snapshots are saved as HTML files, with filenames that 
    include timestamps to ensure uniqueness.

    Attributes:
        user_agent (str): The user-agent string to be used in HTTP requests for downloading the snapshots.
    """

    def __init__(self, user_agent: str):
        """
        Initializes the SnapshotDownloader with the specified user-agent string. This allows the downloader 
        to make HTTP requests to the Wayback Machine with the provided user-agent for proper interaction.

        Args:
            user_agent (str): The user-agent string used in HTTP requests to download snapshots.
        """
        self.user_agent = user_agent

    def download_snapshot(self, archive_url: str, directory: str):
        """
        Downloads the content of a snapshot from the Wayback Machine and saves it as an HTML file in the specified 
        directory. The file is named using a timestamp to ensure uniqueness.

        Args:
            archive_url (str): The URL of the Wayback Machine snapshot to be downloaded.
            directory (str): The directory path where the snapshot file should be saved.

        Raises:
            Exception: If the snapshot cannot be downloaded due to network issues or invalid response.
        
        Steps:
            1. Checks if the provided directory exists.
            2. Sends an HTTP GET request to the Wayback Machine snapshot URL.
            3. If successful, creates the directory (if necessary) and writes the snapshot content to a file.
            4. If there is an error during the process, logs it.
        """
        try:
            # Validate if the provided path is a directory
            if not os.path.isdir(directory):
                appLogger.error(f"❌ The specified path is not a directory: {directory}")
                return

            # Generate a timestamped filename for the snapshot
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = os.path.join(directory, f"snapshot_{timestamp}.html")

            # Send a GET request to the Wayback Machine snapshot URL
            response = requests.get(archive_url, headers={"User-Agent": self.user_agent})

            # If the response is successful, save the snapshot content
            if response.status_code == 200:
                os.makedirs(directory, exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                appLogger.info(f"📥 Snapshot downloaded successfully to {filename}")
            else:
                appLogger.error(f"❌ Failed to retrieve snapshot. HTTP Status Code: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            # Catch any request-related exception and log the error
            appLogger.error(f"❌ Failed to download snapshot from {archive_url}. Error: {e}")