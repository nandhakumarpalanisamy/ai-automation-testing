import json
import pytest
from pathlib import Path
from src.config import Config
from src.test_utils import generate_and_check_api, print_evaluation_results, record_test_result
from src.evaluator import evaluate_consistency

DATA_FILE = Path(__file__).parent.parent / "test_data" / "consistency_test_cases.json"
with open(DATA_FILE, "r") as f:
    test_cases = json.load(f)

@pytest.mark.parametrize("test_case", test_cases, ids=[tc["id"] for tc in test_cases])
def test_consistency(test_case):
    question = test_case["question"]
    category = test_case.get("category", "Consistency")
    
    responses = []
    results = {}
    status = "Passed"
    error_message = ""
    
    try:
        for i in range(Config.CONSISTENCY_RUNS):
            responses.append(generate_and_check_api(question))
            
        is_successful, results = evaluate_consistency(question, responses)
        if not is_successful:
            status = "AI_Quality_Failure"
            
    except Exception as e:
        status = "API_Failure"
        error_message = str(e)
        is_successful = False

    combined_response = "\n".join(responses)
    expected = "Semantically consistent runs"
    
    record_test_result(test_case["id"], category, question, combined_response, expected, results, status, error_message)
    print_evaluation_results(test_case["id"], question, combined_response, expected, results)
    
    if status == "API_Failure":
        pytest.fail(error_message)
    elif status == "AI_Quality_Failure":
        pytest.fail(f"AI Quality failed for {test_case['id']}: Responses are inconsistent.")
