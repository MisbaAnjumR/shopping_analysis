# Customer Behavior Analysis

This project analyzes a dataset containing customer shopping behavior to generate insights on purchasing patterns, customer demographics, and product trends. It uses Python, SQL, and Power BI for end-to-end data processing and visualization.

## Project Structure

- `dataset.csv` - The raw customer shopping behavior dataset.
- `analysis.py` - A Python script used for data cleaning, exploration, and loading into a SQL database.
- `queries.sql` - SQL scripts for querying the data to answer key business questions.
- `run_queries.py` - Python script to execute the queries, display results in the terminal, and automatically generate a formatted PDF report (`Analysis_Report.pdf`).
## How to Run

Follow these steps to run the analysis:

1. **Install Requirements:** Make sure you have the required python packages installed (`pandas`, `sqlalchemy`, and `fpdf2`).
   ```bash
   pip install pandas sqlalchemy fpdf2
   ```

2. **Run the Analysis Script:** Execute the python script to clean the `dataset.csv` and load the data into a local SQLite database (`customer_behavior.db`).
   ```bash
   python analysis.py
   ```

3. **Query the Data & Generate PDF:** Run `run_queries.py` to automatically connect to your database, execute all queries, print insights to the terminal, and generate `Analysis_Report.pdf`:
   ```bash
   python run_queries.py
   ```

4. **Review Report:** Open the newly generated `Analysis_Report.pdf` to see the full presentation of business intelligence findings.
