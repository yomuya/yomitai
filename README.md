# yomitai

A command-line tool for scraping novel data from Syosetu (小説家になろう). Fetch novel metadata via API, scrape individual chapters, or scrape a range of chapters and save results as JSON.

## Features

- Fetch novel info using the Syosetu API
- Scrape a single chapter's content
- Scrape a range of chapters with progress bar
- Saves all results as JSON in a `Scrapes/` directory

## Requirements

- Python 3.7+
- See [requirements.txt](./requirements.txt) for dependencies:

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Menu

Run without arguments for an interactive menu:
```bash
python main.py
```

### Command-Line Arguments

You can also use command-line arguments for scripting:

#### Fetch novel info via API
```bash
python main.py api <ncode>
```

#### Scrape a single chapter
```bash
python main.py chapter <ncode> <chapter_num>
```

#### Scrape a range of chapters
```bash
python main.py range <ncode> <start> <end>
```

Example:
```bash
python main.py range n4185ci 1 5
```

## Output

All results are saved as JSON files in the `Scrapes/` directory.

## Disclaimer

- Respect [robots.txt](https://syosetu.com/robots.txt) and Syosetu's terms of service.
- Use responsibly and avoid excessive requests.
