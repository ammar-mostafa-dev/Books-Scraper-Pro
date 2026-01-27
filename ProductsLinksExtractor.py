from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import time
from logging_config import setup_logger
# configure logging 
logger = setup_logger(__name__)

# ----------------------------
# the main pages urls 
main_url = 'https://books.toscrape.com/'
catalogue_url = 'https://books.toscrape.com/catalogue/'


# --------------------------
# Helper Functions


def get_soup(url):
    '''This function makes a good request to the url and returns the soup (HTML) of the passed URL if the request had succeeded, otherwise returns None '''  
       # mandatory headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    # Using Try To handle Errors 
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()   # catches 4xx and 5xx status codes
    except Exception as e:
        return None
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    return soup
    

def extract_page_links(soup):
    '''This function gets soup for a page ,ensure there's products links in this page ,  extracts and return them , returns None if no products are found'''
    # validate page (Check if page got links or not)

    products_links = soup.select('.image_container a') # get the "a" tags from all products 
    if not products_links : 
        return None
    products_links = [link['href'] for link in products_links] # return links
    
    full_products_urls = [urljoin(catalogue_url,link) for link in products_links] # return full products urls 
    
    return full_products_urls


def extract_next_page_url(soup):
    '''Gets the next page URL dynamically relative to the current page'''
    next_page_tag = soup.select_one('.next > a') # get next page (a) tag
    if next_page_tag:
        return urljoin(catalogue_url, next_page_tag['href']) # return full url 
    else:
        return None
def build_next_page_url(page_num,pattern='page-{num}.html') : 
    '''This Function Is used To build a url in case extracting next page url using selectors failed or the soup itself wasn\'t found '''
    return urljoin(catalogue_url,pattern.format(num=page_num))


# ----------------------
# Main Extraction Function

def extract_all_products_links():
    '''This function Extracts all products links in every page of the website and returns a full list of products urls , handles pagination,expected crashouts and stops after 3 continued scraping failed attempts'''
    # current url variable to help in pagination 
    current_url = urljoin(catalogue_url ,'page-1.html')
    # current page num to help in tracking 
    current_page_num = 1
    # pages extracted variables 
    pages_extracted = 0
    # to store links of products
    all_links = []
    # to track failed attempts 
    failures = 0 

    while True :
        # get page soup
        soup = get_soup(current_url)
        if not soup:
            logger.warning(f'Failed To find {current_url} soup') 
            failures +=1 
            if failures == 3 : 
                logger.error('Failed To Scrape Links')
                return all_links 
            else : 
                current_page_num += 1
                current_url = build_next_page_url(current_page_num)
                pages_extracted += 1
                continue 
        # extract page links
        products_links = extract_page_links(soup)
        if products_links:
            all_links.extend(products_links)
            if current_page_num % 10 == 0 : 
                logger.info(f'{current_page_num} Pages Links Have Been scraped Succsesfuly')
                
            # reset faillures 
            failures = 0
        else:
            logger.warning(f"No Products Links Found For Url {current_url}") 
            failures += 1 
            if failures == 5 : 
                logger.error('Failed To Scrape Links')
                return all_links
            
       
        # find next URL
        next_url = extract_next_page_url(soup)
        if next_url : 
            current_url = next_url 
            current_page_num +=1 
            pages_extracted += 1
            continue
        else : 
            logger.info(f'{pages_extracted} Pages Has Been Scraped ')
            return all_links

def main() : 
    pass
if __name__ == '__main__' : 
    # run file 
    main()
