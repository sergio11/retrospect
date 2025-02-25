from retrospect.utils.logger import appLogger
from waybackpy import WaybackMachineCDXServerAPI

class WaybackMachineService:
    """
    The WaybackMachineService class interacts with the Wayback Machine API to retrieve historical snapshots of
    a given URL for a specific date. The service is designed to fetch the closest available snapshot based on the 
    specified year, month, and day. It helps in obtaining archived versions of web pages to analyze their content, 
    including identifying potential security vulnerabilities or data leaks.

    Attributes:
        user_agent (str): The user-agent string to be used in HTTP requests for interacting with the Wayback Machine.
    """
    
    def __init__(self, user_agent: str):
        """
        Initializes the WaybackMachineService with the provided user-agent string. This allows communication 
        with the Wayback Machine API to search and retrieve historical snapshots.

        Args:
            user_agent (str): The user-agent string used in HTTP requests for the API interactions.
        """
        self.user_agent = user_agent
        appLogger.info(f"🛠️ [INIT] WaybackMachineService online. Awaiting target...")

    def take_snapshots(self, url: str, year: int, month: int, day: int):
        """
        Retrieves the closest historical snapshot from the Wayback Machine for a specified date (year, month, day).
        If a snapshot exactly matching the date is unavailable, the method will attempt to find the closest available 
        snapshot around the specified date.

        Args:
            url (str): The URL of the website to search for in the Wayback Machine archives.
            year (int): The year of the snapshot to retrieve.
            month (int): The month of the snapshot to retrieve.
            day (int): The day of the snapshot to retrieve.

        Returns:
            WaybackMachineCDXServerAPI: The closest snapshot object found from the Wayback Machine. If no snapshot 
            is found or if an error occurs, the method returns `None`.
        
        Raises:
            Exception: If there is an issue with the Wayback Machine API or the connection, an error is logged and 
            `None` is returned.
        """
        try:
            # Initialize the Wayback Machine API client
            cdx_api = WaybackMachineCDXServerAPI(url=url, user_agent=self.user_agent)
            # Attempt to fetch the closest snapshot for the specified date
            snapshot = cdx_api.near(year=year, month=month, day=day)
            return snapshot
        except Exception as e:
            return None