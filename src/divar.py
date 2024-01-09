import requests
from bs4 import BeautifulSoup


class divar:
    def __init__(self, url) -> None:
        self.ads = []
        self.url = url

    def get_ads(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.find_all(class_='post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46')
            for a_item in a_tags:
                try:
                    a_tag = a_item.find('a')
                    if a_tag:
                        self.ads.append('https://divar.ir'+a_tag["href"])
                    else:
                        print("No <a> tag found within a <li> tag.")
                except:
                    pass
        print(len(self.ads))
        return self.ads
