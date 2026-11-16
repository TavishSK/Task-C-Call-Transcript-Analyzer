
# Task C: Call Transcript Analyzer

A Python-based command-line application that analyses
customer contact-centre call transcripts using a locally
running language model through Ollama.

The application generates structured JSON summaries,
classifications, extracted details, next actions and
supporting evidence.

The system is designed to minimize hallucinations through
JSON Schema validation, bounded retries and exact
transcript evidence verification.

## 1. Features

- Local AI inference using Ollama.
- Qwen 2.5 3B language model.
- Payment, renewal, complaint, callback and other
  intent classification.
- Resolved, unresolved, callback_requested and unclear
  outcome classification.
- Customer name, amount, date and reference extraction.
- Structured JSON output.
- JSON Schema validation.
- Maximum two retries per transcript by default.
- Configurable request timeout.
- Word-for-word evidence verification.
- Duplicate extracted detail normalization.
- Execution logging and latency measurements.
- Evaluation against expected development answers.
- Baseline and improved experiment comparison.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Local language model runtime | Ollama |
| Language model | Qwen 2.5 3B |
| HTTP communication | Requests |
| JSON validation | jsonschema |
| Evaluation | Custom Python script |
| Version control | Git |

## 3. Requirements

- macOS, Linux or Windows.
- Python 3.
- Ollama installed and running.
- Sufficient RAM and storage for the selected model.

## 4. Installation

### Step 1: Install Ollama

Download Ollama:

https://ollama.com/download

Install and start the Ollama application.

### Step 2: Download the model

Run:

```bash
ollama pull qwen2.5:3b
```

Verify the installation:

```bash
ollama list
```

### Step 3: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project:

```bash
cd Task-C-Call-Transcript-Analyzer
```

### Step 4: Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### Step 5: Install Python dependencies

```bash
pip install -r requirements.txt
```

Ensure the Ollama application is running and its
local API is accessible at:

http://localhost:11434

## 5. Project Structure

```text
Task-C-Call-Transcript-Analyzer/
│
├── data/
│   ├── transcripts.json
│   └── gold_answers.json
│
├── src/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── validation.py
│   └── evaluate.py
│
├── prompts/
│   └── system_prompt.txt
│
├── outputs/
│   ├── results_baseline.json
│   ├── results_improved.json
│   ├── results_experiment3.json
│   ├── evaluation_metrics.json
│   └── execution logs and failure records
│
├── reports/
│   ├── evaluation_report.md
│   └── failure_analysis.md
│
├── tests/
│
├── DAY1_PREDICTION.md
├── README.md
├── requirements.txt
└── .gitignore
```

## 6. Running the Application

Make sure Ollama is running.

Activate the Python virtual environment.

Run the analyzer:

```bash
python -m src.analyzer data/transcripts.json
```

The application processes every transcript and prints
the generated JSON results.

The default output is:

```text
outputs/results.json
```

Additional files include:

- outputs/failures.json
- outputs/run_metadata.json
- outputs/analyzer.log

### Command-line options

Specify another output file:

```bash
python -m src.analyzer data/transcripts.json \
  --output outputs/custom_results.json
```

Specify a different model:

```bash
python -m src.analyzer data/transcripts.json \
  --model qwen2.5:3b
```

Change the timeout:

```bash
python -m src.analyzer data/transcripts.json \
  --timeout 120
```

Change the retry count:

```bash
python -m src.analyzer data/transcripts.json \
  --retries 2
```

The retry count cannot exceed two.

For a small preliminary test:

```bash
python -m src.analyzer data/transcripts.json --limit 1
```

## 7. Output Structure

Every successful analysis contains:

- summary
- intent
- outcome
- details
  - names
  - amounts
  - dates
  - reference_numbers
- next_action
- evidence
  - intent
  - outcome

The output is validated against the required JSON schema.

Extracted details and non-null evidence values
are also verified against the original transcript.

## 8. Validation and Retry Mechanism

The application uses:

1. JSON parsing.
2. JSON Schema validation.
3. Allowed-label validation.
4. Extracted detail verification.
5. Duplicate detail normalization.
6. Exact evidence verification.
7. Bounded retries with request timeouts.

If all attempts fail, a fallback response is returned
and the failure is recorded for manual review.

## 9. Evaluation

The evaluation script compares generated outputs
against the expected development answers.

Run:

```bash
python -m src.evaluate
```

The evaluation calculates:

- Intent accuracy.
- Outcome accuracy.
- Correct extracted details.
- Missed extracted details.
- Invented extracted details.
- Word-for-word evidence share.
- Evidence coverage.
- JSON/schema failure rate.
- Final analysis failure rate.
- Latency p50.
- Latency p95.

Generated files:

```text
outputs/evaluation_metrics.json
reports/evaluation_report.md
```

The evaluation uses the archived baseline,
improved-prompt and third-experiment results.

## 10. Experiments and Results

Three experiments were conducted.

The baseline achieved the strongest measured
classification performance.

| Metric | Baseline | Improved Prompt | Experiment 3 |
|---|---:|---:|---:|
| Intent accuracy | 76.92% | 69.23% | 61.54% |
| Outcome accuracy | 76.92% | 61.54% | 46.15% |
| Correct details | 31 | 28 | 21 |
| Missed details | 11 | 14 | 21 |
| Invented details | 3 | 4 | 1 |
| Final analysis failures | 1 | 4 | 5 |

The later prompt experiments did not improve overall
classification performance.

The evaluation and failure analysis reports document
the observed problems and attempted solutions.

## 11. Limitations

- Small local models may struggle with nuanced
  conversation classification.
- Hinglish and multilingual extraction can be inconsistent.
- Exact evidence generation can fail even when
  the classification is correct.
- Schema validity does not guarantee semantic accuracy.
- Some transcripts require manual review.
- Further evaluation is necessary before production use.

## 12. Development Principles

- Treat transcripts as untrusted data.
- Never invent missing information.
- Preserve exact extracted values.
- Verify supporting evidence.
- Record failures rather than concealing them.
- Evaluate against independent expected answers.
- Document unsuccessful experiments honestly.

## 13. Author

Developed as part of the Task C:
Call Transcript Analyzer assignment.
