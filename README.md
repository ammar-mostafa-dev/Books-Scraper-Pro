# Books to Scrape - Professional Data Extraction System

A robust, modular web scraping solution built in Python to extract comprehensive book data from the "Books to Scrape" platform. This project is designed with a focus on **reliability**, **data integrity**, and **professional logging**, making it a production-ready example for freelance data extraction gigs.

##  Key Features
- **Full Data Extraction:** Scrapes titles, categories, star ratings, full descriptions, and detailed pricing (including/excluding tax).
- **Automated Pagination:** Dynamically discovers and traverses all catalogue pages.
- **Resilient Error Handling:** Implements custom retry logic and connection timeout management to prevent script crashes.
- **Advanced Data Cleaning:** Uses `html` and `re` modules to fix encoding issues (mojibake) and sanitize text data before export.
- **Multi-Format Export:** Automatically generates cleaned data in both **CSV** and **Excel** formats using Pandas.
- **Professional Logging:** Maintains a persistent `scraper.log` to track progress and identify missing data points in real-time.

##  Project Architecture
The project is split into specialized modules for better maintainability:
- `main.py`: The central controller that initiates the scraping process.
- `ProductsLinksExtractor.py`: Handles site navigation and URL discovery.
- `ProductsDataExtractor.py`: Performs deep parsing and data sanitization.
- `OutputData.py`: Manages data structuring and file exports.
- `logging_config.py`: Standardizes logging formats across all modules.



##  Installation & Setup
1. **Clone the repository.**
2. **Install requirements:**
   ```bash
   pip install -r requirements.txt

   