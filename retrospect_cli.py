import argparse
from retrospect.retrospect import Retrospect
from dotenv import load_dotenv

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Retrospect: Historical Web Analysis & Cybersecurity Tool")
    parser.add_argument('--url', type=str, required=True, help="The target URL to scan (e.g., https://example.com).")
    parser.add_argument('--user_agent', type=str, default="Mozilla/5.0", help="The User-Agent string to be used for HTTP requests (default: Mozilla/5.0).")
    parser.add_argument('--years_ago', type=int, default=10, help="Number of years back to search for snapshots (default: 10).")
    parser.add_argument('--days_interval', type=int, default=30, help="Time interval (in days) between each snapshot request (default: 30).")

    args = parser.parse_args()

    retrospect = Retrospect(user_agent=args.user_agent)
    retrospect.recon(url=args.url, years_ago=args.years_ago, days_interval=args.days_interval)

if __name__ == "__main__":
    main()