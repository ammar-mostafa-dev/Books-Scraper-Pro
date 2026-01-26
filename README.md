# 📚 Professional Web Scraper: High-Resilience Data Pipeline

A robust Python-based scraping solution built to extract 1,000+ entries with 100% crash recovery. Unlike standard scripts, this tool is designed for the real world—where internet connections drop and hardware fails.
## 🎯 What Makes This Scraper Ideal For Your Business Data
Most scraping projects fail because of "silent errors"—data that looks correct but is missing key fields or is corrupted by character encoding. This engine is built to eliminate that risk:

Total Data Transparency: At the end of every run, you receive a full diagnostic report showing the exact success rate of every property (Price, Stock, UPC, etc.).

Zero-Loss Validation: Instead of guessing if the data is complete, the script identifies and logs the specific URLs of any products that failed validation for manual review.

Audit-Ready Logs: Every action is timestamped and categorized, providing a clear paper trail of the extraction process for your records.

Clean-Data Guarantee: Integrated character-repair logic ensures that descriptions and titles are delivered in a "ready-to-use" format, free from HTML artifacts or encoding mess.
## 🛠️ The Problems I Solved
* **Data Persistence:** Implemented a CSV-based checkpoint system. If the script is interrupted (e.g., system crash, power failure), it detects already-scraped entries and resumes instantly without duplicates.
* **Dirty Data Management:** Created a cleaning engine using Regex and HTML unescaping to handle "messy" character encodings (Fixing `â€™` symbols and broken HTML entities).
* **Fault Tolerance:** Built a "Retry & Skip" logic. If a specific product page is corrupted, the script logs the error and moves to the next, preventing the entire process from hanging.

## 🚀 Technical Features
- **Modular Architecture:** Separate components for link discovery, data extraction, and output management.
- **Smart Quoting:** Implemented `csv.QUOTE_ALL` to prevent data corruption from commas within product descriptions.
- **Diagnostic Reporting:** Generates a final "Health Report" showing the success rate for every field (Price, Rating, UPC, etc.).
- **Memory Efficient:** Uses Python generators (`yield`) to handle large datasets with minimal RAM usage.

## 🏗️ Tech Stack
- **Python 3.10+**
- **BeautifulSoup4 & Requests:** For parsing and HTTP communication.
- **Pandas:** For final data validation and Excel (`.xlsx`) report generation.
- **Logging:** Dual-stream logging (Live console feedback + Permanent file logs).

## 📊 How to Run
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the orchestrator: `python main.py`.
4. Review the final report in `books_data.xlsx`.
