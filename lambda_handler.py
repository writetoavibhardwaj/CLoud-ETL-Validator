"""
lambda_handler.py
AWS Lambda entry point wrapping validate_data.py.
For now it just calls the local function — later you can replace local I/O with S3.
"""

import json
from validate_data import validate_csv

def lambda_handler(event=None, context=None):
    # Expect 'file_path' in event
    input_path = event.get("file_path", "sample_data/data.csv") if event else "sample_data/data.csv"

    clean_file, report_file = validate_csv(input_path)
    response = {"clean_file": clean_file, "report_file": report_file}

    return {"statusCode": 200, "body": json.dumps(response)}

if __name__ == "__main__":
    print(lambda_handler({"file_path": "sample_data/data.csv"}, None))
