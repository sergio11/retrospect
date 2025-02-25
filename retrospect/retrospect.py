from datetime import datetime, timedelta
import os
from tqdm import tqdm
from retrospect.core.snapshot_downloader import SnapshotDownloader
from retrospect.core.snapshot_extractor import SnapshotExtractor
from retrospect.core.wayback_machine_service import WaybackMachineService
from retrospect.core.security_analyzer import SensitiveDataAnalyzer
from retrospect.utils.logger import appLogger
from retrospect import __version__

class Retrospect:
    """
    Retrospect is a reconnaissance and security analysis tool that retrieves historical web snapshots, 
    extracts their content, and analyzes potential security risks.

    This class leverages the Wayback Machine to gather archived snapshots of a target URL, downloads the snapshots,
    extracts their text content, and performs security analysis to identify possible data leaks.

    Attributes:
        user_agent (str): The User-Agent string used for HTTP requests to mimic a real browser.
        snapshot_downloader (SnapshotDownloader): Handles the downloading of archived snapshots.
        wayback_service (WaybackMachineService): Interacts with the Wayback Machine to retrieve snapshots.
        security_analyzer (SensitiveDataAnalyzer): Analyzes extracted text for potential security vulnerabilities.

    Methods:
        recon(url: str, years_ago: int = 10, days_interval: int = 30)
            Performs reconnaissance by retrieving, downloading, and processing snapshots from the past.
    """

    def __init__(self, user_agent: str):
        """
        Initializes the Retrospect system by setting up the required services for reconnaissance and security analysis.

        Args:
            user_agent (str): The User-Agent string to be used for HTTP requests.
        """
        self._print_banner()
        self.user_agent = user_agent
        self.snapshot_downloader = SnapshotDownloader(user_agent)
        self.wayback_service = WaybackMachineService(user_agent)
        self.security_analyzer = SensitiveDataAnalyzer()
        appLogger.info(f"🛠️ [SYSTEM ONLINE] Retrospect initialized. Ready for infiltration.")

    def recon(self, url: str, years_ago: int = 10, days_interval: int = 30):
        """
        Performs reconnaissance on a target URL by retrieving, downloading, and analyzing historical snapshots.

        This method queries the Wayback Machine for archived snapshots of the given URL within a specified time range.
        The retrieved snapshots are downloaded, their content is extracted, and a security analysis is performed.

        Args:
            url (str): The target URL to analyze.
            years_ago (int, optional): The number of years back to search for archived snapshots. Defaults to 10 years.
            days_interval (int, optional): The time interval (in days) between each snapshot request. Defaults to 30 days.

        Workflow:
            1. Extracts the domain name from the provided URL.
            2. Defines the search period based on the given years and interval.
            3. Requests archived snapshots from the Wayback Machine within the specified range.
            4. Downloads available snapshots and stores them in a local directory.
            5. Extracts textual content from downloaded snapshots.
            6. Saves extracted content into a unified file for further analysis.
            7. Runs a security analysis to identify potential leaks or vulnerabilities.
        """
        domain_name = url.split("//")[-1].split("/")[0]

        today = datetime.now()
        start_date = (today - timedelta(days=365 * years_ago)).strftime('%Y%m%d')
        end_date = (today - timedelta(days=(365 * years_ago) - days_interval)).strftime('%Y%m%d')

        appLogger.info(f"🔍 [RECON] Target locked: {url}. Scanning archives from {start_date} to {end_date}...")

        file_dir = os.path.join(os.getcwd(), domain_name)
        os.makedirs(file_dir, exist_ok=True)

        with tqdm(desc="💾 [EXFILTRATION] Downloading snapshots", unit="snapshot") as pbar:
            for single_date in self._date_range(start_date, end_date):
                year, month, day = single_date.year, single_date.month, single_date.day
                snapshot = self.wayback_service.take_snapshots(url, year, month, day)
                if snapshot:
                    self.snapshot_downloader.download_snapshot(snapshot.archive_url, file_dir)
                    pbar.update(1)

        appLogger.info(f"🔎 [EXTRACTION] Extracting content from downloaded snapshots...")
        extractor = SnapshotExtractor(file_dir)
        extractor.process_snapshots()
        unified_file = f"{file_dir}/unified_snapshots.txt"
        appLogger.info(f"✅ [DONE] Snapshot extraction completed. Content saved to {unified_file}")

        self._analyze_security(unified_file)


    def _analyze_security(self, file_path: str):
        """
        Analyzes the extracted content for sensitive data leaks and potential security risks.

        This method processes the unified extracted text file to identify security vulnerabilities, such as 
        exposed credentials, personally identifiable information (PII), or other sensitive data.

        Args:
            file_path (str): Path to the extracted and unified text file.

        Logs:
            - Info: Indicates the start of the security analysis.
            - Info: Displays the results of the analysis.
            - Error: Captures and logs any exceptions that occur during the analysis.
        """
        try:
            appLogger.info(f"🔒 [SECURITY ANALYSIS] Analyzing content for sensitive data leaks...")
            result_message = self.security_analyzer.analyze_sensitive_data(unified_file_path=file_path)
            appLogger.info(result_message)

        except Exception as e:
            appLogger.error(f"⚠️ [SECURITY ANALYSIS] Error during security analysis: {e}")

    def _get_target_date(self, years_ago: int) -> datetime:
        """
        Calculates a target date by subtracting the specified number of years from the current date.

        Args:
            years_ago (int): The number of years to subtract from today's date.

        Returns:
            datetime: The calculated target date.

        Logs:
            - Debug: Logs the computed target date for reference.
        """
        target_date = datetime.now() - timedelta(days=365 * years_ago)
        appLogger.debug(f"⏳ [TIME WARP] Adjusting timeline... Target date: {target_date.strftime('%Y-%m-%d')}")
        return target_date

    def _date_range(self, start_date: str, end_date: str):
        """
        Generates a sequence of dates from start_date to end_date, incrementing by one day.

        This generator function is useful for iterating through a range of dates when searching 
        for historical snapshots.

        Args:
            start_date (str): The start date in "YYYYMMDD" format.
            end_date (str): The end date in "YYYYMMDD" format.

        Yields:
            datetime: The next date in the range.
        """
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")
        delta = timedelta(days=1)

        while start <= end:
            yield start
            start += delta


    def _print_banner(self):
        """
        Prints a welcome banner at the start of the program for Retrospect.
        """
        banner = f"""
        ██████╗ ███████╗████████╗██████╗  ██████╗ ███████╗██████╗ ███████╗ ██████╗████████╗
        ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝
        ██████╔╝█████╗     ██║   ██████╔╝██║   ██║███████╗██████╔╝█████╗  ██║        ██║   
        ██╔══██╗██╔══╝     ██║   ██╔══██╗██║   ██║╚════██║██╔═══╝ ██╔══╝  ██║        ██║   
        ██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝███████║██║     ███████╗╚██████╗   ██║   
        ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝                                                                                                                                                                                                                                                                                                                                                                                          
        Retrospect: Advanced Ethical Hacking for passive information gathering and historical web analysis  (Version: {__version__})
        """
        print(banner)