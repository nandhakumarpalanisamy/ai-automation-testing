import json
import pytest
from pathlib import Path
from src.test_utils import generate_and_check_api, print_evaluation_results
from src.evaluator import evaluate_regression

DATA_FILE = Path(__file__).parent.parent / "test_data" / "regression_test_cases.json"
with open(DATA_FILE, "r") as f:
    test_cases = json.load(f)

@pytest.mark.parametrize("test_case", test_cases, ids=[tc["id"] for tc in test_cases])
def test_regression(test_case):
    question = test_case["question"]
    expected_answer = test_case["expected_answer"]
    minimum_score = test_case["minimum_score"]
    
    generated_answer = generate_and_check_api(question)
    
    try:
        is_successful, results = evaluate_regression(question, generated_answer, expected_answer, minimum_score)
    except Exception as e:
        pytest.fail(f"API/INFRASTRUCTURE FAILURE: Evaluator API error: {e}")
        
    print_evaluation_results(test_case["id"], question, generated_answer, expected_answer, results)
    
    assert is_successful, f"AI QUALITY FAILURE for {test_case['id']}: Score dropped below {minimum_score}."
