from datetime import datetime, timedelta
import os
from tqdm import tqdm
from retrospect.core.snapshot_downloader import SnapshotDownloader
from retrospect.core.wayback_machine_service import WaybackMachineService
from retrospect.utils.logger import appLogger

class Retrospect:
    def __init__(self, url: str, user_agent: str):
        self.url = url
        self.user_agent = user_agent
        self.domain_name = url.split("//")[-1].split("/")[0]
        self.wayback_service = WaybackMachineService(url, user_agent)
        self.snapshot_downloader = SnapshotDownloader(user_agent)
        appLogger.info(f"🔎 Initialized Retrospect for URL: {self.url}")

    def _get_target_date(self, years_ago: int) -> datetime:
        target_date = datetime.now() - timedelta(days=365 * years_ago)
        appLogger.debug(f"📅 Target date calculated: {target_date.strftime('%Y-%m-%d')}")
        return target_date

    def search_and_download_snapshots(self, years_ago: int = 10, days_interval: int = 30,
                                      extensions: list = None, match_type: str = "domain"):
    
        today = datetime.now()
        start_period = (today - timedelta(days=365 * years_ago)).strftime('%Y%m%d')
        end_period = (today - timedelta(days=(365 * years_ago) - days_interval)).strftime('%Y%m%d')

        appLogger.info(f"🕵️‍♂️ Searching for snapshots from {start_period} to {end_period} with extensions {extensions}")

        file_dir = os.path.join(os.getcwd(), self.domain_name)
        os.makedirs(file_dir, exist_ok=True)

        with tqdm(desc="Downloading snapshots", unit="snapshot") as pbar:
            for single_date in self._date_range(start_period, end_period):
                year, month, day = single_date.year, single_date.month, single_date.day
                snapshot = self.wayback_service.search_near(year, month, day)
                if snapshot:
                    self.snapshot_downloader.download_snapshot(snapshot.archive_url, file_dir)
                    pbar.update(1)

        appLogger.info("🕵️‍♂️ Searching for other snapshots matching specified extensions...")
        snapshots = self.wayback_service.search_snapshots(start_period, end_period, extensions, match_type)
        if snapshots:
            appLogger.info(f"✅ Found {len(snapshots)} snapshots matching criteria.")
            with tqdm(total=len(snapshots), desc="Downloading snapshots", unit="snapshot") as pbar:
                for snapshot in snapshots:
                    self.snapshot_downloader.download_snapshot(snapshot.archive_url, file_dir)
                    pbar.update(1)
            appLogger.info("🚀 All extended snapshots downloaded successfully. Mission accomplished.")
        else:
            appLogger.warning("❌ No extended snapshots found. The data shadows remain hidden.")

    def _date_range(self, start_date: str, end_date: str):
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")
        delta = timedelta(days=1)
        current_date = start
        while current_date <= end:
            yield current_date
            current_date += delta