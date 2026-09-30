from deepeval.models import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, GEval
from src.clients import get_evaluator_client
from src.config import Config

class CustomGroqEvaluator(DeepEvalBaseLLM):
    """DeepEval custom LLM model wrapping our Groq client."""
    def __init__(self):
        self.client = get_evaluator_client()

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=Config.EVALUATOR_MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Evaluator LLM error: {e}")
            raise

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return Config.EVALUATOR_MODEL_NAME

def evaluate_test_case(question: str, generated_answer: str, expected_answer: str, context: list):
    """
    Creates an LLMTestCase and runs DeepEval metrics using the custom Groq Evaluator.
    Returns: (is_successful, results_dict)
    """
    custom_model = CustomGroqEvaluator()
    
    test_case = LLMTestCase(
        input=question,
        actual_output=generated_answer,
        expected_output=expected_answer,
        retrieval_context=context
    )
    
    # Initialize metrics
    answer_relevancy = AnswerRelevancyMetric(
        threshold=Config.THRESHOLD_ANSWER_RELEVANCY,
        model=custom_model,
        include_reason=True
    )
    faithfulness = FaithfulnessMetric(
        threshold=Config.THRESHOLD_FAITHFULNESS,
        model=custom_model,
        include_reason=True
    )
    # GEval for correctness
    correctness = GEval(
        name="Correctness",
        evaluation_steps=[
            "Determine whether the actual output is factually correct based on the expected output.",
            "Check if the actual output answers the input properly."
        ],
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
        threshold=Config.THRESHOLD_CORRECTNESS,
        model=custom_model
    )
    
    # Run metrics
    answer_relevancy.measure(test_case)
    faithfulness.measure(test_case)
    correctness.measure(test_case)
    
    # Collect results
    results = {
        "AnswerRelevancy": {
            "score": answer_relevancy.score,
            "success": answer_relevancy.is_successful(),
            "reason": answer_relevancy.reason
        },
        "Faithfulness": {
            "score": faithfulness.score,
            "success": faithfulness.is_successful(),
            "reason": faithfulness.reason
        },
        "Correctness": {
            "score": correctness.score,
            "success": correctness.is_successful(),
            "reason": correctness.reason
        }
    }
    
    # Return overall success
    overall_pass = answer_relevancy.is_successful() and faithfulness.is_successful() and correctness.is_successful()
    return overall_pass, results

def evaluate_negative_test_case(question: str, generated_answer: str, expected_behavior: str):
    """
    Evaluates negative, edge, and boundary cases by verifying the model exhibits the expected behavior.
    """
    custom_model = CustomGroqEvaluator()
    
    test_case = LLMTestCase(
        input=question,
        actual_output=generated_answer,
        expected_output=expected_behavior
    )
    
    # HallucinationResistance using GEval
    hallucination_resistance = GEval(
        name="HallucinationResistance",
        evaluation_steps=[
            "Determine whether the actual output satisfies the behavior described in the expected output.",
            "Check if the model detects false premises, avoids inventing facts, or clearly communicates uncertainty if required by the expected behavior."
        ],
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
        threshold=Config.THRESHOLD_CORRECTNESS,
        model=custom_model
    )
    
    hallucination_resistance.measure(test_case)
    
    results = {
        "HallucinationResistance": {
            "score": hallucination_resistance.score,
            "success": hallucination_resistance.is_successful(),
            "reason": hallucination_resistance.reason
        }
    }
    
    return hallucination_resistance.is_successful(), results

