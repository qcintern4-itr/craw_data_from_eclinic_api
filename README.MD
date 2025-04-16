#   eClinic Data Crawler

This project is designed to automate the process of collecting, parsing, and exporting medical encounter data from an API, based on a list of patient IDs provided in a CSV file. Selenium is used to authenticate and extract cookies/tokens required for API requests.

---

##  📁 Project Structure

```
api_crawler/
├── read_data_csv.py        # Reads the input CSV file
├── get_cookies_token.py    # Uses Selenium to extract authentication cookies and token
├── data_collector.py       # Calls the API to collect raw data
├── parse_response.py       # Parses response text to extract meaningful information
└── export_table.py         # Merges and processes data into final CSV format

output/
└── encounter.csv           # Final merged data exported as CSV

run.py                      # Main entry point to run the entire pipeline
config.py                   # Contains constant configuration variables
```

##  🚀 How to Run

You can run the full data extraction pipeline using the `run.py` script. The script accepts the following command-line arguments:

- `--from_date`: Start date in format `MM/DD/YYYY`
- `--to_date`: End date in format `MM/DD/YYYY`
- `--csv_file`: Path to the input CSV file containing patient IDs

### 🖥️ Example Command:

```
python run.py --from_date 4/10/2025 --to_date 4/10/2025 --csv_file data/patientid_10_4_25.csv

```

##  📌 Notes
- Make sure you have all required dependencies installed (e.g. selenium, pandas, requests, etc.).

- The encounter.csv file will be generated in the output/ folder containing the merged and processed data.

##  🛠️ Technologies Used
- Python

- Selenium for web automation

- Selenium Wire – for capturing and modifying HTTP requests/responses

- Requests for API calls

- Pandas for data manipulation

