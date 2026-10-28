
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "evaluation_splits"

# Load the opportunities dataset
df = pd.read_csv(DATA_DIR / "opportunities.csv")

# Parse dates and remove records without a valid creation date
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)
df = df.dropna(subset=["created_at"]).copy()

# Sort chronologically
df = df.sort_values("created_at").reset_index(drop=True)

# Split by time order: earliest 70%, next 15%, latest 15%
n = len(df)
train_end = int(n * 0.70)
validation_end = int(n * 0.85)

train = df.iloc[:train_end].copy()
validation = df.iloc[train_end:validation_end].copy()
test = df.iloc[validation_end:].copy()

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Save separate CSV files
train.to_csv(OUTPUT_DIR / "opportunities_train.csv", index=False)
validation.to_csv(OUTPUT_DIR / "opportunities_validation.csv", index=False)
test.to_csv(OUTPUT_DIR / "opportunities_test.csv", index=False)

# Print a summary
print("Chronological split complete")
print(f"Total records: {n}")
print(f"Training records: {len(train)}")
print(f"Validation records: {len(validation)}")
print(f"Test records: {len(test)}")

for name, split in [
    ("Training", train),
    ("Validation", validation),
    ("Test", test),
]:
    if not split.empty:
        print(
            f"{name} date range: "
            f"{split['created_at'].min()} to {split['created_at'].max()}"
        )

# Verify the time boundaries do not overlap
if not train.empty and not validation.empty:
    assert train["created_at"].max() <= validation["created_at"].min()

if not validation.empty and not test.empty:
    assert validation["created_at"].max() <= test["created_at"].min()

print("Chronological ordering checks passed.")
print(f"Files saved in: {OUTPUT_DIR}")
