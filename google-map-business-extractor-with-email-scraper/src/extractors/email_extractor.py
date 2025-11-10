thonimport requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class EmailExtractor:
    def __init__(self, business_url):
        self.business_url = business_url

    def fetch_page(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(self.business_url, headers=headers)
        return response.text if response.status_code == 200 else None

    def extract_email(self):
        page_content = self.fetch_page()
        soup = BeautifulSoup(page_content, 'html.parser')
        email = None
        for link in soup.find_all('a', href=True):
            if re.match(r"mailto:", link['href']):
                email = link['href'][7:]
                break
        return email