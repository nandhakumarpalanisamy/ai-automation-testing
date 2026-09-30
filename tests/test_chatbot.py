import json
import pytest
from pathlib import Path
from src.clients import generate_answer
from src.evaluator import evaluate_test_case

# Load test data
DATA_FILE = Path(__file__).parent.parent / "test_data" / "test_cases.json"
with open(DATA_FILE, "r") as f:
    test_cases = json.load(f)

@pytest.mark.parametrize("test_case", test_cases, ids=[tc["id"] for tc in test_cases])
def test_chatbot_quality(test_case):
    question = test_case["question"]
    expected_answer = test_case["expected_answer"]
    context = test_case["context"]
    
    # Step 1: Generate answer from Model 1
    generated_answer = generate_answer(question)
    
    # Guard against API failures from Model 1. 
    # Do not treat API errors as AI quality failures.
    if generated_answer.startswith("Error generating answer") or generated_answer == "An unexpected error occurred.":
        pytest.fail(f"API execution failed: {generated_answer}")
        
    # Step 2: Evaluate using Model 2 (DeepEval)
    try:
        is_successful, results = evaluate_test_case(
            question=question,
            generated_answer=generated_answer,
            expected_answer=expected_answer,
            context=context
        )
    except Exception as e:
        pytest.fail(f"DeepEval Evaluation failed due to API error: {e}")
    
    # Step 3: Print and Assert success
    print(f"\n--- Evaluation Results for {test_case['id']} ---")
    for metric_name, result in results.items():
        print(f"{metric_name} | Score: {result['score']} | Pass: {result['success']}")
        print(f"Reason: {result['reason']}\n")
        
    assert is_successful, f"AI Quality failed for {test_case['id']}."
