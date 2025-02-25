import os
from bs4 import BeautifulSoup
from retrospect.utils.logger import appLogger

class SnapshotExtractor:
    """
    Extracts text and metadata from HTML snapshots stored in a directory.

    This class is responsible for parsing downloaded HTML snapshots, removing unnecessary elements,
    extracting relevant textual content and metadata, and consolidating the extracted data into a single file.
    """

    def __init__(self, directory: str):
        """
        Initializes the SnapshotExtractor with the given directory containing .html snapshots.

        Args:
            directory (str): Path to the folder containing snapshot files.

        Attributes:
            directory (str): The directory containing the snapshot files.
            output_file (str): Path to the file where extracted content will be saved.
        """
        self.directory = directory
        self.output_file = os.path.join(directory, "unified_snapshots.txt")
        appLogger.info(f"📂 [INIT] SnapshotExtractor initialized for directory: {directory}")

    def _extract_text_from_html(self, file_path: str) -> str:
        """
        Parses an HTML file to extract meaningful text and metadata.

        This method loads the HTML content, removes unnecessary elements (scripts, styles),
        and extracts visible text along with metadata such as the page title and description.

        Args:
            file_path (str): Path to the HTML snapshot.

        Returns:
            str: A formatted string containing the extracted title, description, and cleaned text content.

        Logs:
            - Debug: Indicates which file is currently being processed.
            - Error: Captures and logs any issues encountered while processing the file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

            # Removing scripts, styles, and extracting visible text
            for script in soup(["script", "style"]):
                script.extract()

            # Extracting visible text
            text = soup.get_text(separator=" ")
            text = ' '.join(text.split())  # Remove excessive whitespace

            # Extracting metadata (title, description)
            title = soup.title.string if soup.title else 'No title'
            description = soup.find('meta', attrs={'name': 'description'})
            description_content = description['content'] if description else 'No description'

            snapshot_info = (
                f"Title: {title}\n"
                f"Description: {description_content}\n"
                f"Extracted Text: {text}\n"
            )

            return snapshot_info

        except Exception as e:
            appLogger.error(f"❌ [ERROR] Failed to process {file_path}: {e}")
            return ""

    def process_snapshots(self):
        """
        Iterates through all .html files in the directory, extracts text and metadata,
        and consolidates the data into a unified text file.

        This method scans the target directory for HTML files, processes each file,
        and writes the extracted content into a single output file.

        Logs:
            - Info: Indicates the start of the snapshot processing.
            - Debug: Logs each file being processed.
            - Info: Confirms successful extraction and saving of results.
            - Warning: Alerts if no snapshots were processed.
        """
        appLogger.info(f"🔍 [PROCESSING] Extracting text and metadata from snapshots in {self.directory}")

        snapshot_data = []
        for file in os.listdir(self.directory):
            if file.endswith(".html"):
                file_path = os.path.join(self.directory, file)
                appLogger.debug(f"📜 [EXTRACT] Processing {file_path}")
                
                snapshot_info = self._extract_text_from_html(file_path)
                if snapshot_info:
                    snapshot_data.append(snapshot_info)

        if snapshot_data:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(snapshot_data))

            appLogger.info(f"✅ [DONE] Unified snapshot data saved to {self.output_file}")
        else:
            appLogger.warning(f"⚠️ [WARNING] No snapshots were processed.")