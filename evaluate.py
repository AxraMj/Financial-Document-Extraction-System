import os
import json
from typing import List, Dict, Any
from app.api.main import classifier, RegexExtractor
# Note: In real world we would use the full pipeline.
# Here we verify the components we have: Classifier and Regex.

# Mock Ground Truth
GROUND_TRUTH = [
    {
        "text": "Invoice #123. Date: 2023-01-01. Total: $500.00",
        "type": "Invoice",
        "expected_data": {"total_amount": 500.0, "date": "2023-01-01"}
    },
    {
        "text": "Payment Receipt. Thank you. Paid $20.00 on 12/12/2023.",
        "type": "Receipt",
        "expected_data": {"total_amount": 20.0, "date": "12/12/2023"}
    },
    {
        "text": "Bank Statement. Ending Balance $1000.00.",
        "type": "Bank Statement",
        "expected_data": {"total_amount": None, "date": None} # None expected by Regex here
    }
]

def calculate_metrics(results: List[Dict[str, Any]], field: str):
    tp = 0
    fp = 0
    fn = 0
    
    for res in results:
        pred = res["predicted"].get(field)
        actual = res["actual"].get(field)
        
        # Simple Exact Match logic for float/string
        if pred == actual:
            if pred is not None:
                tp += 1
            # else: True Negative (ignore for precision/recall typically or count as match?)
        else:
            if pred is None and actual is not None:
                fn += 1
            elif pred is not None and actual is None:
                fp += 1
            else:
                # Mismatch
                fp += 1
                fn += 1 # Is this double counting? 
                # Strict: It's a False Positive (wrong value) AND False Negative (missed correct value)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision, recall, f1

def run_evaluation():
    print("Running Evaluation on Mock Dataset...")
    
    extraction_results = []
    clf_correct = 0
    
    for case in GROUND_TRUTH:
        text = case["text"]
        
        # 1. Classify
        pred_type, _, _ = classifier.classify(text)
        if pred_type == case["type"]:
            clf_correct += 1
            
        # 2. Extract
        extractor = RegexExtractor(text)
        data = extractor.extract_all()
        
        extraction_results.append({
            "predicted": data,
            "actual": case["expected_data"]
        })

    # Report
    print(f"\nClassification Accuracy: {clf_correct / len(GROUND_TRUTH):.1%}")
    
    p_amt, r_amt, f1_amt = calculate_metrics(extraction_results, "total_amount")
    print(f"Total Amount -> Precision: {p_amt:.2f}, Recall: {r_amt:.2f}, F1: {f1_amt:.2f}")
    
    p_date, r_date, f1_date = calculate_metrics(extraction_results, "date")
    print(f"Date         -> Precision: {p_date:.2f}, Recall: {r_date:.2f}, F1: {f1_date:.2f}")

if __name__ == "__main__":
    run_evaluation()
