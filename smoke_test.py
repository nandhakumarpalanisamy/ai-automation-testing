from src.clients import generate_answer, evaluate_answer

def run_smoke_test():
    print("--- Starting AI Models Smoke Test ---")
    
    # 1. Test Model Under Test
    question = "Explain briefly how solar energy works in two sentences."
    print(f"\n[Model 1] Asking question: '{question}'")
    answer = generate_answer(question)
    print(f"[Model 1] Answer received:\n{answer}")
    
    # 2. Test Evaluator Model
    eval_prompt = f"Please evaluate this answer for accuracy: '{answer}'. Is it correct and concise? Reply with Yes or No and a short reason."
    print(f"\n[Model 2] Sending evaluation prompt: '{eval_prompt}'")
    eval_result = evaluate_answer(eval_prompt)
    print(f"[Model 2] Evaluator response:\n{eval_result}")
    
    print("\n--- Smoke Test Completed ---")

if __name__ == "__main__":
    run_smoke_test()
