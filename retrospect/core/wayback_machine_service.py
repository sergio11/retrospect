from waybackpy import WaybackMachineCDXServerAPI
from retrospect.utils.logger import appLogger

class WaybackMachineService:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        appLogger.info(f"🛠️ [INIT] WaybackMachineService online. Awaiting target...")

    def take_snapshots(self, url: str, year: int, month: int, day: int):
        """
        Take a snapshot or retrieve the closest one to a specific date.

        Args:
            url (str): Target URL to search in Wayback Machine.
            year (int): Year of the snapshot.
            month (int): Month of the snapshot.
            day (int): Day of the snapshot.

        Returns:
            The closest snapshot for the specified date, or None if no snapshot is found.
        """
        appLogger.info(f"📡 [SCANNING] Searching Wayback Machine for {url} on {year}-{month}-{day}...")
        cdx_api = WaybackMachineCDXServerAPI(url=url, user_agent=self.user_agent)
        snapshot = cdx_api.near(year=year, month=month, day=day)

        if snapshot:
            appLogger.info(f"📸 [HIT] Snapshot found: {snapshot.archive_url}")
            return snapshot
        else:
            appLogger.warning(f"❌ [MISS] No snapshot found for {url} on {year}-{month}-{day}")
            return None
