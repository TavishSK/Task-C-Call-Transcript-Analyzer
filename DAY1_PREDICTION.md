
# Day 1 - Model Failure Predictions

## Objective
Identify situations where a local language model may incorrectly
classify a call transcript or extract information.

These are predictions made before running the model.

## Expected Difficult Cases

### 1. T03 - Complaint classification
The model may confuse a complaint about an incorrect charge
with a normal payment enquiry.

### 2. T04 - Callback request
The overdue instalment mentioned by the agent may cause the
model to classify the call as a payment enquiry instead of
a callback request.

### 3. T05 - Disconnected call
The model may incorrectly assume that the payment discussion
was resolved even though the transcript was cut off.

### 4. T06 - Silence and missing information
The model may invent an intent, names or other details even
though the transcript contains almost no useful information.

### 5. T07 - Uncertain payment commitment
The model may interpret the caller's willingness to try
paying as a confirmed payment commitment.

### 6. T08 - Hinglish transcript
The model may struggle with Hindi written in English letters
and miss payment information, names or relative dates.

### 7. T09 - Renewal versus callback
The model may confuse the caller's intention to call back
with a request for the company to call them back.

### 8. T10 - Withdrawn payment arrangement
The model may classify the issue as resolved because the
caller initially agreed to pay, ignoring the later withdrawal.

### 9. T13 - Multiple amounts and dates
The model may miss amounts or dates when a single conversation
contains multiple instalments and a part-payment arrangement.

## General Risks

- Hallucination of missing information.
- Incorrect extraction of agent names as customer names.
- Treating durations as dates.
- Inventing evidence sentences.
- Confusing a proposed arrangement with an agreed arrangement.
- Following instructions contained inside the transcript.

## Planned Improvements

- Use structured JSON output.
- Validate all fields and allowed labels.
- Verify evidence directly against the transcript.
- Use bounded retries.
- Evaluate predictions against the provided answers.
