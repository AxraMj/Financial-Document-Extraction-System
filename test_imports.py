try:
    print("Importing config...")
    import app.core.config
    print("Importing cleaner...")
    import app.preprocessing.cleaner
    print("Importing regex...")
    import app.extraction.regex_extractor
    print("Importing loader...")
    import app.ingestion.loader
    print("Importing rules...")
    import app.classification.rules
    print("Importing ml_model...")
    import app.classification.ml_model
    print("Importing router...")
    import app.classification.router
    print("Importing llm_extractor...")
    import app.extraction.llm_extractor
    print("Importing schemas...")
    import app.api.schemas
    print("Importing main...")
    import app.api.main
    print("All imports successful")
except Exception as e:
    print(f"Import failed: {e}")
except SyntaxError as e:
    print(f"Syntax Error in import: {e}")
