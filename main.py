from retrospect.retrospect import Retrospect

def main():
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    url = "www.nbcnews.com"

    retrospect = Retrospect(user_agent)
    retrospect.extract(url=url, years_ago=5, days_interval=20)

if __name__ == "__main__":
    main()