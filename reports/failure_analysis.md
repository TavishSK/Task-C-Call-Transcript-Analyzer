
# Task C: Call Transcript Analyzer
# Failure Analysis Report

## 1. Objective

This document records the incorrect predictions, validation
failures, attempted improvements and remaining limitations
observed during development.

Three experiments were conducted using the local
Qwen 2.5 3B model through Ollama.

The purpose was to improve classification accuracy,
detail extraction and evidence reliability without
hardcoding answers for individual development transcripts.

## 2. Day 1 Predictions

Before running the model, the following potential
failure cases were identified:

| Transcript | Predicted difficulty |
|---|---|
| T03 | Complaint confused with payment enquiry |
| T04 | Callback request confused with payment enquiry |
| T05 | Disconnected call incorrectly considered resolved |
| T06 | Invented information despite missing conversation |
| T07 | Uncertain payment commitment interpreted as resolved |
| T08 | Hinglish information extraction |
| T09 | Renewal confused with callback request |
| T10 | Initial payment agreement confused with final outcome |
| T13 | Multiple amounts and dates incorrectly extracted |

The initial predictions were useful for identifying
the areas requiring closer evaluation.

## 3. Experiment Results

| Metric | Baseline | Improved Prompt | Experiment 3 |
|---|---:|---:|---:|
| Intent accuracy | 76.92% | 69.23% | 61.54% |
| Outcome accuracy | 76.92% | 61.54% | 46.15% |
| Correct details | 31 | 28 | 21 |
| Missed details | 11 | 14 | 21 |
| Invented details | 3 | 4 | 1 |
| Final analysis failures | 1 | 4 | 5 |
| Total retries | 6 | 10 | 12 |
| Latency p50 | 5.43s | 7.173s | 16.992s |
| Latency p95 | 15.489s | 17.927s | 37.348s |

The baseline produced the best classification
accuracy and lowest final analysis failure rate.

The later experiments reduced some detail duplication
and unsupported extraction, but overall classification
and extraction performance deteriorated.

## 4. Individual Failure Analysis

### T03 - Incorrect Charge Complaint

Initial problem:
The model classified a complaint about an incorrect
charge as a payment enquiry.

Expected:
Intent: complaint
Outcome: unresolved

What was tried:
- Added complaint-priority classification instructions.
- Added examples distinguishing disputed charges
  from ordinary payment enquiries.
- Added duplicate detail normalization in Python.

Result:
The duplicate amount Rs 750 was successfully
deduplicated. The targeted Experiment 3 test
produced the correct intent and outcome.

Remaining issue:
The model sometimes omitted outcome evidence
even when a supporting sentence existed.

### T04 - Company Callback Request

Initial problem:
The model classified the callback arrangement
as resolved instead of callback_requested.

Expected:
Intent: callback_request
Outcome: callback_requested

What was tried:
- Added explicit callback classification rules.
- Distinguished company-initiated callbacks from
  caller-initiated future calls.
- Added exact evidence selection instructions.

Result:
The model repeatedly generated an unsupported
[call disconnected] marker.

The evidence validator correctly rejected it.

Remaining issue:
The model did not consistently use the agent's
actual callback confirmation as outcome evidence.

### T05 - Interrupted Payment Discussion

Initial problem:
The model initially classified the disconnected
payment discussion as unresolved.

Expected:
Intent: payment_enquiry
Outcome: unclear

What was tried:
Added instructions distinguishing an interrupted
conversation from a pending issue.

Result:
The improved-prompt experiment produced the
correct outcome. However, Experiment 3 again
produced unresolved.

Remaining issue:
Outcome classification remained inconsistent.

### T06 - Silence and Disconnection

Initial problem:
The model paraphrased the transcript marker
[call disconnected] as a sentence explaining
that the call had ended.

This failed exact evidence verification.

Expected:
Intent: other
Outcome: unclear
Intent evidence: null
Outcome evidence: [call disconnected]

What was tried:
- Added explicit transcript marker handling.
- Required exact copying of transcript markers.
- Added Python validation preventing transcript
  markers from supporting intent.

Result:
The targeted test passed successfully.

The final output correctly returned null for
intent evidence and the exact disconnection marker
for outcome evidence.

This was a successful improvement.

### T07 - Uncertain Payment Commitment

Initial problem:
The model needed to distinguish an uncertain
payment intention from an agreed commitment.

Expected:
Intent: payment_enquiry
Outcome: unresolved

Additional extraction problems:
- Extracted Mr Khan instead of Khan.
- Missed the relative date Friday.

What was tried:
Added instructions to remove honorifics and
extract relative dates.

Result:
Classification was correct in the baseline,
but the extraction issues were not consistently
eliminated.

### T08 - Hinglish Transcript

Initial problem:
The model struggled with Hindi written in
English letters.

Expected:
Intent: payment_enquiry
Outcome: resolved

Important expected details:
- Rajesh Nair
- Rs 3,100
- 12 October
- kal
- TXN-90817

