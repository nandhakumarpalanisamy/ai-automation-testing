from openai import OpenAI, OpenAIError
from src.config import Config

def get_model_under_test_client():
    """Create and return an OpenAI client for the model under test."""
    base_url = Config.MODEL_UNDER_TEST_BASE_URL
    if base_url and "console.groq.com" in base_url:
        print("Warning: MODEL_UNDER_TEST_BASE_URL is a web console URL. Falling back to Groq API endpoint.")
        base_url = "https://api.groq.com/openai/v1"
    elif not base_url:
        base_url = "https://api.groq.com/openai/v1"
        
    return OpenAI(
        api_key=Config.MODEL_UNDER_TEST_API_KEY,
        base_url=base_url
    )

def get_evaluator_client():
    """Create and return an OpenAI client for the evaluator model."""
    base_url = Config.EVALUATOR_BASE_URL
    if base_url and "console.groq.com" in base_url:
        print("Warning: EVALUATOR_BASE_URL is a web console URL. Falling back to Groq API endpoint.")
        base_url = "https://api.groq.com/openai/v1"
    elif not base_url:
        base_url = "https://api.groq.com/openai/v1"
        
    return OpenAI(
        api_key=Config.EVALUATOR_API_KEY,
        base_url=base_url
    )

def generate_answer(question: str) -> str:
    """Sends a question to the AI model under test and returns its response."""
    client = get_model_under_test_client()
    try:
        response = client.chat.completions.create(
            model=Config.MODEL_UNDER_TEST_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        print(f"API Error in generate_answer: {e}")
        return f"Error generating answer: {e}"
    except Exception as e:
        print(f"Unexpected error in generate_answer: {e}")
        return "An unexpected error occurred."

def evaluate_answer(prompt: str) -> str:
    """Sends an evaluation prompt to the evaluator model and returns its response."""
    client = get_evaluator_client()
    try:
        response = client.chat.completions.create(
            model=Config.EVALUATOR_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a strict and objective AI judge."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        print(f"API Error in evaluate_answer: {e}")
        return f"Error evaluating answer: {e}"
    except Exception as e:
        print(f"Unexpected error in evaluate_answer: {e}")
        return "An unexpected error occurred."
