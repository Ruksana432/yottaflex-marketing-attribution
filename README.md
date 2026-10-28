\# YottaFlex Marketing Attribution \& Anomaly Detection



\## 1. Project Overview



This project builds a reproducible synthetic marketing dataset and an attribution pipeline to evaluate marketing campaign performance. It generates campaign, channel, contact, touchpoint, lead, opportunity, order, cost, and attribution data.



It supports three attribution models:

\- First-touch attribution

\- Last-touch attribution

\- Linear attribution



It also injects known data-quality anomalies, detects them, and evaluates the findings against separately stored ground-truth labels.



\## 2. Key Features



\- Reproducible synthetic data generation using seed `20261022`

\- Marketing dataset generation at the required scale

\- SQLite database schema and CSV data loading

\- Campaign ROI reporting for three attribution models

\- Data integrity and attribution revenue validation

\- Five labeled anomaly scenarios

\- Anomaly detection evaluation with precision, recall, and F1 score



\## 3. Technology Stack



\- Python

\- pandas

\- Faker

\- SQLite

\- CSV

\- PowerShell / Windows terminal



\## 4. Dataset



The generated baseline dataset includes:



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



The number of orders depends on the generated opportunity outcomes. Attribution records are created only for won opportunities with eligible touchpoints.



\## 5. Project Structure



```text

yottaflex-marketing-attribution/

├── data/

│   ├── anomalous/

│   ├── channels.csv

│   ├── campaigns.csv

│   ├── contacts.csv

│   ├── touchpoints.csv

│   ├── web\_sessions.csv

│   ├── leads.csv

│   ├── opportunities.csv

│   ├── orders.csv

│   ├── cost\_records.csv

│   └── attribution\_results.csv

├── src/

│   ├── schema.sql

│   ├── setup\_db.py

│   ├── generate\_data.py

│   ├── load\_data.py

│   ├── validate\_data.py

│   ├── validate\_attribution.py

│   ├── roi\_report.py

│   ├── inject\_anomalies.py

│   ├── detect\_anomalies.py

│   └── evaluate\_anomalies.py

├── requirements.txt

├── VALIDATION.md

└── README.md

```



\## 6. Setup



Use Python 3.10 or later. From the project root, create and activate a virtual environment if needed.



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

```



\## 7. Generate and Load Data



Generate the synthetic CSV files:



```powershell

python .\\src\\generate\_data.py

```



Create the SQLite database and schema:



```powershell

python .\\src\\setup\_db.py

```



Load CSV data into SQLite:



```powershell

python .\\src\\load\_data.py

```



\## 8. Validate Data and Attribution



Run database integrity checks:



```powershell

python .\\src\\validate\_data.py

```



Run attribution reconciliation checks:



```powershell

python .\\src\\validate\_attribution.py

```



The current generated dataset has 4,466 won opportunities. Of these, 3,167 have eligible touchpoints and 1,299 have no touchpoints on or before conversion. All three attribution models currently report zero revenue mismatches and zero missing-attribution errors for opportunities with eligible touchpoints.



\## 9. Generate the Campaign ROI Report



```powershell

python .\\src\\roi\_report.py

```



The report is written to `data/campaign\_roi\_report.csv`. It contains 1,500 rows: 500 campaigns for each of the three attribution models.



ROI is calculated as:



`ROI (%) = ((Attributed Revenue - Marketing Cost) / Marketing Cost) \* 100`



ROI is undefined when marketing cost is zero.



\## 10. Anomaly Detection



Generate separate anomalous test data and ground-truth labels:



```powershell

python .\\src\\inject\_anomalies.py

```



Detect anomalies:



```powershell

python .\\src\\detect\_anomalies.py

```



Evaluate findings against ground truth:



```powershell

python .\\src\\evaluate\_anomalies.py

```



The five injected scenarios are:

1\. Duplicate revenue

2\. Post-conversion touchpoint

3\. Currency mismatch

4\. Missing campaign costs

5\. Unsupported identity link



In the current injected-case evaluation, all five cases were detected, with zero false positives and zero false negatives. The resulting precision, recall, and F1 score were each 100%. This measures performance on the five known injected cases and should not be interpreted as general real-world detection performance.



Ground truth is stored separately from the detected findings under `data/anomalous/`.



\## 11. Reproducibility



The generator uses the fixed seed `20261022` for Python's random generator and Faker. Regenerating the data overwrites the generated baseline CSV files.



Run the generation, loading, validation, reporting, and anomaly-evaluation scripts individually as shown above. Run the generator before loading data so the database reflects the latest CSV files.



\## 12. Limitations



\- The dataset is synthetic and does not represent actual customer or campaign records.

\- Attribution results depend on the defined attribution rules and generated touchpoints.

\- The anomaly evaluation uses five deliberately injected cases.

\- Real-world performance requires testing against independently labeled, representative data.



\## 13. AI Assistance



AI assistance was used during development to help review code, debug attribution reconciliation, improve validation logic, and prepare project documentation. The implementation and test results should be reviewed against the submitted source code.


## Chronological Evaluation Split

The project includes chronological partitions of the 10,000 generated opportunities to support time-aware evaluation.

| Split | Records | Proportion |
|---|---:|---:|
| Training | 7,000 | 70% |
| Validation | 1,500 | 15% |
| Test | 1,500 | 15% |
| **Total** | **10,000** | **100%** |

### Generate the splits

Run this command from the project root:

```powershell
python .\src\create_time_splits.py
```

The generated files are saved under `data/evaluation_splits/`:

- `opportunities_train.csv`
- `opportunities_validation.csv`
- `opportunities_test.csv`

The partitions are ordered by opportunity creation time. These files are intended for future time-aware model evaluation; creating the partitions alone does not constitute a trained model or demonstrate predictive performance.

For predictive modeling, exclude information that would not be available at prediction time, such as final opportunity status, closure time, and realized revenue when predicting conversion outcomes.

