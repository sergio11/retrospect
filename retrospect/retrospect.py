import requests
from datetime import datetime, timedelta
from waybackpy import WaybackMachineCDXServerAPI
from retrospect.utils.logger import appLogger

class Retrospect:
    """
    Class to search and retrieve historical snapshots of web pages using the Wayback Machine API.

    Attributes:
        url (str): URL of the website to search for its previous versions.
        user_agent (str): User agent string used for HTTP requests.
    """
    
    def __init__(self, url: str, user_agent: str):
        """
        Initializes the class with the URL and the user agent.

        Args:
            url (str): URL of the website to search for.
            user_agent (str): User agent for making requests.
        """
        self.url = url
        self.user_agent = user_agent
        appLogger.info(f"🔎 Initialized Retrospect for URL: {self.url} using user-agent: {self.user_agent}")

    def _get_target_date(self, years_ago: int) -> datetime:
        """
        Calculate the target date based on how many years ago from today.

        Args:
            years_ago (int): Number of years ago from today to calculate the target date.

        Returns:
            datetime: The target date for snapshot search.
        """
        target_date = datetime.now() - timedelta(days=365 * years_ago)
        appLogger.debug(f"📅 Target date calculated: {target_date.strftime('%Y-%m-%d')}")
        return target_date

    def search_snapshot(self, years_ago: int = 10, filename: str = "snapshot.html"):
        """
        Search for a snapshot close to a specific date and save it in a file.

        Args:
            years_ago (int, optional): Number of years ago from today to search for a snapshot. Default is 10.
            filename (str, optional): Name of the file to save the snapshot. Default is 'snapshot.html'.
        """
        target_date = self._get_target_date(years_ago)
        year, month, day = target_date.year, target_date.month, target_date.day

        appLogger.info(f"🚨 Searching for snapshot from {year}-{month:02d}-{day:02d}")

        cdx_api = WaybackMachineCDXServerAPI(self.url, self.user_agent)
        snapshot = cdx_api.near(year=year, month=month, day=day)

        if snapshot:
            appLogger.success(f"📈 Snapshot found! Timestamp: {snapshot.timestamp}, URL: {snapshot.archive_url}")
            self._download_snapshot(snapshot.archive_url, filename)
        else:
            appLogger.warning(f"❌ No snapshot found for the specified date.")

    def _download_snapshot(self, archive_url: str, filename: str):
        """
        Download the content of a Wayback Machine snapshot and save it to a file.

        Args:
            archive_url (str): URL of the snapshot on Wayback Machine.
            filename (str): Name of the file to save the snapshot.

        Returns:
            None
        """
        try:
            appLogger.info(f"⬇️ Downloading snapshot from: {archive_url}")
            response = requests.get(archive_url)
            response.raise_for_status()

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            
            appLogger.success(f"💾 Snapshot successfully saved to {filename}")

        except requests.exceptions.RequestException as e:
            appLogger.error(f"❌ Failed to download snapshot. Error: {e}")

    def search_snapshots_by_extensions(self, years_ago: int = 4, days_interval: int = 30, 
                                       extensions: list = None, match_type: str = "domain"):
        """
        Search for snapshots by file type within a specific time interval.

        Args:
            years_ago (int): Number of years ago to start searching.
            days_interval (int): Duration of the interval in days from the start date of the search.
            extensions (list, optional): List of file extensions to filter snapshots.
            match_type (str, optional): Type of match for the search in Wayback Machine.

        Returns:
            None: Printed results to the console.
        """
        if extensions is None:
            extensions = ["pdf", "doc", "docx", "ppt", "xls", "xlsx", "txt"]

        today = datetime.now()
        start_period = (today - timedelta(days=365 * years_ago)).strftime('%Y%m%d')
        end_period = (today - timedelta(days=(365 * years_ago) - days_interval)).strftime('%Y%m%d')

        appLogger.info(f"🕵️‍♂️ Searching for snapshots from {start_period} to {end_period} with extensions {extensions}")

        cdx_api = WaybackMachineCDXServerAPI(url=self.url, user_agent=self.user_agent,
                                             start_timestamp=start_period, end_timestamp=end_period,
                                             match_type=match_type)

        regex_filter = "(" + "|".join([f".*\\.{ext}$" for ext in extensions]) + ")"
        cdx_api.filters = [f"urlkey:{regex_filter}"]

        snapshots = cdx_api.snapshots()
        if snapshots:
            appLogger.info(f"✅ Found {len(snapshots)} snapshots matching criteria.")
            for snapshot in snapshots:
                appLogger.info(f"📅 Snapshot found! Timestamp: {snapshot.timestamp}, URL: {snapshot.archive_url}")
        else:
            appLogger.warning("❌ No snapshots found for the specified file types.")

if __name__ == "__main__":
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    url = "github.com"

    retrospect = Retrospect(url, user_agent)

    # Example snapshot search
    retrospect.search_snapshot()
    retrospect.search_snapshots_by_extensions(years_ago=1, days_interval=100)