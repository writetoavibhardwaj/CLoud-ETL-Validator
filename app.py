from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
import io
import datetime
import sqlite3

app = FastAPI(title="Data Validator API", description="Uploads a CSV and returns summary statistics.")

# ---------- Helper Function ----------
def log_to_db(filename: str, rows: int, cols: int):
    """Logs each upload into a local SQLite database."""
    conn = sqlite3.connect("validator_log.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            rows INTEGER,
            columns INTEGER,
            upload_time TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO uploads (filename, rows, columns, upload_time)
        VALUES (?, ?, ?, ?)
    """, (filename, rows, cols, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

# ---------- Main Endpoint ----------
@app.post("/validate")
async def validate_file(file: UploadFile = File(...)):
    """Accepts a CSV file and returns basic stats + null counts."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=415, detail="Only CSV files are supported.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        summary = {
            "filename": file.filename,
            "rows": len(df),
            "columns": df.shape[1],
            "column_names": list(df.columns),
            "null_counts": df.isnull().sum().to_dict(),
            "preview": df.head(3).to_dict(orient="records")
        }

        # Log upload info
        log_to_db(file.filename, len(df), df.shape[1])

        return {"status": "success", "summary": summary}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
