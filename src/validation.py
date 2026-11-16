
import json

from jsonschema import validate, ValidationError


# ==================================================
# 1. ALLOWED CLASSIFICATION LABELS
# ==================================================

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


# ==================================================
# 2. REQUIRED OUTPUT SCHEMA
# ==================================================

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
                    "items": {
                        "type": "string",
                        "minLength": 1
                    },
                    "uniqueItems": True
                },

                "amounts": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1
                    },
                    "uniqueItems": True
                },

                "dates": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1
                    },
                    "uniqueItems": True
                },

                "reference_numbers": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1
                    },
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
            "required": [
                "intent",
                "outcome"
            ],
            "properties": {
                "intent": {
                    "type": ["string", "null"],
                    "minLength": 1
                },

                "outcome": {
                    "type": ["string", "null"],
                    "minLength": 1
                }
            }
        }
    }
}


# ==================================================
# 3. CUSTOM VALIDATION EXCEPTION
# ==================================================

class OutputValidationError(Exception):
    """Raised when AI output fails validation."""

    pass


# ==================================================
# 4. TRANSCRIPT MARKER DETECTION
# ==================================================

def is_transcript_marker(value):
    """
    Identify bracketed transcript markers.

    Examples:
    [call disconnected]
    [silence]
    [noise]

    These markers can support an outcome but cannot
    establish the intent of a conversation.
    """

    value = value.strip()

    return (
        value.startswith("[")
        and value.endswith("]")
    )


# ==================================================
# 5. JSON PARSING
# ==================================================

def parse_json(raw_output):
    """
    Parse the AI response into a Python dictionary.

    Reject invalid JSON and non-object responses.
    """

    if not isinstance(raw_output, str):
        raise OutputValidationError(
            "AI output must be a string."
        )

    try:
        data = json.loads(raw_output)

    except json.JSONDecodeError as error:
        raise OutputValidationError(
            f"Invalid JSON: {error}"
        ) from error

    if not isinstance(data, dict):
        raise OutputValidationError(
            "AI output must be a JSON object."
        )

    return data


# ==================================================
# 6. SCHEMA VALIDATION
# ==================================================

def validate_schema(data):
    """
    Validate required fields, data types,
    allowed labels and JSON structure.
    """

    try:
        validate(
            instance=data,
            schema=OUTPUT_SCHEMA
        )

    except ValidationError as error:
        raise OutputValidationError(
            f"Schema validation failed: {error.message}"
        ) from error


# ==================================================
# 7. DETAIL VERIFICATION
# ==================================================

def validate_details(data, transcript):
    """
    Verify that every extracted detail appears
    exactly as written in the original transcript.
    """

    detail_categories = [
        "names",
        "amounts",
        "dates",
        "reference_numbers"
    ]

    for category in detail_categories:

        values = data["details"][category]

        for value in values:

            if value not in transcript:

                raise OutputValidationError(
                    f"Invented or incorrectly copied detail "
                    f"in {category}: {value}"
                )


# ==================================================
# 8. EVIDENCE VERIFICATION
# ==================================================

def validate_evidence(data, transcript):
    """
    Verify evidence word for word.

    Intent and outcome evidence are checked separately.

    Transcript markers such as [call disconnected]
    may support an outcome but cannot establish intent.
    """

    evidence_fields = [
        "intent",
        "outcome"
    ]

    for evidence_type in evidence_fields:

        evidence_sentence = data["evidence"][evidence_type]

        # Null is permitted when evidence is unavailable.
        if evidence_sentence is None:
            continue

        # Check exact word-for-word presence.
        if evidence_sentence not in transcript:

            raise OutputValidationError(
                f"Evidence verification failed for "
                f"{evidence_type}: {evidence_sentence}"
            )

        # Special rule for intent evidence.
        if (
            evidence_type == "intent"
            and is_transcript_marker(evidence_sentence)
        ):

            raise OutputValidationError(
                "Transcript markers cannot support intent. "
                "Use null when no clear conversational purpose "
                "exists."
            )


# ==================================================
# 9. MAIN VALIDATION FUNCTION
# ==================================================

def parse_and_validate(raw_output, transcript):
    """
    Complete validation pipeline.

    Step 1: Parse JSON.
    Step 2: Validate JSON schema.
    Step 3: Verify extracted details.
    Step 4: Verify evidence word for word.
    Step 5: Return validated data.
    """

    if not isinstance(transcript, str):

        raise OutputValidationError(
            "Transcript must be a string."
        )

    # Step 1: Parse JSON
    data = parse_json(raw_output)

    # Step 2: Validate structure and labels
    validate_schema(data)

    # Step 3: Verify all extracted details
    validate_details(
        data,
        transcript
    )

    # Step 4: Verify evidence
    validate_evidence(
        data,
        transcript
    )

    # Step 5: Return validated result
    return data
