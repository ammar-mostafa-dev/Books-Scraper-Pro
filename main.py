from OutputData import output_data 
from logging_config import setup_logger

logger = setup_logger(__name__)

# Force clear log file 
open("scraper.log", "w").close()

def main() : 
    logger.info('Scraper Started')
    output_data()

if __name__ == '__main__' : 
    main()