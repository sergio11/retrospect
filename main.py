from retrospect.retrospect import Retrospect

def main():
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    url = "github.com"

    retrospect = Retrospect(url, user_agent)
    retrospect.search_and_download_snapshots(years_ago=1, days_interval=3)

if __name__ == "__main__":
    main()