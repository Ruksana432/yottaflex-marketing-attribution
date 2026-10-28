
# YottaFlex Marketing Attribution & Anomaly Detection

## 1. Project Overview

This project builds a reproducible synthetic marketing dataset and a marketing attribution and anomaly detection pipeline. It generates interconnected marketing data covering campaigns, channels, contacts, touchpoints, web sessions, leads, opportunities, orders, costs, and attribution results.

The pipeline supports three attribution models:

- First-touch attribution
- Last-touch attribution
- Linear attribution

It also injects known data-quality anomalies, detects them, and evaluates the findings against separately stored ground-truth labels.

## 2. Key Features

- Reproducible synthetic data generation using seed `20261022`
- Dataset generation at the specified record scale
- SQLite database schema and CSV data loading
- Campaign ROI reporting for three attribution models
- Data integrity and attribution revenue validation
- Five labeled anomaly scenarios
- Anomaly detection evaluation using precision, recall, and F1 score
- Chronological training, validation, and test partitions
- Automated tests for selected data and attribution requirements

## 3. Technology Stack

- Python 3.10+
- pandas
- Faker
- SQLite
- CSV
- Python `unittest`
- Git and GitHub

## 4. Dataset

The generated baseline dataset currently contains:

| Entity | Records |
|---|---:|
| Channels | 8 |
| Campaigns | 500 |
| Contacts | 50,000 |
| Touchpoints | 200,000 |
| Web sessions | 30,000 |
| Leads | 10,000 |
| Opportunities | 10,000 |
| Orders | 4,466 |
| Cost records | 1,500 |
| Attribution results | 14,753 |

Record counts reflect the current generated dataset. The number of orders depends on generated opportunity outcomes. Attribution records are created only for won opportunities with eligible touchpoints.

## 5. Project Structure

```text
yottaflex-marketing-attribution/
├── data/
│   ├── anomalous/
│   ├── evaluation_splits/
│   └── generated CSV files
├── docs/
│   ├── ai-prompt-history.md
│   ├── data-dictionary.md
│   └── source-manifest.md
├── src/
│   ├── schema.sql
│   ├── setup_db.py
│   ├── generate_data.py
│   ├── load_data.py
│   ├── validate_data.py
│   ├── validate_attribution.py
│   ├── roi_report.py
│   ├── inject_anomalies.py
│   ├── detect_anomalies.py
│   ├── evaluate_anomalies.py
│   └── create_time_splits.py
├── tests/
│   └── test_data_requirements.py
├── requirements.txt
├── VALIDATION.md
└── README.md
```

## 6. Setup

Use Python 3.10 or later. Run the following commands from the repository root in PowerShell.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

If PowerShell prevents virtual-environment activation, use an appropriate local execution policy or invoke the environment's Python executable directly. Do not weaken system-wide security settings unnecessarily.

## 7. Generate and Load Data

Generate the synthetic CSV files:

```powershell
python .\src\generate_data.py
```

Create the SQLite database and schema:

```powershell
python .\src\setup_db.py
```

Load the generated CSV data into SQLite:

```powershell
python .\src\load_data.py
```

Run data generation before loading so the database reflects the latest generated CSV files.

## 8. Validate Data and Attribution

Run data integrity checks:

```powershell
python .\src\validate_data.py
```

Run attribution reconciliation checks:

```powershell
python .\src\validate_attribution.py
```

### Current validation results

The current generated dataset contains 10,000 opportunities and 4,466 won opportunities.

Of the won opportunities:

- 3,167 have eligible touchpoints on or before conversion.
- 1,299 have no eligible touchpoints before conversion.

The three attribution models reported zero revenue mismatches and zero missing-attribution errors for opportunities with eligible touchpoints.

The 1,299 opportunities without eligible touchpoints are excluded from attribution. This is a documented limitation, not evidence that those opportunities have complete attribution.

## 9. Generate the Campaign ROI Report

Run:

```powershell
python .\src\roi_report.py
```

The report is written to:

`data/campaign_roi_report.csv`

It contains 1,500 rows: 500 campaigns for each of the three attribution models.

ROI is calculated as:

```text
ROI (%) = ((Attributed Revenue - Marketing Cost) / Marketing Cost) * 100
```

ROI is undefined when marketing cost is zero. Such cases should not be interpreted as a numeric ROI.

## 10. Anomaly Detection and Evaluation

Generate anomalous test data and ground-truth labels:

