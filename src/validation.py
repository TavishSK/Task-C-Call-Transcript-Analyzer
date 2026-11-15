
import json
from jsonschema import validate, ValidationError


# Allowed classification labels
ALLOWED_INTENTS = [
    "payment_enquiry",
    "renewal",
    "complaint",
    "callback_request",
    "other"
]

ALLOWED_OUTCOMES = [
    "resolved",
    "unresolved",
    "callback_requested",
    "unclear"
]


# Required output structure
OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "summary",
        "intent",
        "outcome",
        "details",
        "next_action",
        "evidence"
    ],
    "properties": {
        "summary": {
            "type": "string",
            "minLength": 1
        },
        "intent": {
            "type": "string",
            "enum": ALLOWED_INTENTS
        },
        "outcome": {
            "type": "string",
            "enum": ALLOWED_OUTCOMES
        },
        "details": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "names",
                "amounts",
                "dates",
                "reference_numbers"
            ],
            "properties": {
                "names": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                    "uniqueItems": True
                },
                "amounts": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                    "uniqueItems": True
                },
                "dates": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                    "uniqueItems": True
                },
                "reference_numbers": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                    "uniqueItems": True
                }
            }
        },
        "next_action": {
            "type": "string",
            "minLength": 1
        },
        "evidence": {
            "type": "object",
            "additionalProperties": False,
            "required": ["intent", "outcome"],
            "properties": {
                "intent": {
                    "type": ["string", "null"]
                },
                "outcome": {
                    "type": ["string", "null"]
                }
            }
        }
    }
}


class OutputValidationError(Exception):
    """Raised when AI output fails validation."""
    pass


def parse_and_validate(raw_output, transcript):
    """
    Parse AI output, validate its JSON schema,
    and verify extracted details and evidence.
    """

    # Check 1: Parse JSON
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as error:
        raise OutputValidationError(
            f"Invalid JSON: {error}"
        ) from error

    # Check 2: Validate required structure and labels
    try:
        validate(instance=data, schema=OUTPUT_SCHEMA)
    except ValidationError as error:
        raise OutputValidationError(
            f"Schema validation failed: {error.message}"
        ) from error

    # Check 3: Verify every extracted detail exists
    # exactly as written in the original transcript.
    for category, values in data["details"].items():
        for value in values:
            if value not in transcript:
                raise OutputValidationError(
                    f"Invented or incorrectly copied detail "
                    f"in {category}: {value}"
                )

    # Check 4: Verify evidence word for word.
    for evidence_type in ["intent", "outcome"]:
        evidence_sentence = data["evidence"][evidence_type]

        if evidence_sentence is not None:
            if evidence_sentence not in transcript:
                raise OutputValidationError(
                    f"Evidence verification failed for "
                    f"{evidence_type}: {evidence_sentence}"
                )

    return data
