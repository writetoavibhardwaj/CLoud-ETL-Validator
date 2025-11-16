import requests
import io

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200

def test_valid_csv():
    sample = b"col1,col2\n1,2\n3,4"
    files = {"file": ("sample.csv", io.BytesIO(sample), "text/csv")}
    r = requests.post(f"{BASE_URL}/validate", files=files)
    assert r.status_code == 200

def test_invalid_file_type():
    files = {"file": ("bad.txt", io.BytesIO(b"notcsv"), "text/plain")}
    r = requests.post(f"{BASE_URL}/validate", files=files)
    assert r.status_code == 415
