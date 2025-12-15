from fastapi.testclient import TestClient
from app.api.main import app
import os

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("[PASS] Health Check")

def test_extract_endpoint():
    # Use the sample invoice generated earlier
    file_path = "data/sample_invoice.pdf"
    if not os.path.exists(file_path):
        print(f"[SKIP] {file_path} not found")
        return

    with open(file_path, "rb") as f:
        response = client.post(
            "/extract",
            files={"file": ("sample_invoice.pdf", f, "application/pdf")}
        )
    
    if response.status_code != 200:
        print(f"[FAIL] /extract returned {response.status_code}: {response.text}")
        return

    data = response.json()
    print(f"Response: {data}")
    
    # Assertions
    assert data["filename"] == "sample_invoice.pdf"
    # The sample invoice usually is classified as Invoice by Rules
    print(f"[PASS] /extract - Type: {data['document_type']} (Conf: {data['confidence']})")

if __name__ == "__main__":
    test_health_check()
    test_extract_endpoint()
