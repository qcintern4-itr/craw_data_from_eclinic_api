import argparse
from api_crawler.export_tables import merge_df_csv

parser = argparse.ArgumentParser(description="Run data extraction with custom dates and CSV file.")
parser.add_argument("--from_date", required=True, help="Start date in format MM/DD/YYYY")
parser.add_argument("--to_date", required=True, help="End date in format MM/DD/YYYY")
parser.add_argument("--csv_file", required=True, help="Path to the input CSV file")

args = parser.parse_args()

merge_df_csv(args.from_date, args.to_date, args.csv_file)
