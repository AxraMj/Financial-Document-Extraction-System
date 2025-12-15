import random
from app.classification.ml_model import MLClassifier
from app.core.config import setup_logger

logger = setup_logger("trainer")

def generate_mock_data():
    """
    Generates synthetic text data for 3 classes.
    """
    data = []
    labels = []
    
    # helper
    def add(text, label, count=20):
        for _ in range(count):
            # slightly vary text? For simple BOW/TF-IDF repetition is okay but let's mix
            # noise or random words to simulate variety
            variation = text + " " + " ".join(random.choices(["ref", "id", "#", "code", "date", "customer"], k=3))
            data.append(variation)
            labels.append(label)

    # Invoices
    add("Invoice Bill To Total Amount Due Due Date Tax Details Itemized Charges", "Invoice", 50)
    add("INVOICE #001 Please pay by date. Subtotal VAT Total", "Invoice", 50)
    
    # Receipts
    add("Receipt Payment Received Thank you for your business Transaction ID Credit Card Visa", "Receipt", 50)
    add("Store Receipt Total Paid Change Due Items purchased Cashier", "Receipt", 50)
    
    # Bank Statements
    add("Bank Statement Account Summary Opening Balance Closing Balance Withdrawals Deposits", "Bank Statement", 50)
    add("Monthly Statement Account Number Transaction History Interest Earned", "Bank Statement", 50)
    
    return data, labels

def train_and_save():
    logger.info("Generating mock training data...")
    X, y = generate_mock_data()
    
    clf = MLClassifier()
    logger.info(f"Training model on {len(X)} samples...")
    clf.train(X, y)
    logger.info(f"Model saved to {clf.model_path}")

if __name__ == "__main__":
    train_and_save()
