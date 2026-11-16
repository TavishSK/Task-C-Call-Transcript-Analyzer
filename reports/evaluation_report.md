# Task C: Call Transcript Analyzer

## Evaluation Report

This report compares the development experiments against the supplied expected answers.

## 1. Experiment comparison

| Metric | Baseline | Improved Prompt | Experiment 3 |
|---|---:|---:|---:|
| Intent accuracy | 10/13 (76.92%) | 9/13 (69.23%) | 8/13 (61.54%) |
| Outcome accuracy | 10/13 (76.92%) | 8/13 (61.54%) | 6/13 (46.15%) |
| Correct details | 31 | 28 | 21 |
| Missed details | 11 | 14 | 21 |
| Invented details | 3 | 4 | 1 |
| Word-for-word evidence | 10/10 (100.0%) | 10/10 (100.0%) | 11/11 (100.0%) |
| Evidence coverage | 38.46% | 38.46% | 42.31% |
| Final analysis failure rate | 1/13 (7.69%) | 4/13 (30.77%) | 5/13 (38.46%) |
| Final JSON/schema failure rate | 0/13 (0.0%) | 1/13 (7.69%) | 0/13 (0.0%) |
| Total retries | 6 | 10 | 12 |
| Latency p50 | 5.43 s | 7.173 s | 16.992 s |
| Latency p95 | 15.489 s | 17.927 s | 37.348 s |

## 2. Per-transcript classification results

### Baseline

| ID | Expected intent | Predicted intent | Expected outcome | Predicted outcome | Status |
|---|---|---|---|---|---|
| T01 | payment_enquiry | payment_enquiry | resolved | resolved | Both correct |
| T02 | renewal | renewal | resolved | resolved | Both correct |
| T03 | complaint | payment_enquiry | unresolved | unresolved | Accuracy error |
| T04 | callback_request | callback_request | callback_requested | resolved | Accuracy error |
| T05 | payment_enquiry | payment_enquiry | unclear | unresolved | Accuracy error |
| T06 | other | other | unclear | unclear | Failed analysis |
| T07 | payment_enquiry | payment_enquiry | unresolved | unresolved | Both correct |
| T08 | payment_enquiry | payment_enquiry | resolved | resolved | Both correct |
| T09 | renewal | renewal | unresolved | unresolved | Both correct |
| T10 | payment_enquiry | payment_enquiry | unresolved | unresolved | Both correct |
| T11 | complaint | payment_enquiry | resolved | resolved | Accuracy error |
| T12 | other | other | resolved | resolved | Both correct |
| T13 | payment_enquiry | payment_enquiry | resolved | resolved | Both correct |

### Improved Prompt

| ID | Expected intent | Predicted intent | Expected outcome | Predicted outcome | Status |
|---|---|---|---|---|---|
| T01 | payment_enquiry | payment_enquiry | resolved | resolved | Both correct |
| T02 | renewal | renewal | resolved | resolved | Both correct |
| T03 | complaint | other | unresolved | unclear | Failed analysis |
| T04 | callback_request | other | callback_requested | unclear | Failed analysis |
| T05 | payment_enquiry | payment_enquiry | unclear | unclear | Both correct |
| T06 | other | other | unclear | unclear | Both correct |
| T07 | payment_enquiry | payment_enquiry | unresolved | unresolved | Both correct |
| T08 | payment_enquiry | payment_enquiry | resolved | resolved | Both correct |
| T09 | renewal | other | unresolved | unclear | Failed analysis |
| T10 | payment_enquiry | payment_enquiry | unresolved | resolved | Accuracy error |
| T11 | complaint | other | resolved | unclear | Failed analysis |
| T12 | other | other | resolved | resolved | Both correct |
| T13 | payment_enquiry | payment_enquiry | resolved | resolved | Both correct |

### Experiment 3

