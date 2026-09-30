import json
import pytest
from pathlib import Path
from src.clients import generate_answer
from src.evaluator import evaluate_negative_test_case

# Load test data
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
    
    # Step 1: Generate answer from Model 1
    generated_answer = generate_answer(question)
    
    # Guard against API failures from Model 1
    if generated_answer.startswith("Error generating answer") or generated_answer == "An unexpected error occurred.":
        pytest.fail(f"API/INFRASTRUCTURE FAILURE: {generated_answer}")
        
    # Step 2: Evaluate using Model 2 (DeepEval)
    try:
        is_successful, results = evaluate_negative_test_case(
            question=question,
            generated_answer=generated_answer,
            expected_behavior=expected_behavior
        )
    except Exception as e:
        pytest.fail(f"API/INFRASTRUCTURE FAILURE: Evaluator API error: {e}")
    
    # Step 3: Print and Assert success
    print(f"\n--- AI QUALITY FAILURE / REPORT ---")
    print(f"Test ID: {test_case['id']}")
    print(f"Question: {question}")
    print(f"Model Response: {generated_answer}")
    print(f"Expected Behavior: {expected_behavior}")
    for metric_name, result in results.items():
        print(f"Metric Name: {metric_name}")
        print(f"Metric Score: {result['score']}")
        print(f"Evaluation Reason: {result['reason']}")
    
    assert is_successful, f"AI QUALITY FAILURE for {test_case['id']}."
