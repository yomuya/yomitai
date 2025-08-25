import os
import sys
import json
import argparse
from scrape import fetch_novel_api, scrape_chapter_data, scrape_chapters_range
from rich import print

def save_json(data, filename):
    os.makedirs("Scrapes", exist_ok=True)
    path = os.path.join("Scrapes", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {path}")

def run_menu():
    print("Syosetu Scraper CLI")
    print("1. Fetch novel info via API")
    print("2. Scrape a single chapter")
    print("3. Scrape a range of chapters")
    choice = input("Choose an option (1-3): ").strip()
    ncode = input("Enter novel ncode (e.g., n4185ci): ").strip()
    # Always save as JSON, no prompt

    if choice == "1":
        from scrape import fetch_novel_api
        try:
            data = fetch_novel_api(ncode)
            save_json(data, f"{ncode}_api.json")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "2":
        from scrape import scrape_chapter_data
        chapter_num = int(input("Enter chapter number: ").strip())
        try:
            data = scrape_chapter_data(ncode, chapter_num)
            save_json(data, f"{ncode}_chapter_{chapter_num}.json")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "3":
        from scrape import scrape_chapters_range
        start = int(input("Enter start chapter number: ").strip())
        end = int(input("Enter end chapter number: ").strip())
        try:
            results = scrape_chapters_range(ncode, start, end)
            save_json(results, f"{ncode}_range_{start}_{end}.json")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice.")

def run_args(args):
    parser = argparse.ArgumentParser(description="Syosetu Scraper CLI")
    parser.add_argument("ncode", help="Novel ncode (e.g., n4185ci)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("api", help="Fetch novel info via API")

    parser_chapter = subparsers.add_parser("chapter", help="Scrape a single chapter")
    parser_chapter.add_argument("chapter_num", type=int, help="Chapter number")

    parser_range = subparsers.add_parser("range", help="Scrape a range of chapters")
    parser_range.add_argument("start", type=int, help="Start chapter number")
    parser_range.add_argument("end", type=int, help="End chapter number")

    args = parser.parse_args()

    if args.command == "api":
        try:
            data = fetch_novel_api(args.ncode)
            save_json(data, f"{args.ncode}_api.json")
        except Exception as e:
            print(f"Error: {e}")
    elif args.command == "chapter":
        try:
            data = scrape_chapter_data(args.ncode, args.chapter_num)
            save_json(data, f"{args.ncode}_chapter_{args.chapter_num}.json")
        except Exception as e:
            print(f"Error: {e}")
    elif args.command == "range":
        try:
            results = scrape_chapters_range(args.ncode, args.start, args.end)
            save_json(results, f"{args.ncode}_range_{args.start}_{args.end}.json")
        except Exception as e:
            print(f"Error: {e}")
    else:
        parser.print_help()


def main():
    if len(sys.argv) == 1:
        run_menu()
    else:
        run_args(sys.argv)



if __name__ == "__main__":
    main()
