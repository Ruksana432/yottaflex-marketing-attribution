# Data and Attribution Validation

## Dataset
- Random seed: `20261022`
- Won opportunities checked: 4,466
- Won opportunities with eligible touchpoints: 3,167
- Won opportunities without eligible touchpoints: 1,299

## Attribution Results

| Model | Revenue mismatches | Missing attribution despite eligible touchpoints |
|---|---:|---:|
| First-touch | 0 | 0 |
| Last-touch | 0 | 0 |
| Linear | 0 | 0 |

## Interpretation
All three attribution models reconcile attributed revenue to opportunity revenue for opportunities with eligible touchpoints. The 1,299 won opportunities without eligible touchpoints are excluded from attribution because no touchpoint occurred on or before conversion.

## Reproduction
Run the following commands from the project root:

```powershell
python .\src\generate_data.py
python .\src\load_data.py
python .\src\validate_attribution.py
```

The dataset is synthetic and generated with a fixed random seed. These results validate internal consistency on the generated dataset; they do not establish real-world attribution accuracy.
