import json
import pytest
from pathlib import Path
from src.test_utils import generate_and_check_api, print_evaluation_results, record_test_result
from src.evaluator import evaluate_negative_test_case

DATA_FILE = Path(__file__).parent.parent / "test_data" / "negative_test_cases.json"
with open(DATA_FILE, "r") as f:
    negative_test_cases = json.load(f)

BOUNDARY_DATA_FILE = Path(__file__).parent.parent / "test_data" / "boundary_test_cases.json"
with open(BOUNDARY_DATA_FILE, "r") as f:
    boundary_test_cases = json.load(f)

@pytest.mark.parametrize("test_case", negative_test_cases, ids=[tc["id"] for tc in negative_test_cases])
def test_negative_cases(test_case):
    _run_behavior_test(test_case)

@pytest.mark.parametrize("test_case", boundary_test_cases, ids=[tc["id"] for tc in boundary_test_cases])
def test_boundary_cases(test_case):
    _run_behavior_test(test_case)

def _run_behavior_test(test_case):
    question = test_case["question"]
    expected_behavior = test_case["expected_behavior"]
    category = test_case.get("category", "Behavioral")
    
    generated_answer = ""
    results = {}
    status = "Passed"
    error_message = ""
    
    try:
        generated_answer = generate_and_check_api(question)
        is_successful, results = evaluate_negative_test_case(
            question=question,
            generated_answer=generated_answer,
            expected_behavior=expected_behavior
        )
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
        pytest.fail(f"AI Quality failed for {test_case['id']}.")
