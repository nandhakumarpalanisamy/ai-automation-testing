import json
import pytest
from pathlib import Path
from src.config import Config
from src.test_utils import generate_and_check_api, print_evaluation_results
from src.evaluator import evaluate_consistency

DATA_FILE = Path(__file__).parent.parent / "test_data" / "consistency_test_cases.json"
with open(DATA_FILE, "r") as f:
    test_cases = json.load(f)

@pytest.mark.parametrize("test_case", test_cases, ids=[tc["id"] for tc in test_cases])
def test_consistency(test_case):
    question = test_case["question"]
    responses = []
    
    for i in range(Config.CONSISTENCY_RUNS):
        responses.append(generate_and_check_api(question))
        
    try:
        is_successful, results = evaluate_consistency(question, responses)
    except Exception as e:
        pytest.fail(f"API/INFRASTRUCTURE FAILURE: Evaluator API error: {e}")
        
    print_evaluation_results(test_case["id"], question, "\n".join(responses), "Semantically consistent runs", results)
    
    assert is_successful, f"AI QUALITY FAILURE for {test_case['id']}: Responses are inconsistent."