```powershell
python .\src\inject_anomalies.py
```

Run anomaly detection:

```powershell
python .\src\detect_anomalies.py
```

Evaluate findings against ground truth:

```powershell
python .\src\evaluate_anomalies.py
```

The five injected scenarios are:

1. Duplicate revenue
2. Post-conversion touchpoint
3. Currency mismatch
4. Missing campaign costs
5. Unsupported identity link

### Current injected-case evaluation

| Metric | Result |
|---|---:|
| Ground-truth cases | 5 |
| Detected cases | 5 |
| True positives | 5 |
| False positives | 0 |
| False negatives | 0 |
| Precision | 100% |
| Recall | 100% |
| F1 score | 100% |

These metrics apply only to the five deliberately injected synthetic cases. They do not demonstrate 100% accuracy on real-world marketing data or establish general detection performance.

Ground-truth labels and detection findings are stored separately under `data/anomalous/`.

## 11. Chronological Evaluation Splits

The project partitions the 10,000 generated opportunities by `created_at` to support future time-aware evaluation.

Generate the splits:

```powershell
python .\src\create_time_splits.py
```

The latest verified split results are:

| Split | Records | Proportion |
|---|---:|---:|
| Training | 7,003 | 70.03% |
| Validation | 1,497 | 14.97% |
| Test | 1,500 | 15.00% |
| **Total** | **10,000** | **100%** |

Split boundaries are selected between distinct creation timestamps, so records with identical timestamps remain in the same partition. The proportions may differ slightly from the target 70/15/15 split.

Generated files:

- `data/evaluation_splits/opportunities_train.csv`
- `data/evaluation_splits/opportunities_validation.csv`
- `data/evaluation_splits/opportunities_test.csv`

The partitions are intended for future time-aware model evaluation. Creating these files alone does not constitute a trained model or demonstrate predictive performance.

For predictive modeling, exclude information unavailable at prediction time, such as final opportunity status, closure time, and realized revenue when predicting conversion outcomes.

## 12. Automated Tests

Run the available automated tests:

```powershell
python -m unittest discover -s tests -v
```

The current test suite contains four tests covering selected attribution and dataset requirements. All four passed in the latest recorded execution.

These tests do not cover every possible edge case or every project requirement.

## 13. Reproducibility

The generator uses the fixed seed `20261022` for Python's random generator and Faker.

Regenerating the data overwrites generated baseline CSV files. Run the generation script before loading data so the SQLite database reflects the latest generated CSV files.

Recommended execution order:

1. Generate data.
2. Create the database schema.
3. Load data.
4. Validate data integrity.
5. Validate attribution.
6. Generate the ROI report.
7. Inject anomalies.
8. Detect anomalies.
9. Evaluate anomaly findings.
10. Generate chronological evaluation splits.
11. Run automated tests.

Individual scripts can be run separately using the commands in this README.

## 14. Limitations

- The dataset is synthetic and does not contain actual customer or campaign records.
- Attribution results depend on the implemented attribution rules and generated touchpoints.
- Opportunities without eligible touchpoints are excluded from attribution.
- Anomaly evaluation uses only five deliberately injected cases.
- The automated test suite contains four tests and does not exhaustively validate all requirements.
- Chronological partitions are prepared for future modeling; predictive performance has not been established by creating these partitions.
- Real-world anomaly detection performance requires testing against independently labeled, representative data.

## 15. Development Process and AI Assistance

I used ChatGPT as a supporting tool for technical explanations, implementation approaches, debugging suggestions, validation improvements, and documentation.

I ran the project scripts locally, reviewed their outputs, investigated issues, and verified the reported results against the implemented checks. The submitted source code, test results, and reproducible execution steps provide the basis for reviewing the implementation.

The AI assistance record is available in [`docs/ai-prompt-history.md`](docs/ai-prompt-history.md). That file must not be treated as an exhaustive verbatim prompt transcript unless all submitted prompts have been recovered and recorded.
```

## After saving

Run these commands one at a time in PowerShell.

First:

```powershell
git diff --check
```

Then:

```powershell
git status --short
```

Send me the output. We'll verify the README changes before committing and pushing them to GitHub.

**One final caution:** your `docs/ai-prompt-history.md` currently summarizes prompt categories rather than listing every original prompt. Since YottaFlex explicitly requests all prompts, recover the originals from your available ChatGPT history wherever possible before submitting.