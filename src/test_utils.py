import pytest
from src.clients import generate_answer

# Global storage for test results
GLOBAL_TEST_RESULTS = []

def record_test_result(test_id, category, question, generated_answer, expected, results, status, error_message=""):
    """Records the test execution details for the final report."""
    GLOBAL_TEST_RESULTS.append({
        "test_id": test_id,
        "category": category,
        "question": question,
        "response": generated_answer,
        "expected": expected,
        "metrics": results,
        "status": status,
        "error_message": error_message
    })

def generate_and_check_api(question: str) -> str:
    """Generates an answer and directly handles API failures to avoid duplicate Pytest code."""
    generated_answer = generate_answer(question)
    if generated_answer.startswith("Error generating answer") or generated_answer == "An unexpected error occurred.":
        raise Exception(f"API/INFRASTRUCTURE FAILURE: {generated_answer}")
    return generated_answer

def print_evaluation_results(test_id: str, question: str, generated_answer: str, expected_context: str, results: dict):
    """Utility to format and print AI evaluation results for Pytest logs."""
    print(f"\n--- AI QUALITY FAILURE / REPORT ---")
    print(f"Test ID: {test_id}")
    print(f"Question: {question}")
    print(f"Model Response: {generated_answer}")
    print(f"Expected Context/Behavior: {expected_context}")
    if results:
        for metric_name, result in results.items():
            print(f"Metric Name: {metric_name}")
            print(f"Metric Score: {result.get('score')}")
            print(f"Evaluation Reason: {result.get('reason')}")

