from ProductsLinksExtractor import get_soup, extract_all_products_links
from logging_config import setup_logger
import re
import time
import html

# Configure logger
logger = setup_logger(__name__)
# Product Schema 
""" Product Data Schema:
Each extracted product is stored as a dictionary with the following structure:

{
    "title": str,                # Full product title
    "price_excl_tax": float,     # Price without tax (e.g., 51.77)
    "price_incl_tax": float,     # Price with tax included
    "tax": float,         # Tax value
    "description": str,          # Full product description text
    "rating": int,               # Numerical star rating (1-5)
    "stock_availability": bool,  # Boolean availability (e.g., "True","False")
    "quantity_available": int,   # Numeric stock count
}
"""
# Helper Functions
# ----------------------

def clean_description(text):
    if not text:
        return None

    try:
        # 1. THE REPAIR: This fixes the 'â€™' symbols automatically
        # It takes the 'Latin-1' mess and converts it back to proper UTF-8
        text = text.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If it's already clean, the above might fail, so we just keep going
        pass

    # 2. Handle HTML entities (like &amp; or &eacute;)
    text = html.unescape(text)

    # 3. Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def clean_price(price_string):
    """Cleans a price string to float."""
    if not price_string:
        return None
    
    try:
        # This regex says: "Find everything that is NOT a digit or a decimal point and remove it"
        # It handles '£51.77', 'Â£51.77', or even 'Price: 51.77'
        price_cleaned = re.sub(r'[^\d.]', '', price_string)
        
        return float(price_cleaned)
    except (ValueError, TypeError):
        return None

def extract_stock(text):
    """Returns stock availability as bool and quantity as int or None."""
    in_stock = "in stock" in text.lower()
    match = re.search(r'\((\d+)\s+available\)', text)
    quantity = int(match.group(1)) if match else None
    return in_stock, quantity

def extract_category(soup):
    """Extracts book category from breadcrumbs."""
    breadcrumb_links = soup.select('ul.breadcrumb li a')
    if len(breadcrumb_links) >= 2:
        return breadcrumb_links[1].get_text(strip=True)
    return None

def extract_title(soup):
    tag = soup.select_one('.col-sm-6.product_main h1')
    return tag.get_text(strip=True) if tag else None

def extract_description(soup):
    tag = soup.select_one('#product_description + p')
    return clean_description(tag.get_text(strip=True)) if tag else None

def extract_rating(soup):
    tag = soup.select_one('p.star-rating')
    classes = tag.get('class', []) if tag else []
    mapping = {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5}
    for cls in classes:
        if cls in mapping:
            return mapping[cls]
    return None

def extract_price_data(soup):
    """Extracts price excluding, including tax, tax, and availability."""
    data = {}
    table = soup.select_one('table.table.table-striped')
    if table:
        for tr in table.select('tr'):
            header = tr.select_one('th').get_text(strip=True)
            value = tr.select_one('td').get_text(strip=True)
            if header == 'Price (excl. tax)':
                data['price excluding tax'] = clean_price(value)
            elif header == 'Price (incl. tax)':
                data['price including tax'] = clean_price(value)
            elif header == 'Tax':
                data['tax'] = clean_price(value)
            elif header == 'Availability':
                in_stock, quantity = extract_stock(value)
                data['stock availability'] = in_stock
                data['quantity'] = quantity
    return data




# ----------------------
# Main Extraction Functions


def extract_product_data(product_url):
    """Extracts all attributes of a product."""
    soup = get_soup(product_url)
    if not soup:
        return None
    attributes = {
        'title': extract_title(soup),
        'description': extract_description(soup),
        'category': extract_category(soup),
        'rating': extract_rating(soup),
    }
    attributes.update(extract_price_data(soup))
    
    return attributes

def extract_all_products_datas():
    """Extracts data from all products and logs missing info and progress."""
    products_urls = extract_all_products_links()
    all_products_data = []
    failures = 0
    # The global tracker for all missing attributes
    products_missing_attrs = {
        "title": {"count": 0, "urls": []},
        "price_excl_tax": {"count": 0, "urls": []},
        "price_incl_tax": {"count": 0, "urls": []},
        "tax": {"count": 0, "urls": []},
        "description": {"count": 0, "urls": []},
        "category": {"count":0, "urls":[]},
        "rating": {"count": 0, "urls": []},
        "stock_availability": {"count": 0, "urls": []},
        "quantity_available": {"count": 0, "urls": []}
    }
    for i, url in enumerate(products_urls, start=1):
        product_data = extract_product_data(url)
        
        if not product_data:
            logger.error(f"Failed to extract data for product: {url}")
            failures += 1
            if failures == 20:
                logger.error("Breaking loop: 20 consecutive failures")
                return all_products_data
            continue

        # get missing attributes for the current single product
        current_missing_attributes = [key for key, val in product_data.items() if val is None]
        # check if there's is missing attributes or not 
        if current_missing_attributes:
            # add the missing attributes in the list of all missing attributes 
            for attr in current_missing_attributes:
                products_missing_attrs[attr]['count'] += 1 
                products_missing_attrs[attr]['urls'].append(url)
                
                count = products_missing_attrs[attr]['count']
    
                # Log the individual sample for the first few times
                if count <= 5:
                    logger.warning(f"Missing {attr} for {url}")
                    if count == 5 : 
                        logger.info(f"Additional individual logs for {attr} will be hidden in a safe space")

                # 2. Alert if it becomes a systematic problem
                elif count == 20:
                    logger.error(f"ATTRIBUTE EXTRACTION FAILURE detected for {attr}. Ceasing individual logs.")
        

        all_products_data.append(product_data)
        failures = 0
        time.sleep(0.4)

        # Batch log every 100 products
        if i % 100 == 0:
            logger.info(f"{i} products have been scraped successfully")
    finalize_scraper(products_missing_attrs,len(all_products_data))
    return all_products_data

def finalize_scraper(products_missing_attrs, total_products):
    print("\n" + "="*50)
    print("        FINAL SCRAPING DIAGNOSTIC REPORT")
    print("="*50)
    
    logger.info("Generating final diagnostic report...")
    
    for attr, data in products_missing_attrs.items():
        count = data['count']
        urls = data['urls']
        success_rate = ((total_products - count) / total_products) * 100

        if count == 0:
            print(f"✅ {attr.upper():<20} | Success: {success_rate:>6.2f}% (Perfect)")
        elif count < 20:
            print(f"⚠️ {attr.upper():<20} | Success: {success_rate:>6.2f}% ({count} random gaps)")
            # Log the specific URLs to the file for manual checking
            for url in urls:
                logger.warning(f"Gap in {attr}: {url}")
        else:
            print(f"❌ {attr.upper():<20} | Success: {success_rate:>6.2f}% (SYSTEMATIC FAILURE)")
            logger.error(f"CRITICAL: {attr} selector likely broken. Failed on {count} products.")

    print("="*50)
    print(f"Scrape Complete. Total Products Processed: {total_products}")
    print("Check 'scraper_errors.log' for deep-dive details.")

def main(): 
   products_datas = extract_all_products_datas() 
   

if __name__ == '__main__' : 
    main()