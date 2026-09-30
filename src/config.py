import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    MODEL_UNDER_TEST_NAME = os.getenv("MODEL_UNDER_TEST_NAME")
    MODEL_UNDER_TEST_API_KEY = os.getenv("MODEL_UNDER_TEST_API_KEY")
    MODEL_UNDER_TEST_BASE_URL = os.getenv("MODEL_UNDER_TEST_BASE_URL")
    
    EVALUATOR_MODEL_NAME = os.getenv("EVALUATOR_MODEL_NAME")
    EVALUATOR_API_KEY = os.getenv("EVALUATOR_API_KEY")
    EVALUATOR_BASE_URL = os.getenv("EVALUATOR_BASE_URL")
    
    # DeepEval evaluation thresholds
    THRESHOLD_ANSWER_RELEVANCY = float(os.getenv("THRESHOLD_ANSWER_RELEVANCY", "0.7"))
    THRESHOLD_FAITHFULNESS = float(os.getenv("THRESHOLD_FAITHFULNESS", "0.7"))
    THRESHOLD_CORRECTNESS = float(os.getenv("THRESHOLD_CORRECTNESS", "0.7"))
    
    # Consistency test runs
    CONSISTENCY_RUNS = int(os.getenv("CONSISTENCY_RUNS", "3"))

def validate_config():
    required_vars = [
        ("MODEL_UNDER_TEST_NAME", Config.MODEL_UNDER_TEST_NAME),
        ("MODEL_UNDER_TEST_API_KEY", Config.MODEL_UNDER_TEST_API_KEY),
        ("EVALUATOR_MODEL_NAME", Config.EVALUATOR_MODEL_NAME),
        ("EVALUATOR_API_KEY", Config.EVALUATOR_API_KEY),
    ]

    missing = [name for name, val in required_vars if not val]
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

validate_config()
