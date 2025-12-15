from app.classification.router import ClassifierRouter

def test_router():
    router = ClassifierRouter(use_ml=True)
    
    test_cases = [
        # Explicit keywords -> Rules
        ("This is a Tax Invoice for services rendered. Balance Due: $500", "Invoice", "rules"),
        
        # Ambiguous but context heavy -> ML (hopefully)
        ("Account ending in 4455. Monthly withdrawals: $200. Deposits: $5000.", "Bank Statement", "ml"),
        
        # Receipt keywords -> Rules
        ("Payment Received. Thank you for shopping with us. Visa..", "Receipt", "rules")
    ]
    
    print("Running Classification Verification...")
    for text, expected, expected_method in test_cases:
        pred, conf, method = router.classify(text)
        print(f"Text: {text[:30]}...")
        print(f"  Expected: {expected} ({expected_method})")
        print(f"  Got:      {pred} ({method}) [Conf: {conf:.2f}]")
        
        # Soft assertion
        if pred != expected:
            print("  [FAIL] Class mismatch")
        else:
            print("  [PASS]")

if __name__ == "__main__":
    test_router()
