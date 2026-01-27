import csv
import os
import pandas as pd
from logging_config import setup_logger 
logger = setup_logger(__name__)
def save_row_to_csv(data_dict, filename="books_data.csv"):
    """Handles the physical writing to the file"""
    # check if file exists
    file_exists = os.path.isfile(filename) and os.stat(filename).st_size > 0
    # open the file to write new data 
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        # quoting = csv.quote_all to ensure that descriptions quotes are handled correctly
        writer = csv.DictWriter(f, fieldnames=data_dict.keys(),quoting=csv.QUOTE_ALL)
        # if file has been made now then add headers to it otherwise just append the data row to the file
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_dict)



def convert_csv_to_excel(csv_filename="books_data.csv", excel_filename="books_data.xlsx"):
    """Converts the final CSV into a professional Excel file."""
    try:
        # Read the finished CSV
        df = pd.read_csv(csv_filename)
        # Export to Excel
        df.to_excel(excel_filename, index=False)
        logger.info(f"Successfully converted to Excel: {excel_filename}")
    except Exception as e:
        logger.warning(f"Excel conversion failed: {e}")


def get_already_scraped_urls(filename="books_data.csv"):
    """Reads the CSV and returns a set of URLs already scraped."""
    # if the file doesn't exist return a set
    if not os.path.exists(filename):
        return set()
    
    with open(filename, mode='r', encoding='utf-8') as f:
        # Use DictReader to specifically target the 'url' column
        reader = csv.DictReader(f)
        try:
            # get the url from each row 
            return {row['url'] for row in reader if 'url' in row}
        except KeyError:
            # if the file is empty or headers are messed up return an empty set 
            return set()
        

def finalize_report(filename="books_data.csv"):
    import pandas as pd
    import os

    if not os.path.exists(filename):
        logger.error("Report Failed: No data file found.")
        return

    try:
        df = pd.read_csv(filename)
        total_rows = len(df)
        
        # 1. Start building the report string in a list
        report_lines = [
            "", # Visual gap
            "="*50,
            f"        FINAL DATA INTEGRITY REPORT",
            f"        Total Products Processed: {total_rows}",
            "="*50
        ]

        # 2. Append each attribute's result to the list
        for column in df.columns:
            missing_count = df[column].isna().sum()
            success_rate = ((total_rows - missing_count) / total_rows) * 100
            status = "PASS" if success_rate == 100 else "WARN" if success_rate > 95 else "FAIL"
            
            report_lines.append(f" {column.upper():<20} | Success: {success_rate:>6.2f}% | {status}")

        report_lines.append("="*50)

        # 3. JOIN everything with newlines and log as ONE single message
        final_message = "\n".join(report_lines)
        logger.info(final_message)
        
    except Exception as e:
        logger.error(f"Integrity check failed: {e}")