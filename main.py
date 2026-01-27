# main.py
import ProductsDataExtractor as datas_extractor
import ProductsLinksExtractor as links_extractor
import OutputData as output
from logging_config import setup_logger 

logger = setup_logger(__name__)

def main():
    # Get already done urls 
    already_done_urls = output.get_already_scraped_urls()
    # if the scraper csv file has urls (there was scraped products) then log that the scraper has been resumed and get remaining links to extract
    if already_done_urls : 
        logger.info(f'Scraper Resumed ({len(already_done_urls)}) Products have been already scraped')
        # filter links to visit 
        all_links = links_extractor.extract_all_products_links()
        links_to_visit = [link for link in all_links if link not in already_done_urls]
    else : 
        # Force Clear the logging file since it's the start of the program 
        open("scraper.log", "w").close()
        logger.info('Scraper Started')
        # if the scraper has just started ,visit each link in the website products page
    
        links_to_visit = links_extractor.extract_all_products_links()
    
    
    # loop through the generator
    for product in datas_extractor.extract_all_products_datas(links_to_visit):
        # Pass the product data to the output module
        output.save_row_to_csv(product)
    # show the results of the scraper 
    output.finalize_report()
    # Initialize the excel file as a copy of the csv after finishing to extract all products datas and showing the final data extraction process results
    output.convert_csv_to_excel()
    logger.info('Successfully Outputted Data To Csv')
if __name__ == "__main__":
    main()