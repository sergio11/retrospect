from retrospect.utils.logger import appLogger
from waybackpy import WaybackMachineCDXServerAPI

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
            The closest snapshot for the specified date, or None if no snapshot is found or if an error occurs.
        """
        try:
            cdx_api = WaybackMachineCDXServerAPI(url=url, user_agent=self.user_agent)
            snapshot = cdx_api.near(year=year, month=month, day=day)
            return snapshot
        except Exception as e:
            appLogger.error(f"❌ [ERROR] An error occurred while fetching snapshot for {url} on {year}-{month}-{day}: {e}")
            return None
