import requests
import time
from bs4 import BeautifulSoup
import urllib.robotparser
from tqdm import tqdm
from rich import print

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Cookie': 'over18=yes'
}

def is_allowed_by_robots(url, user_agent=HEADERS['User-Agent']):
    parsed_url = requests.utils.urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception:
        return False
    return rp.can_fetch(user_agent, url)

def fetch_novel_api(ncode):
    ncode = ncode.lower()
    url = f"https://api.syosetu.com/novelapi/api/?out=json&ncode={requests.utils.quote(ncode)}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def scrape_chapter_data(ncode, chapter_num):
    url = f"https://ncode.syosetu.com/{requests.utils.quote(ncode)}/{requests.utils.quote(str(chapter_num))}"
    if not is_allowed_by_robots(url):
        raise Exception(f"Scraping disallowed by robots.txt: {url}")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select_one('.p-novel__title')
    preface = soup.select_one('div.p-novel__text--preface')
    chapter = soup.select_one('div.p-novel__text:not(.p-novel__text--preface):not(.p-novel__text--afterword)')
    afterword = soup.select_one('div.p-novel__text--afterword')

    title_text = title.get_text(strip=True) if title else ""
    preface_text = preface.get_text(strip=True) if preface else ""
    chapter_text = chapter.get_text(strip=True) if chapter else ""
    afterword_text = afterword.get_text(strip=True) if afterword else ""
    length_chars = len(preface_text) + len(chapter_text) + len(afterword_text)

    return {
        "ncode": ncode,
        "chapterNum": chapter_num,
        "title": title_text,
        "preface": preface_text,
        "body": chapter_text,
        "afterword": afterword_text,
        "length_chars": length_chars,
        "url": url
    }

def scrape_chapters_range(ncode, start, end):
    ncode = ncode.lower()
    results = []
    for ch in tqdm(range(start, end + 1), desc="Scraping chapters"):
        try:
            data = scrape_chapter_data(ncode, ch)
            results.append({"chapter": ch, "success": True, "data": data})
        except Exception as e:
            results.append({"chapter": ch, "success": False, "error": str(e)})

        # respect crawl-delay from robots.txt 
        # default to 1.5s if not set
        parsed_url = requests.utils.urlparse(f"https://ncode.syosetu.com/{ncode}/{ch}")
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
        except Exception:
            pass
        user_agent = HEADERS['User-Agent']
        delay = rp.crawl_delay(user_agent)
        time.sleep(delay if delay is not None else 1.5)
    return results
