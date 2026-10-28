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


## Assignment Prompt 1 — YottaFlex Project Requirements

**AI tool:** ChatGPT

**Purpose:** Understand the project requirements and plan implementation.

**Prompt record:** Full assignment text supplied by the user, covering the business context, objectives, entities and relationships, synthetic data generation, attribution models, anomaly scenarios, validation rules, acceptance criteria, and submission requirements.

**Record status:** This entry is currently a summary. The complete original assignment text should be included below when available.


### Recovered Original Prompts

#### Prompt 2 — Data generation
**AI tool:** ChatGPT

**Original prompt:**  Requested assistance with creating src/generate_data.py to generate synthetic marketing data, including channels, campaigns, contacts, touchpoints, web sessions, leads, opportunities, orders, and campaign costs. The implementation used a fixed random seed (20261022) and CSV outputs.


#### Prompt 3 — Debugging
**AI tool:** ChatGPT

**Original prompt:** Requested help investigating and fixing project issues, checking Python scripts and database operations, troubleshooting data-generation and validation problems, and resolving errors in attribution, anomaly detection, and chronological evaluation splits.

#### Database Design and Setup — Prompt Record

**AI tool:** ChatGPT

**Purpose:** Design and set up the relational database for the marketing attribution pipeline.

**Prompt summary:** Requested assistance with defining database tables and relationships, creating SQL schema definitions, setting up SQLite database operations, loading generated CSV data, and validating primary keys and foreign-key relationships.

**Verification:** Database and data-validation scripts were run locally to check record counts, identifiers, and relationships.

**Record status:** Summary of database development assistance based on available project context. This is not a verbatim transcript of the original prompts.

#### Attribution Models and ROI Reporting — Prompt Record

**AI tool:** ChatGPT

**Purpose:** Compare marketing attribution methods and calculate campaign performance.

**Prompt summary:** Requested assistance with implementing and validating first-touch, last-touch, and linear attribution models, connecting eligible marketing touchpoints to won opportunities, reconciling attributed revenue, and generating campaign ROI reports.

**Verification:** The attribution validation script reported zero revenue mismatches for the three models. The ROI report was generated for 500 campaigns across three attribution models.

**Record status:** Summary of attribution and reporting assistance based on available project context. This is not a verbatim transcript of the original prompts.
