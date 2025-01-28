from waybackpy import WaybackMachineCDXServerAPI
from retrospect.utils.logger import appLogger

class WaybackMachineService:
    def __init__(self, url: str, user_agent: str):
        self.url = url
        self.user_agent = user_agent

    def search_near(self, year: int, month: int, day: int):
        """
        Search for the snapshot closest to a specific date.

        Args:
            year (int): Year of the snapshot.
            month (int): Month of the snapshot.
            day (int): Day of the snapshot.

        Returns:
            The closest snapshot for the specified date, or None if no snapshot is found.
        """
        cdx_api = WaybackMachineCDXServerAPI(url=self.url, user_agent=self.user_agent)
        snapshot = cdx_api.near(year=year, month=month, day=day)
        if snapshot:
            return snapshot
        else:
            return None


    def search_snapshots(self, start_period: str, end_period: str, extensions: list = None, match_type: str = "domain") -> list:
        """
        Search for snapshots in a date range with specified extensions.

        Args:
            start_period (str): Start date of the period (format: 'YYYYMMDD').
            end_period (str): End date of the period (format: 'YYYYMMDD').
            extensions (list): List of file extensions to filter snapshots.

        Returns:
            list: List of snapshots that match the extensions and period.
        """
        if extensions is None:
            extensions = ["pdf", "doc", "docx", "ppt", "xls", "xlsx", "txt", "html"]

        cdx_api = WaybackMachineCDXServerAPI(url=self.url, user_agent=self.user_agent,
                                             start_timestamp=start_period, end_timestamp=end_period,
                                             match_type=match_type)

        regex_filter = "(" + "|".join([f".*\\.{ext}$" for ext in extensions]) + ")"
        cdx_api.filters = [f"urlkey:{regex_filter}"]

        snapshots = list(cdx_api.snapshots())

        if snapshots:
            return snapshots
        else:
            return []