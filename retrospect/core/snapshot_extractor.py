import os
from bs4 import BeautifulSoup
from retrospect.utils.logger import appLogger

class SnapshotExtractor:
    def __init__(self, directory: str):
        """
        Initializes the SnapshotExtractor with the given directory containing .html snapshots.

        Args:
            directory (str): Path to the folder containing snapshots.
        """
        self.directory = directory
        self.output_file = os.path.join(directory, "unified_snapshots.txt")
        appLogger.info(f"📂 [INIT] SnapshotExtractor initialized for directory: {directory}")

    def _extract_text_from_html(self, file_path: str) -> str:
        """
        Parses an HTML file and extracts meaningful text and metadata.

        Args:
            file_path (str): Path to the HTML snapshot.

        Returns:
            str: Cleaned text and relevant metadata extracted from the HTML.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

            # Removing scripts, styles, and extracting visible text
            for script in soup(["script", "style"]):
                script.extract()

            # Extracting text
            text = soup.get_text(separator=" ")
            text = ' '.join(text.split())  # Remove excessive whitespace

            # Extracting links
            links = [a['href'] for a in soup.find_all('a', href=True)]

            # Extracting images and alt attributes
            images = [img['alt'] for img in soup.find_all('img', alt=True)]

            # Extracting metadata (title, description)
            title = soup.title.string if soup.title else 'No title'
            description = soup.find('meta', attrs={'name': 'description'})
            description_content = description['content'] if description else 'No description'

            # Combine everything into a structured format
            snapshot_info = (
                f"##### Snapshot: {file_path} #####\n\n"
                f"Title: {title}\n"
                f"Description: {description_content}\n"
                f"Links: {', '.join(links)}\n"
                f"Image Alt Texts: {', '.join(images)}\n"
                f"Extracted Text: {text}\n"
            )

            return snapshot_info

        except Exception as e:
            appLogger.error(f"❌ [ERROR] Failed to process {file_path}: {e}")
            return ""

    def process_snapshots(self):
        """
        Iterates through all .html files in the directory, extracts text, links, images, and metadata,
        and creates a unified text file.
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