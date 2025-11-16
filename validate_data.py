"""
validate_data.py
Simple local ETL + validation script.
Reads a CSV, checks nulls & value ranges, and exports clean data + report.
"""

import pandas as pd
import json
from pathlib import Path

def validate_csv(input_path: str, output_dir: str = "output"):
    df = pd.read_csv(input_path)

    report = {"total_rows": len(df), "columns": {}}

    # Example numeric range check
    for col in df.columns:
        nulls = df[col].isna().sum()
        dtype = str(df[col].dtype)
        report["columns"][col] = {"nulls": int(nulls), "dtype": dtype}

        # Example numeric validation
        if pd.api.types.is_numeric_dtype(df[col]):
            out_of_range = ((df[col] < 0) | (df[col] > 1e6)).sum()
            report["columns"][col]["out_of_range"] = int(out_of_range)

    # create clean version (drop NA)
    clean_df = df.dropna()
    Path(output_dir).mkdir(exist_ok=True)
    clean_path = Path(output_dir) / "clean_data.csv"
    clean_df.to_csv(clean_path, index=False)

    # write report
    report_path = Path(output_dir) / "validation_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f" Validation complete. Clean file → {clean_path}")
    return str(clean_path), str(report_path)


if __name__ == "__main__":
    validate_csv("sample_data/data.csv")
