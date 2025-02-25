from datetime import datetime, timedelta
import os
from tqdm import tqdm
from retrospect.core.snapshot_downloader import SnapshotDownloader
from retrospect.core.snapshot_extractor import SnapshotExtractor
from retrospect.core.wayback_machine_service import WaybackMachineService
from retrospect.core.security_analyzer import SensitiveDataAnalyzer
from retrospect.utils.logger import appLogger

class Retrospect:

    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.snapshot_downloader = SnapshotDownloader(user_agent)
        self.wayback_service = WaybackMachineService(user_agent)
        self.security_analyzer = SensitiveDataAnalyzer()
        appLogger.info(f"🛠️ [SYSTEM ONLINE] Retrospect initialized. Ready for infiltration.")

    def recon(self, url: str, years_ago: int = 10, days_interval: int = 30):
        """
        Performs reconnaissance on historical snapshots of a target URL, downloads them, and extracts content.
        
        Args:
            url (str): The target URL to scan.
            years_ago (int): How many years back to look for snapshots.
            days_interval (int): Interval in days to define the search period.
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

        Args:
            file_path (str): Path to the extracted and unified file.
        """
        try:
            appLogger.info(f"🔒 [SECURITY ANALYSIS] Analyzing content for sensitive data leaks...")
            result_message = self.security_analyzer.analyze_sensitive_data(
                unified_file_path=file_path
            )
            appLogger.info(result_message)
        
        except Exception as e:
            appLogger.error(f"⚠️ [SECURITY ANALYSIS] Error during security analysis: {e}")

    def _get_target_date(self, years_ago: int) -> datetime:
        """Calculates the target date based on the years_ago parameter."""
        target_date = datetime.now() - timedelta(days=365 * years_ago)
        appLogger.debug(f"⏳ [TIME WARP] Adjusting timeline... Target date: {target_date.strftime('%Y-%m-%d')}")
        return target_date
    
    def _date_range(self, start_date: str, end_date: str):
        """Generates a date range between start_date and end_date."""
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")
        delta = timedelta(days=1)
        
        while start <= end:
            yield start
            start += delta