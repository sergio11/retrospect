from datetime import datetime, timedelta
import os
from tqdm import tqdm
from retrospect.core.snapshot_downloader import SnapshotDownloader
from retrospect.core.wayback_machine_service import WaybackMachineService
from retrospect.utils.logger import appLogger

class Retrospect:

    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.snapshot_downloader = SnapshotDownloader(user_agent)
        self.wayback_service = WaybackMachineService(user_agent)
        appLogger.info(f"🛠️ [SYSTEM ONLINE] Retrospect initialized. Ready for infiltration.")

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

    def extract(self, url: str, years_ago: int = 10, days_interval: int = 30):
        """
        Searches for historical snapshots of a target URL and downloads them.

        Args:
            url (str): The target URL to extract.
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
                snapshot = self.wayback_service.take_snapshots(url, year, month, day)  # ✅ URL ahora es argumento
                
                if snapshot:
                    appLogger.info(f"📡 [BREACH DETECTED] Snapshot found: {snapshot.archive_url}")
                    self.snapshot_downloader.download_snapshot(snapshot.archive_url, file_dir)
                    pbar.update(1)
                else:
                    appLogger.warning(f"❌ [NO TRACE] No data footprint detected for {year}-{month}-{day}")
