thonimport requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin

class GoogleMapBusinessExtractor:
    def __init__(self, search_url):
        self.search_url = search_url
        self.business_data = []

    def fetch_page(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        return response.text if response.status_code == 200 else None

    def extract_business_info(self, page_content):
        soup = BeautifulSoup(page_content, 'html.parser')
        businesses = soup.find_all('div', class_='section-result')
        
        for business in businesses:
            name = business.find('h3', class_='section-result-title').text.strip()
            address = business.find('span', class_='section-result-location').text.strip()
            phone = business.find('span', class_='section-result-phone').text.strip() if business.find('span', class_='section-result-phone') else 'N/A'
            email = self.extract_email_from_website(business)
            self.business_data.append({
                'businessName': name,
                'address': address,
                'phone': phone,
                'email': email
            })
    
    def extract_email_from_website(self, business):
        website_url = business.find('a', class_='section-result-action')['href']
        page_content = self.fetch_page(urljoin(self.search_url, website_url))
        soup = BeautifulSoup(page_content, 'html.parser')
        email = None
        for link in soup.find_all('a', href=True):
            if re.match(r"mailto:", link['href']):
                email = link['href'][7:]
                break
        return email

    def save_data(self):
        with open('business_data.json', 'w') as f:
            json.dump(self.business_data, f, indent=4)

    def scrape(self):
        page_content = self.fetch_page(self.search_url)
        if page_content:
            self.extract_business_info(page_content)
            self.save_data()

if __name__ == "__main__":
    search_url = 'https://www.google.com/maps/search/marketing+agencies+near+me'
    scraper = GoogleMapBusinessExtractor(search_url)
    scraper.scrape()