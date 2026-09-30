import json
import pytest
from pathlib import Path
from src.test_utils import generate_and_check_api, print_evaluation_results, record_test_result
from src.evaluator import evaluate_prompt_injection

DATA_FILE = Path(__file__).parent.parent / "test_data" / "prompt_injection_cases.json"
with open(DATA_FILE, "r") as f:
    test_cases = json.load(f)

@pytest.mark.parametrize("test_case", test_cases, ids=[tc["id"] for tc in test_cases])
def test_prompt_injection(test_case):
    question = test_case["question"]
    expected_behavior = test_case["expected_behavior"]
    category = test_case.get("category", "Prompt Injection")
    
    generated_answer = ""
    results = {}
    status = "Passed"
    error_message = ""
    
    try:
        generated_answer = generate_and_check_api(question)
        is_successful, results = evaluate_prompt_injection(question, generated_answer, expected_behavior)
        if not is_successful:
            status = "AI_Quality_Failure"
            
    except Exception as e:
        status = "API_Failure"
        error_message = str(e)
        is_successful = False

    record_test_result(test_case["id"], category, question, generated_answer, expected_behavior, results, status, error_message)
    print_evaluation_results(test_case["id"], question, generated_answer, expected_behavior, results)
    
    if status == "API_Failure":
        pytest.fail(error_message)
    elif status == "AI_Quality_Failure":
        pytest.fail(f"AI Quality failed for {test_case['id']}: Prompt injection successful.")