| ID | Expected intent | Predicted intent | Expected outcome | Predicted outcome | Status |
|---|---|---|---|---|---|
| T01 | payment_enquiry | payment_enquiry | resolved | resolved | Both correct |
| T02 | renewal | renewal | resolved | resolved | Both correct |
| T03 | complaint | complaint | unresolved | unresolved | Both correct |
| T04 | callback_request | other | callback_requested | unclear | Failed analysis |
| T05 | payment_enquiry | payment_enquiry | unclear | unresolved | Accuracy error |
| T06 | other | other | unclear | unclear | Both correct |
| T07 | payment_enquiry | payment_enquiry | unresolved | unresolved | Both correct |
| T08 | payment_enquiry | other | resolved | unclear | Failed analysis |
| T09 | renewal | other | unresolved | unclear | Failed analysis |
| T10 | payment_enquiry | payment_enquiry | unresolved | resolved | Accuracy error |
| T11 | complaint | other | resolved | unclear | Failed analysis |
| T12 | other | other | resolved | resolved | Both correct |
| T13 | payment_enquiry | other | resolved | unclear | Failed analysis |

## 3. Detail extraction analysis — Baseline

- **T04 / names**
  - Correct: []
  - Missed: ['Meena Iyer']
  - Invented: []
- **T07 / names**
  - Correct: []
  - Missed: ['Khan']
  - Invented: ['Mr Khan']
- **T08 / names**
  - Correct: []
  - Missed: ['Rajesh Nair']
  - Invented: []
- **T13 / names**
  - Correct: []
  - Missed: ['Dutta']
  - Invented: ['Mr Dutta']
- **T13 / amounts**
  - Correct: ['Rs 3,000', 'Rs 6,000']
  - Missed: ['Rs 9,000']
  - Invented: []
- **T04 / dates**
  - Correct: []
  - Missed: []
  - Invented: ['6 in the evening']
- **T07 / dates**
  - Correct: ['5 October']
  - Missed: ['Friday']
  - Invented: []
- **T08 / dates**
  - Correct: []
  - Missed: ['12 October', 'kal']
  - Invented: []
- **T10 / dates**
  - Correct: ['8 October']
  - Missed: ['tomorrow']
  - Invented: []
- **T13 / dates**
  - Correct: ['1 October', '1 September', '20 November']
  - Missed: ['today']
  - Invented: []
- **T10 / reference_numbers**
  - Correct: []
  - Missed: ['AC-30177']
  - Invented: []

## 3. Detail extraction analysis — Improved Prompt

- **T03 / names**
  - Correct: []
  - Missed: ['Sunil Mehta']
  - Invented: []
- **T04 / names**
  - Correct: []
  - Missed: ['Meena Iyer']
  - Invented: []
- **T07 / names**
  - Correct: []
  - Missed: ['Khan']
  - Invented: ['Mr Khan']
- **T08 / names**
  - Correct: ['Rajesh Nair']
  - Missed: []
  - Invented: ['Priya']
- **T10 / names**
  - Correct: []
  - Missed: []
  - Invented: ['Caller']
- **T11 / names**
  - Correct: []
  - Missed: ['Farah Siddiqui']
  - Invented: []
- **T13 / names**
  - Correct: []
  - Missed: ['Dutta']
  - Invented: ['Mr Dutta']
- **T03 / amounts**
  - Correct: []
  - Missed: ['Rs 750']
  - Invented: []
- **T11 / amounts**
  - Correct: []
  - Missed: ['Rs 300']
  - Invented: []
- **T07 / dates**
  - Correct: ['5 October']
  - Missed: ['Friday']
  - Invented: []
- **T08 / dates**
  - Correct: ['12 October']
  - Missed: ['kal']
  - Invented: []
- **T10 / dates**
  - Correct: ['8 October']
  - Missed: ['tomorrow']
  - Invented: []
- **T13 / dates**
  - Correct: ['1 October', '1 September', '20 November']
  - Missed: ['today']
  - Invented: []
- **T02 / reference_numbers**
  - Correct: []
  - Missed: ['HP-558210']
  - Invented: []
- **T03 / reference_numbers**
  - Correct: []
  - Missed: ['AC-44019']
  - Invented: []
- **T11 / reference_numbers**
  - Correct: []
  - Missed: ['RV-2208']
  - Invented: []

