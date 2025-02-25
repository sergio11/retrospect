from retrospect.retrospect import Retrospect

def main():
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    url = "example.com" #The domain

    retrospect = Retrospect(user_agent)
    retrospect.recon(url=url, years_ago=5, days_interval=3)

if __name__ == "__main__":
    main()