from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from requests import get
from urllib.parse import urljoin
from time import sleep
class DataCollection:
    def __init__(self, start_url):
        self.url = start_url

    def fetch_all_hrefs(self):
        hrefs = []
        html = get(self.url).text
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")
        for link in links:
            if link.get("href") is None:
                continue
            if "mid" in link.get("href"):
                hrefs.append(link.get("href"))
        return hrefs
    def download_from_hrefs(self, hrefs):
        for href in hrefs:
            fpath = "midi_downloads/" + href
            download_loc = urljoin(self.url, href)
            urlretrieve(download_loc, fpath)
            print("Saved to:", fpath)
            sleep(4)


dc = DataCollection("https://www.vgmusic.com/music/other/miscellaneous/piano/")
hrefs = dc.fetch_all_hrefs()
dc.download_from_hrefs(hrefs)