## 3. Detail extraction analysis — Experiment 3

- **T04 / names**
  - Correct: []
  - Missed: ['Meena Iyer']
  - Invented: []
- **T07 / names**
  - Correct: []
  - Missed: ['Khan']
  - Invented: ['Mr Khan']
- **T08 / names**
  - Correct: []
  - Missed: ['Rajesh Nair']
  - Invented: []
- **T11 / names**
  - Correct: []
  - Missed: ['Farah Siddiqui']
  - Invented: []
- **T13 / names**
  - Correct: []
  - Missed: ['Dutta']
  - Invented: []
- **T08 / amounts**
  - Correct: []
  - Missed: ['Rs 3,100']
  - Invented: []
- **T11 / amounts**
  - Correct: []
  - Missed: ['Rs 300']
  - Invented: []
- **T13 / amounts**
  - Correct: []
  - Missed: ['Rs 3,000', 'Rs 6,000', 'Rs 9,000']
  - Invented: []
- **T07 / dates**
  - Correct: ['5 October']
  - Missed: ['Friday']
  - Invented: []
- **T08 / dates**
  - Correct: []
  - Missed: ['12 October', 'kal']
  - Invented: []
- **T10 / dates**
  - Correct: ['8 October']
  - Missed: ['tomorrow']
  - Invented: []
- **T13 / dates**
  - Correct: []
  - Missed: ['1 October', '1 September', '20 November', 'today']
  - Invented: []
- **T08 / reference_numbers**
  - Correct: []
  - Missed: ['TXN-90817']
  - Invented: []
- **T11 / reference_numbers**
  - Correct: []
  - Missed: ['RV-2208']
  - Invented: []
- **T13 / reference_numbers**
  - Correct: []
  - Missed: ['PP-5512']
  - Invented: []

## 4. Failure analysis — Baseline

- **T06** (3 attempts): Evidence verification failed for outcome: The call ended due to disconnection.

## 4. Failure analysis — Improved Prompt

- **T03** (3 attempts): Schema validation failed: ['Rs 750', 'Rs 750'] has non-unique elements
- **T04** (3 attempts): Evidence verification failed for outcome: [call disconnected]
- **T09** (3 attempts): Evidence verification failed for outcome: [call disconnected]
- **T11** (3 attempts): Evidence verification failed for intent: The fee was applied in error. I have reversed Rs 300 and the reference is RV-2208

## 4. Failure analysis — Experiment 3

- **T04** (3 attempts): Evidence verification failed for outcome: [call disconnected]
- **T08** (3 attempts): Evidence verification failed for intent: The agent confirms a payment of Rs 3,100 due on October 12 and provides the reference number TXN-90817.
- **T09** (3 attempts): Evidence verification failed for outcome: [caller says they will call back later]
- **T11** (3 attempts): Evidence verification failed for intent: The fee was applied in error. I have reversed Rs 300 and the reference is RV-2208
- **T13** (3 attempts): Evidence verification failed for intent: I can pay Rs 3,000 today and the rest on 20 November. The reference is PP-5512

## 5. Evaluation methodology

- Classification accuracy is measured against the supplied answer key.
- Final failed analyses are counted as incorrect for classification accuracy.
- Extracted details are compared using exact string matching.
- Word-for-word evidence checks whether every non-null evidence value occurs exactly in the original transcript.
- Evidence coverage reports how many of the possible evidence fields were populated.
- JSON/schema failure rate measures unresolved JSON parsing or schema failures after retries.
- Final analysis failure rate also includes detail and evidence verification failures.
- p50 and p95 latency are taken from the analyzer's recorded run metadata.
- Next-action quality requires manual review and is not scored through exact text matching.

## 6. Important limitations

A word-for-word evidence match does not by itself prove that the sentence semantically supports the selected label. Such support requires human review.

A zero final JSON/schema failure rate does not mean no retry attempts encountered invalid responses. It means no unresolved final JSON/schema failures were recorded.

## 7. Final observations

Use the comparison and failure tables above to identify which experiment performed best. Do not assume that a higher technical validation success rate automatically means higher classification or extraction accuracy.