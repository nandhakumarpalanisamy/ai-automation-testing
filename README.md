# AI Model Testing Framework

A production-quality mini-project for AI Model Testing using Python, DeepEval, and Pytest.
This framework evaluates the responses of one AI model (Model Under Test) using a second AI model as an LLM judge (Evaluator).

## Project Structure
- `src/`: Source code for configurations and core logic.
- `tests/`: Pytest test cases and evaluation metrics.
- `test_data/`: Input data for testing.
- `reports/`: Test execution reports.
- `config/`: Additional configuration files if needed.

## Setup Instructions

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`.
   - Update `.env` with your actual model names and API keys.
   - Do NOT commit the `.env` file!

4. **Run Tests**:
   - Run a single test case: `venv\Scripts\pytest.exe tests/test_chatbot.py -v -s -k TC001`
   - Run all test cases: `venv\Scripts\pytest.exe tests/test_chatbot.py -v -s`

## DeepEval Integration Architecture
This framework integrates **DeepEval** to assess the quality of the primary model's responses.
1. **Model Under Test (Model 1)**: Accepts the user's question and generates a response.
2. **Evaluator Model (Model 2)**: Acts as the "LLM Judge" via DeepEval using a custom `DeepEvalBaseLLM` wrapper.

## Evaluation Metrics
We use the following metrics, configured with a default threshold of **0.7** in `.env`:
1. **AnswerRelevancyMetric**: Ensures the answer is relevant to the question.
2. **FaithfulnessMetric**: Verifies that the answer is factually grounded in the provided context.
3. **GEval (Correctness)**: Checks if the output aligns with the expected answer.

## Test Cases Format
Defined in `test_data/test_cases.json`, each test includes: `id`, `question`, `expected_answer`, `context`, and `category`.
