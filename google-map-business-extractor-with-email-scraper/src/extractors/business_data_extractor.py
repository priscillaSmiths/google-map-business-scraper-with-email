thonimport requests
from bs4 import BeautifulSoup

class BusinessDataExtractor:
    def __init__(self, business_page_url):
        self.business_page_url = business_page_url

    def fetch_page(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(self.business_page_url, headers=headers)
        return response.text if response.status_code == 200 else None

    def extract_business_info(self):
        page_content = self.fetch_page()
        soup = BeautifulSoup(page_content, 'html.parser')
        name = soup.find('h1', class_='section-hero-header-title').text.strip()
        address = soup.find('span', class_='section-info-line').text.strip()
        phone = soup.find('button', class_='section-hero-header-phone').text.strip()
        return {
            'businessName': name,
            'address': address,
            'phone': phone
        }