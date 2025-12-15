from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.api.main import app
import os
import json

client = TestClient(app)

def test_llm_fallback_logic():
    # 1. Create a dummy PDF that produces NO regex matches
    # We can assume loading works (tested in P1), here we care about the logic flow.
    # But integration test needs a real file.
    
    file_path = "data/complex_invoice.pdf"
    
    # Just reuse sample invoice but mock the RegexExtractor to fail
    existing_file = "data/sample_invoice.pdf"
    
    if not os.path.exists(existing_file):
        print("[SKIP] sample_invoice.pdf missing")
        return

    print("Testing LLM Fallback Logic...")
    
    # Mocking RegexExtractor to return None for critical fields
    with patch("app.api.main.RegexExtractor") as MockRegex:
        instance = MockRegex.return_value
        instance.extract_all.return_value = {
            "total_amount": None, # Force fallback
            "date": None,
            "method": "regex"
        }
        
        # Mocking LLMExtractor to return valid data
        with patch("app.extraction.llm_extractor.LLMExtractor") as MockLLM:
            llm_instance = MockLLM.return_value
            llm_instance.client = True # Pretend we have an API Key
            llm_instance.extract.return_value = {
                "total_amount": 9999.99,
                "date": "2024-01-01",
                "vendor": "Mocked AI Vendor"
            }
            
            with open(existing_file, "rb") as f:
                response = client.post(
                    "/extract",
                    files={"file": ("complex_invoice.pdf", f, "application/pdf")}
                )
            
            data = response.json()
            print(f"Response: {data}")
            
            # Assertions
            if data["total_amount"] == 9999.99:
                 print("[PASS] Fallback used LLM value")
            else:
                 print(f"[FAIL] Expected 9999.99, got {data.get('total_amount')}")

            if "llm_fallback" in data["method"]:
                 print("[PASS] Method indicates fallback")
            else:
                 print(f"[FAIL] Method string missing fallback: {data['method']}")

if __name__ == "__main__":
    test_llm_fallback_logic()