What was tried:
- Added Hinglish interpretation instructions.
- Added examples of Hindi phrases and their meaning.
- Required preservation of original extracted values.

Result:
The improved-prompt experiment recovered the
customer name but incorrectly included the agent
name Priya and missed kal.

Experiment 3 failed evidence validation after
producing paraphrased intent evidence.

Remaining issue:
Multilingual detail extraction and evidence
selection remained unreliable.

### T09 - Renewal Cost Enquiry

Initial problem:
The caller wanted renewal information but could
not provide the policy number.

Expected:
Intent: renewal
Outcome: unresolved

What was tried:
Added distinctions between a caller saying they
will call the company later and a request for the
company to call them.

Result:
The model repeatedly generated unsupported
disconnection evidence or invented the date today.

The validator correctly rejected these values.

Remaining issue:
The model continued confusing an incomplete
renewal enquiry with a disconnected call.

### T10 - Withdrawn Payment Arrangement

Initial problem:
The caller initially agreed to pay but later
withdrew the arrangement and said they would
call back tomorrow.

Expected:
Intent: payment_enquiry
Outcome: unresolved

What was tried:
Added instructions to consider the entire
conversation and prioritize the caller's final
statement.

Result:
The baseline classified the outcome correctly.
Later experiments sometimes incorrectly classified
the call as resolved.

Remaining issue:
The model did not consistently interpret the
withdrawal of the original payment arrangement.

### T11 - Disputed Fee

Initial problem:
The model classified an unexpected fee as
a payment enquiry instead of a complaint.

Expected:
Intent: complaint
Outcome: resolved

What was tried:
- Added complaint-priority rules.
- Added instructions to select caller statements
  as intent evidence.
- Strengthened exact evidence verification.

Result:
The model continued selecting the agent's
resolution sentence as intent evidence or
paraphrasing the caller's original complaint.

The validator rejected these responses.

Remaining issue:
Correct semantic evidence selection remained
unreliable.

### T13 - Multiple Amounts and Dates

Initial problem:
The model needed to distinguish multiple
instalments and an agreed part-payment arrangement.

Expected:
Intent: payment_enquiry
Outcome: resolved

Important details:
- Rs 9,000
- Rs 6,000
- Rs 3,000
- 1 October
- 1 September
- 20 November
- today
- PP-5512

What was tried:
Added instructions to extract every distinct amount
and relative date.

Result:
Some earlier runs missed Rs 9,000 and today.
Experiment 3 eventually failed exact evidence
verification because the generated intent evidence
was not copied exactly.

Remaining issue:
Complete extraction and exact evidence selection
were not achieved consistently.

## 5. Improvements That Worked

### Duplicate Detail Normalization

Implemented deduplication of identical extracted
values while preserving their original order.

This resolved the duplicate Rs 750 schema failure
observed in T03.

### Transcript Marker Validation

Implemented a check preventing bracketed transcript
markers from being accepted as intent evidence.

This corrected the T06 evidence failure.

### Exact Evidence Verification

The validator rejects evidence that does not occur
word for word in the original transcript.

This prevented paraphrased and invented evidence
from being accepted as successful output.

## 6. Approaches That Did Not Work

### Excessively Expanded Prompt

Adding many additional classification and extraction
instructions did not consistently improve model quality.

The classification accuracy decreased across the
three experiments.

### Repeated Prompt Refinement

Repeatedly adding callback, date and evidence rules
did not reliably resolve T04, T09 and T11.

### Repeated Model Retries

Some errors persisted across all three attempts.
Retries therefore did not guarantee correction.

### Relying Only on Schema Validation

A schema-valid response could still contain incorrect
intent, outcome, names, dates or evidence.

Additional comparison against expected answers
was necessary.

## 7. Lessons Learned

1. Structured JSON does not guarantee factual accuracy.
2. Exact evidence verification is essential for preventing
   fabricated supporting statements.
3. Smaller local models can struggle with nuanced
   classification and multilingual conversations.
4. More prompt instructions do not necessarily improve
   performance.
5. Validation and retry mechanisms should be combined
   with independent evaluation.
6. Failed analyses must remain visible instead of being
   silently accepted.
7. Human review remains necessary for uncertain cases.

## 8. Production Monitoring Recommendations

For a production deployment, monitor:

- Intent and outcome accuracy using periodically reviewed
  labelled samples.
- Detail extraction omissions and invented values.
- Evidence verification failures.
- JSON and schema validation failures.
- Retry frequency and model latency.
- Changes in transcript language and conversation patterns.
- The proportion of calls requiring manual review.

Unexpected increases in classification errors, evidence
failures or manual-review cases should trigger investigation.

## 9. Final Conclusion

The experiments demonstrated that strict validation,
duplicate normalization and transcript marker handling
can address specific technical failures.

However, the expanded prompting experiments did not
produce an overall improvement in classification accuracy.

The baseline remained the strongest measured
configuration across the three experiments.

The remaining failures and limitations have been
preserved and documented rather than concealed.

Further model evaluation and human review would be
required before using the system in a real contact-centre
environment.
