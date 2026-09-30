import json
import pytest
from pathlib import Path
from src.test_utils import generate_and_check_api, print_evaluation_results
from src.evaluator import evaluate_prompt_injection

DATA_FILE = Path(__file__).parent.parent / "test_data" / "prompt_injection_cases.json"
with open(DATA_FILE, "r") as f:
    test_cases = json.load(f)

@pytest.mark.parametrize("test_case", test_cases, ids=[tc["id"] for tc in test_cases])
def test_prompt_injection(test_case):
    question = test_case["question"]
    expected_behavior = test_case["expected_behavior"]
    
    generated_answer = generate_and_check_api(question)
    
    try:
        is_successful, results = evaluate_prompt_injection(question, generated_answer, expected_behavior)
    except Exception as e:
        pytest.fail(f"API/INFRASTRUCTURE FAILURE: Evaluator API error: {e}")
        
    print_evaluation_results(test_case["id"], question, generated_answer, expected_behavior, results)
    
    assert is_successful, f"AI QUALITY FAILURE for {test_case['id']}: Prompt injection successful."
