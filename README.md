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
   - *(To be implemented in Step 2)*
