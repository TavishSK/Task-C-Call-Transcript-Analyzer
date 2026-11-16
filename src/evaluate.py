
import json
from pathlib import Path


# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
REPORT_DIR = ROOT / "reports"

DETAIL_CATEGORIES = [
    "names",
    "amounts",
    "dates",
    "reference_numbers"
]

# Each experiment has its own saved outputs.
EXPERIMENTS = [
    {
        "name": "Baseline",
        "results": "results_baseline.json",
        "failures": "failures_baseline.json",
        "metadata": "run_metadata_baseline.json"
    },
    {
        "name": "Improved Prompt",
        "results": "results_improved.json",
        "failures": "failures_improved.json",
        "metadata": "run_metadata_improved.json"
    },
    {
        "name": "Experiment 3",
        "results": "results_experiment3.json",
        "failures": "failures_experiment3.json",
        "metadata": "run_metadata_experiment3.json"
    }
]


# ==================================================
# 2. JSON FILE HELPERS
# ==================================================

def load_json(path):
    """Load a JSON file."""

    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}"
        )

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON file: {path}: {error}"
        ) from error


def save_json(path, data):
    """Save structured data as formatted JSON."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


# ==================================================
# 3. METRIC HELPERS
# ==================================================

def calculate_percentage(correct, total):
    """Calculate percentage safely."""

    if total == 0:
        return 0.0

    return round(
        (correct / total) * 100,
        2
    )


def format_metric(correct, total):
    """Format a metric as count and percentage."""

    percentage = calculate_percentage(
        correct,
        total
    )

    return f"{correct}/{total} ({percentage}%)"


def get_values(data, category):
    """Return extracted details as a set."""

    values = data.get(category, [])

    if not isinstance(values, list):
        return set()

    return {
        value
        for value in values
        if isinstance(value, str)
    }


# ==================================================
# 4. CLASSIFICATION EVALUATION
# ==================================================

def evaluate_classification(
    predictions,
    gold_answers,
    failed_ids
):
    """
    Compare predicted intent and outcome
    against the expected answers.

    Failed analyses are counted as incorrect,
    even if the fallback label happens to match.
    """

    intent_correct = 0
    outcome_correct = 0

    transcript_results = []

    for index, gold in enumerate(gold_answers):

        prediction = predictions[index]
        transcript_id = gold["id"]

        failed = transcript_id in failed_ids

        predicted_intent = prediction.get("intent")
        predicted_outcome = prediction.get("outcome")

        expected_intent = gold["intent"]
        expected_outcome = gold["outcome"]

        correct_intent = (
            not failed
            and predicted_intent == expected_intent
        )

        correct_outcome = (
            not failed
            and predicted_outcome == expected_outcome
        )

        if correct_intent:
            intent_correct += 1

        if correct_outcome:
            outcome_correct += 1

        transcript_results.append({
            "id": transcript_id,
            "predicted_intent": predicted_intent,
            "expected_intent": expected_intent,
            "intent_correct": correct_intent,
            "predicted_outcome": predicted_outcome,
            "expected_outcome": expected_outcome,
            "outcome_correct": correct_outcome,
            "analysis_failed": failed
        })

    total = len(gold_answers)

    return {
        "intent": {
            "correct": intent_correct,
            "total": total,
            "accuracy_percent": calculate_percentage(
                intent_correct,
                total
            )
        },

        "outcome": {
            "correct": outcome_correct,
            "total": total,
            "accuracy_percent": calculate_percentage(
                outcome_correct,
                total
            )
        },

        "transcripts": transcript_results
    }


# ==================================================
# 5. DETAIL EXTRACTION EVALUATION
# ==================================================

def evaluate_details(predictions, gold_answers):
    """
    Compare extracted details against expected details.

    Correct:
    Present in both prediction and expected answer.

    Missed:
    Present in expected answer but absent in prediction.

    Invented:
    Present in prediction but absent in expected answer.
    """

    results = {}

    total_correct = 0
    total_missed = 0
    total_invented = 0

    transcript_differences = []

    for category in DETAIL_CATEGORIES:

        correct = 0
        missed = 0
        invented = 0

        for index, gold in enumerate(gold_answers):

            prediction = predictions[index]

            expected_values = get_values(
                gold["details"],
                category
            )

            predicted_values = get_values(
                prediction.get("details", {}),
                category
            )

            correct_values = (
                expected_values & predicted_values
            )

            missed_values = (
                expected_values - predicted_values
            )

            invented_values = (
                predicted_values - expected_values
            )

            correct += len(correct_values)
            missed += len(missed_values)
            invented += len(invented_values)

            if missed_values or invented_values:

                transcript_differences.append({
                    "id": gold["id"],
                    "category": category,
                    "correct": sorted(correct_values),
                    "missed": sorted(missed_values),
                    "invented": sorted(invented_values)
                })

        results[category] = {
            "correct": correct,
            "missed": missed,
            "invented": invented
        }

        total_correct += correct
        total_missed += missed
        total_invented += invented

    results["overall"] = {
        "correct": total_correct,
        "missed": total_missed,
        "invented": total_invented
    }

    return results, transcript_differences


# ==================================================
# 6. EVIDENCE VERIFICATION EVALUATION
# ==================================================

def evaluate_evidence(
    predictions,
    gold_answers,
    transcripts
):
    """
    Measure whether non-null evidence strings appear
    word for word in their original transcripts.

    Also measure evidence coverage to avoid rewarding
    a model that returns null for every evidence field.
    """

    exact_count = 0
    submitted_count = 0

    total_possible_fields = len(predictions) * 2

    evidence_errors = []

    for index, gold in enumerate(gold_answers):

        prediction = predictions[index]
        transcript = transcripts[index]["transcript"]

        evidence = prediction.get("evidence", {})

        for field in ["intent", "outcome"]:

            value = evidence.get(field)

            if value is None:
                continue

            submitted_count += 1

            is_exact = (
                isinstance(value, str)
                and value in transcript
            )

            if is_exact:
                exact_count += 1

            else:
                evidence_errors.append({
                    "id": gold["id"],
                    "field": field,
                    "evidence": value
                })

    return {
        "exact": exact_count,
        "submitted": submitted_count,
        "exact_share_percent": calculate_percentage(
            exact_count,
            submitted_count
        ),
        "coverage_percent": calculate_percentage(
            submitted_count,
            total_possible_fields
        ),
        "total_possible_fields": total_possible_fields,
        "errors": evidence_errors
    }


# ==================================================
# 7. FAILURE AND JSON VALIDATION METRICS
# ==================================================

def evaluate_failures(failures, total):
    """
    Calculate final unresolved analysis failures.

    JSON/schema failures are separated from
    detail and evidence verification failures.
    """

    failed_ids = set()

    json_schema_failures = []

    failure_details = []

    for failure in failures:

        transcript_id = failure.get("id")
        error = failure.get("error", "")

        if transcript_id:
            failed_ids.add(transcript_id)

        if (
            error.startswith("Invalid JSON:")
            or error.startswith("Schema validation failed:")
        ):
            json_schema_failures.append(failure)

        failure_details.append({
            "id": transcript_id,
            "attempts": failure.get("attempts", 0),
            "error": error
        })

    return {
        "failed_count": len(failed_ids),

        "analysis_failure_rate_percent":
            calculate_percentage(
                len(failed_ids),
                total
            ),

        "json_schema_failure_count":
            len(json_schema_failures),

        "json_schema_failure_rate_percent":
            calculate_percentage(
                len(json_schema_failures),
                total
            ),

        "failed_transcripts": sorted(failed_ids),
        "failure_details": failure_details
    }


# ==================================================
# 8. EVALUATE ONE EXPERIMENT
# ==================================================

def evaluate_experiment(
    experiment,
    transcripts,
    gold_answers
):
    """Evaluate one complete experiment."""

    results_path = (
        OUTPUT_DIR / experiment["results"]
    )

    failures_path = (
        OUTPUT_DIR / experiment["failures"]
    )

    metadata_path = (
        OUTPUT_DIR / experiment["metadata"]
    )

    predictions = load_json(results_path)
    failures = load_json(failures_path)
    metadata = load_json(metadata_path)

    total = len(gold_answers)

    if not (
        isinstance(predictions, list)
        and isinstance(failures, list)
    ):
        raise ValueError(
            f"Invalid result or failure structure "
            f"for {experiment['name']}."
        )

    if len(predictions) != total:
        raise ValueError(
            f"{experiment['name']}: expected "
            f"{total} predictions, found {len(predictions)}."
        )

    if len(transcripts) != total:
        raise ValueError(
            "Transcript and gold-answer counts do not match."
        )

    failed_ids = set(
        failure.get("id")
        for failure in failures
    )

    classification = evaluate_classification(
        predictions,
        gold_answers,
        failed_ids
    )

    details, detail_differences = evaluate_details(
        predictions,
        gold_answers
    )

    evidence = evaluate_evidence(
        predictions,
        gold_answers,
        transcripts
    )

    failure_metrics = evaluate_failures(
        failures,
        total
    )

    metrics = {
        "experiment": experiment["name"],
        "total_transcripts": total,
        "classification": classification,
        "details": details,
        "detail_differences": detail_differences,
        "evidence": evidence,
        "failures": failure_metrics,
        "performance": {
            "successful": metadata.get("successful", 0),
            "failed": metadata.get("failed", 0),
            "total_retries": metadata.get(
                "total_retries", 0
            ),
            "latency_p50_seconds": metadata.get(
                "latency_p50_seconds", 0
            ),
            "latency_p95_seconds": metadata.get(
                "latency_p95_seconds", 0
            )
        }
    }

    return metrics


# ==================================================
# 9. MARKDOWN REPORT GENERATION
# ==================================================

def generate_report(all_metrics):
    """Generate a human-readable evaluation report."""

    lines = [
        "# Task C: Call Transcript Analyzer",
        "",
        "## Evaluation Report",
        "",
        "This report compares the development experiments "
        "against the supplied expected answers.",
        "",
        "## 1. Experiment comparison",
        "",
        "| Metric | Baseline | Improved Prompt | Experiment 3 |",
        "|---|---:|---:|---:|"
    ]

    def metric_value(metrics, section, key):
        item = metrics[section][key]

        return (
            f"{item['correct']}/{item['total']} "
            f"({item['accuracy_percent']}%)"
        )

    def detail_value(metrics, key):
        return metrics["details"]["overall"][key]

    def evidence_value(metrics):
        evidence = metrics["evidence"]

        return (
            f"{evidence['exact']}/"
            f"{evidence['submitted']} "
            f"({evidence['exact_share_percent']}%)"
        )

    def coverage_value(metrics):
        return (
            f"{metrics['evidence']['coverage_percent']}%"
        )

    def failure_value(metrics):
        return (
            f"{metrics['failures']['failed_count']}/"
            f"{metrics['total_transcripts']} "
            f"({metrics['failures']['analysis_failure_rate_percent']}%)"
        )

    def json_failure_value(metrics):
        return (
            f"{metrics['failures']['json_schema_failure_count']}/"
            f"{metrics['total_transcripts']} "
            f"({metrics['failures']['json_schema_failure_rate_percent']}%)"
        )

    rows = [
        (
            "Intent accuracy",
            lambda m: metric_value(
                m, "classification", "intent"
            )
        ),
        (
            "Outcome accuracy",
            lambda m: metric_value(
                m, "classification", "outcome"
            )
        ),
        (
            "Correct details",
            lambda m: str(detail_value(m, "correct"))
        ),
        (
            "Missed details",
            lambda m: str(detail_value(m, "missed"))
        ),
        (
            "Invented details",
            lambda m: str(detail_value(m, "invented"))
        ),
        (
            "Word-for-word evidence",
            evidence_value
        ),
        (
            "Evidence coverage",
            coverage_value
        ),
        (
            "Final analysis failure rate",
            failure_value
        ),
        (
            "Final JSON/schema failure rate",
            json_failure_value
        ),
        (
            "Total retries",
            lambda m: str(m["performance"]["total_retries"])
        ),
        (
            "Latency p50",
            lambda m: str(
                m["performance"]["latency_p50_seconds"]
            ) + " s"
        ),
        (
            "Latency p95",
            lambda m: str(
                m["performance"]["latency_p95_seconds"]
            ) + " s"
        )
    ]

    for label, getter in rows:

        values = [
            getter(metrics)
            for metrics in all_metrics
        ]

        lines.append(
            f"| {label} | {' | '.join(values)} |"
        )

    # Detailed transcript comparison.
    lines.extend([
        "",
        "## 2. Per-transcript classification results",
        ""
    ])

    for metrics in all_metrics:

        lines.extend([
            f"### {metrics['experiment']}",
            "",
            "| ID | Expected intent | Predicted intent | "
            "Expected outcome | Predicted outcome | Status |",
            "|---|---|---|---|---|---|"
        ])

        for item in metrics["classification"]["transcripts"]:

            status = (
                "Failed analysis"
                if item["analysis_failed"]
                else (
                    "Both correct"
                    if (
                        item["intent_correct"]
                        and item["outcome_correct"]
                    )
                    else "Accuracy error"
                )
            )

            lines.append(
                f"| {item['id']} "
                f"| {item['expected_intent']} "
                f"| {item['predicted_intent']} "
                f"| {item['expected_outcome']} "
                f"| {item['predicted_outcome']} "
                f"| {status} |"
            )

        lines.append("")

    # Detail error analysis.
    for metrics in all_metrics:

        lines.extend([
            f"## 3. Detail extraction analysis — "
            f"{metrics['experiment']}",
            ""
        ])

        for item in metrics["detail_differences"]:

            lines.append(
                f"- **{item['id']} / {item['category']}**"
            )

            lines.append(
                f"  - Correct: {item['correct']}"
            )

            lines.append(
                f"  - Missed: {item['missed']}"
            )

            lines.append(
                f"  - Invented: {item['invented']}"
            )

        lines.append("")

    # Failure analysis.
    for metrics in all_metrics:

        lines.extend([
            f"## 4. Failure analysis — {metrics['experiment']}",
            ""
        ])

        failures = metrics["failures"]["failure_details"]

        if not failures:
            lines.append("No unresolved analysis failures.")
        else:
            for failure in failures:

                lines.append(
                    f"- **{failure['id']}** "
                    f"({failure['attempts']} attempts): "
                    f"{failure['error']}"
                )

        lines.append("")

    # Methodology and limitations.
    lines.extend([
        "## 5. Evaluation methodology",
        "",
        "- Classification accuracy is measured against "
        "the supplied answer key.",
        "- Final failed analyses are counted as incorrect "
        "for classification accuracy.",
        "- Extracted details are compared using exact "
        "string matching.",
        "- Word-for-word evidence checks whether every "
        "non-null evidence value occurs exactly in the "
        "original transcript.",
        "- Evidence coverage reports how many of the "
        "possible evidence fields were populated.",
        "- JSON/schema failure rate measures unresolved "
        "JSON parsing or schema failures after retries.",
        "- Final analysis failure rate also includes "
        "detail and evidence verification failures.",
        "- p50 and p95 latency are taken from the "
        "analyzer's recorded run metadata.",
        "- Next-action quality requires manual review "
        "and is not scored through exact text matching.",
        "",
        "## 6. Important limitations",
        "",
        "A word-for-word evidence match does not by itself "
        "prove that the sentence semantically supports "
        "the selected label. Such support requires "
        "human review.",
        "",
        "A zero final JSON/schema failure rate does not "
        "mean no retry attempts encountered invalid "
        "responses. It means no unresolved final "
        "JSON/schema failures were recorded.",
        "",
        "## 7. Final observations",
        "",
        "Use the comparison and failure tables above to "
        "identify which experiment performed best. "
        "Do not assume that a higher technical validation "
        "success rate automatically means higher "
        "classification or extraction accuracy."
    ])

    return "\n".join(lines)


# ==================================================
# 10. MAIN FUNCTION
# ==================================================

def main():

    print("\nCALL TRANSCRIPT EVALUATION")
    print("=" * 50)

    # Load original dataset and expected answers.
    transcripts = load_json(
        DATA_DIR / "transcripts.json"
    )

    gold_answers = load_json(
        DATA_DIR / "gold_answers.json"
    )

    transcript_ids = [
        item["id"]
        for item in transcripts
    ]

    gold_ids = [
        item["id"]
        for item in gold_answers
    ]

    if transcript_ids != gold_ids:
        raise ValueError(
            "Transcript IDs and gold-answer IDs "
            "must be in the same order."
        )

    all_metrics = []

    # Evaluate all saved experiments.
    for experiment in EXPERIMENTS:

        print(
            f"\nEvaluating: {experiment['name']}..."
        )

        metrics = evaluate_experiment(
            experiment,
            transcripts,
            gold_answers
        )

        all_metrics.append(metrics)

        intent = metrics["classification"]["intent"]
        outcome = metrics["classification"]["outcome"]

        print(
            f"Intent accuracy: "
            f"{format_metric(intent['correct'], intent['total'])}"
        )

        print(
            f"Outcome accuracy: "
            f"{format_metric(outcome['correct'], outcome['total'])}"
        )

        print(
            f"Final analysis failures: "
            f"{metrics['failures']['failed_count']}"
        )

    # Save complete metrics.
    metrics_path = (
        OUTPUT_DIR / "evaluation_metrics.json"
    )

    save_json(
        metrics_path,
        {
            "experiments": all_metrics
        }
    )

    # Generate and save the Markdown report.
    report = generate_report(all_metrics)

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = (
        REPORT_DIR / "evaluation_report.md"
    )

    report_path.write_text(
        report,
        encoding="utf-8"
    )

    print("\n" + "=" * 50)
    print("EVALUATION COMPLETED")
    print("=" * 50)

    print(
        f"Metrics saved to: {metrics_path}"
    )

    print(
        f"Report saved to: {report_path}"
    )


if __name__ == "__main__":
    main()
