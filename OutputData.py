import pandas as pd
from ProductsDataExtractor import extract_all_products_datas
from logging_config import setup_logger

logger = setup_logger(__name__)

def output_data():
    # Get all products data
    products_data = extract_all_products_datas()
    
    # Check if data exists
    if not products_data:
        logger.error("No data to export")
        return False
    
    # Create DataFrame
    df = pd.DataFrame(products_data)
    
    # Output to CSV
    try:
        df.to_csv('books_data.csv', index=False,encoding='utf-8-sig')
        logger.info(f"Successfully exported {len(df)} products to books_data.csv")
    except Exception as e:
        logger.error(f"Failed to export CSV: {e}")
        return False
    
    # Output to Excel
    try:
        df.to_excel('books_data.xlsx', index=False)
        logger.info(f"Successfully exported {len(df)} products to books_data.xlsx")
    except Exception as e:
        logger.error(f"Failed to export Excel: {e}")
        return False
    
    return True

