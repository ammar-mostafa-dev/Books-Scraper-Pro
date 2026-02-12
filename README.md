# 📚 Professional Web Scraper: High-Resilience Data Pipeline

A robust Python-based scraping solution built to extract 1,000+ entries with 100% crash recovery. Designed for real-world reliability where others fail.

### 📊 [Download 1,000+ Item Sample Dataset (Excel)](./books_data.xlsx)
*Direct proof of extraction: Verified dataset including UPCs, Prices, and Stock availability with 100% data density.*

---

## 🎯 Why This Engine?
Most scrapers fail during long runs due to network drops or "silent errors." This engine is built to eliminate those risks:

* **Total Data Transparency:** Receive a full diagnostic "Health Report" showing the success rate of every field (Price, Stock, UPC, etc.).
* **Zero-Loss Validation:** Automatically identifies and logs specific URLs that failed validation for easy manual review.
* **Audit-Ready Logs:** Every action is timestamped, providing a clear paper trail of the entire extraction process.
* **Clean-Data Guarantee:** Integrated character-repair logic (Regex/HTML unescape) ensures descriptions are delivered ready-to-use.

## 🛠️ The Problems I Solved
* **Data Persistence:** Implemented a **checkpoint system**. If the system crashes, it resumes instantly without duplicating data.
* **Dirty Data Management:** Created an engine to fix character encoding issues (e.g., repairing `â€™` symbols and broken HTML).
* **Fault Tolerance:** Built "Retry & Skip" logic to prevent one corrupted page from hanging the entire 1,000+ item process.

## 🚀 Technical Features
* **Modular Architecture:** Separate components for link discovery, data extraction, and output management.
* **Smart Quoting:** Uses `csv.QUOTE_ALL` to ensure commas in descriptions never break your spreadsheet structure.
* **Memory Efficient:** Uses Python generators (`yield`) to handle massive datasets with minimal RAM usage.

## 🏗️ Tech Stack
* **Python 3.10+**
* **BeautifulSoup4 & Requests:** Optimized HTTP communication and parsing.
* **Pandas:** For final data validation and high-fidelity Excel (`.xlsx`) exports.
* **Logging:** Dual-stream logging (Live console feedback + Permanent file logs).

## 📊 How to Run
1. **Clone:** `git clone https://github.com/ammar-mostafa-dev/Books-Scraper-Pro.git`
2. **Install:** `pip install -r requirements.txt`
3. **Execute:** `python main.py`
4. **Result:** Review the final report in `books_data.xlsx`,`books_data.csv`.
