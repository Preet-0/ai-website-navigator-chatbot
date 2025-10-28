import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_site_links(base_url, max_pages=20):
    visited = set()
    links = {}

    def crawl(url):
        if len(visited) >= max_pages:
            return
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            for a_tag in soup.find_all("a", href=True):
                full_link = urljoin(base_url, a_tag["href"])
                if base_url in full_link and full_link not in visited:
                    visited.add(full_link)
                    links[a_tag.text.strip() or "Unnamed Link"] = full_link
                    crawl(full_link)
        except Exception:
            pass

    crawl(base_url)
    return links
