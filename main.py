import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(list)
        self.visited = set()
        self.session_visited = set()

    def crawl(self, url, base_url=None, depth=0, max_depth=2):
        if url in self.visited or depth >= max_depth:
            return
        self.visited.add(url)
        self.session_visited.add(url)  # Add to session visited URLs
        print(f"Crawling: {url}")

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    if urlparse(href).netloc:
                        absolute_url = href
                    else:
                        absolute_url = urljoin(base_url or url, href)
                    if absolute_url.startswith("http"):  # Check if it's an absolute URL
                        if absolute_url not in self.session_visited:  # Check if URL is already visited in this session
                           self.crawl(absolute_url, base_url=base_url or url, depth=depth+1, max_depth=max_depth)
        except Exception as e:
            print(f"Error crawling {url}: {e}")


    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            if keyword.lower()  in text.lower(): #removed not because it not displaying weather their is a result or not 
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")# replaced result with undefined_variable
        else:
            print("No results found.")


def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.crawl(start_url)

    keyword = "Domain"
    results = crawler.search(keyword)
    crawler.print_results(results)

if __name__=="__main__":
    main()