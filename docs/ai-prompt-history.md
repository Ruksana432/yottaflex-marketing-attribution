# Development Process and AI Assistance Record

## 1. Project ownership and responsibility

This project was developed through individual engineering work, including requirement analysis, implementation, debugging, testing, validation, and documentation.

I was responsible for working through the project requirements, organizing the repository, running the pipeline locally, reviewing outputs, investigating issues, and checking whether the implementation behaved as expected.

ChatGPT was used as a supporting tool for selected technical questions, implementation guidance, debugging suggestions, and documentation assistance. AI-generated suggestions were treated as assistance to review and verify, not as a replacement for understanding or testing the project.

## 2. Development and verification work

The development process covered the following areas:

- **Requirements and architecture:** Organizing the marketing attribution and anomaly detection pipeline into data generation, database, validation, attribution, reporting, and evaluation components.
- **Data engineering:** Working with synthetic marketing entities, CSV files, relational database tables, identifiers, and data relationships.
- **Attribution:** Implementing and checking first-touch, last-touch, and linear attribution, including revenue reconciliation.
- **Data quality:** Running checks for duplicate identifiers, invalid references, and inconsistent opportunity/order data.
- **Anomaly detection:** Testing detection logic for duplicate revenue, post-conversion touchpoints, currency mismatches, missing campaign costs, and unsupported identity links.
- **Reporting and evaluation:** Generating campaign ROI reports, creating chronological evaluation splits, and reviewing anomaly evaluation metrics.
- **Testing:** Running the data validation scripts, attribution validation, anomaly evaluation, and automated unit tests.
- **Repository and documentation:** Organizing project files, maintaining documentation, and publishing the repository to GitHub.

## 3. Use of ChatGPT

ChatGPT assisted with technical explanations, implementation approaches, troubleshooting, interpreting test results, and improving documentation.

The development workflow included running commands locally and reviewing their actual outputs. The reported validation results are based on those executions, not on unverified claims from an AI response.

The available conversation history should be used to recover the exact prompts submitted to ChatGPT. The categories below are a summary of the assistance areas, not verbatim prompts.

### Prompt categories

1. Understanding the project requirements and planning the implementation.
2. Designing synthetic marketing data and relational database structures.
3. Developing and troubleshooting data generation and loading scripts.
4. Implementing data-quality and relationship validation checks.
5. Implementing and validating attribution models.
6. Developing anomaly detection checks and comparing findings against injected ground truth.
7. Generating ROI reports and chronological evaluation splits.
8. Interpreting automated test results and improving project documentation.
9. Using Git and GitHub to manage and publish the project.

## 4. Verification results

The following results were observed during local execution:

- Data validation completed with an overall PASS.
- Attribution validation reported zero revenue mismatches for the three attribution models.
- Five expected anomaly types were detected.
- Evaluation against five injected synthetic anomaly cases reported five true positives, zero false positives, and zero false negatives.
- Four automated unit tests passed.

These results apply to the implemented checks and the small synthetic evaluation set. They do not establish performance on real-world marketing data.

## 5. Transparency and limitations

This document is a summary of the development process and AI assistance. It is not yet a verified, exhaustive transcript of every prompt submitted.

The available conversation history should be reviewed to add the original prompts wherever they can be recovered. Any unrecoverable prompts should be identified honestly rather than reconstructed and presented as exact quotations.

The project should be evaluated on the implementation, reasoning, testing, and limitations that I can explain and demonstrate.
