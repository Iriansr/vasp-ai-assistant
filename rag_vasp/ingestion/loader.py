import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time, json, os

BASE_URL = "https://vasp.at"
ALL_PAGES = "https://vasp.at/wiki/Special:AllPages"


class VaspWikiLoader:

    def __init__(self, delay=0.5):
        self.delay = delay

    def fetch(self, url):
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text

    def is_valid_page(self, href):

        if not href.startswith("/wiki/"):
            return False

        blacklist = [
            "Special:",
            "File:",
            "Category:",
            "Template:",
            "Help:"
        ]

        return not any(x in href for x in blacklist)

    def get_all_pages(self):

        pages = []
        next_page = ALL_PAGES

        while next_page:

            html = self.fetch(next_page)
            soup = BeautifulSoup(html, "lxml")

            content = soup.find("div", class_="mw-allpages-body")

            for a in content.find_all("a"):

                href = a.get("href")

                if self.is_valid_page(href):

                    url = urljoin(BASE_URL, href)

                    if "index.php" not in url:
                        pages.append(url)

            next_link = soup.find("a", string="Next page")

            if next_link:
                next_page = urljoin(BASE_URL, next_link["href"])
            else:
                next_page = None

        return sorted(set(pages))

    def normalize_text(self,text):

        text = text.replace("\xa0", " ")
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        text = text.replace(" – ", " - ")

        return text.strip()

    def parse_sections(self, soup):

        content = soup.find("div", id="mw-content-text")

        if not content:
            return []

        for tag in content(["table", "style", "script"]):
            tag.decompose()

        sections = []
        current_section = "Introduction"
        buffer = []

        for element in content.find_all(["h2", "h3", "p", "li"]):

            if element.name in ["h2", "h3"]:

                if buffer:

                    text = "\n".join(buffer)
                    text = self.normalize_text(text)

                    if len(text) > 200:   # filtro clave
                        sections.append({
                            "section": current_section,
                            "content": text
                        })

                    buffer = []

                current_section = element.get_text(strip=True)

                # limpiar headings tipo [edit]
                current_section = current_section.replace("[edit]", "")

            else:

                text = element.get_text(" ", strip=True)

                if len(text) > 40:
                    buffer.append(text)

        if buffer:

            text = "\n".join(buffer)
            text = self.normalize_text(text)

            if len(text) > 200:
                sections.append({
                    "section": current_section,
                    "content": text
                })

        return sections
    

    def parse_page(self, url):

        html = self.fetch(url)
        soup = BeautifulSoup(html, "lxml")

        title = soup.find("h1").text.strip()
        title = title.replace("Category:", "")

        sections = self.parse_sections(soup)

        return {
            "title": title,
            "url": url,
            "sections": sections
        }

    def load(self):

        pages = self.get_all_pages()

        print("Total pages:", len(pages))

        docs = []

        for url in pages:

            try:

                doc = self.parse_page(url)

                if len(doc["sections"]) > 0:
                    docs.append(doc)

                time.sleep(self.delay)

            except Exception as e:

                print("error:", url, e)

        return docs
    
    def save_docs(self, docs, path="data/docs.jsonl"):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:

            for doc in docs:
                f.write(json.dumps(doc) + "\n")
    
    def load_docs(path="data/docs.jsonl"):

        docs = []

        with open(path) as f:

            for line in f:
                docs.append(json.loads(line))

        return docs

    def save_chunks(chunks, path="data/chunks.jsonl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:

            for c in chunks:
                f.write(json.dumps(c) + "\n")

    def load_chunks(path="data/chunks.jsonl"):

        chunks = []

        with open(path) as f:

            for line in f:
                chunks.append(json.loads(line))

        return chunks

if __name__ == "__main__":

    loader = VaspWikiLoader()

    docs = loader.load()

    print("documents:", len(docs))