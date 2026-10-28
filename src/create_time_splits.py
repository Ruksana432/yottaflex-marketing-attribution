
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "evaluation_splits"

# Load opportunities
df = pd.read_csv(DATA_DIR / "opportunities.csv")

# Parse dates and remove invalid creation dates
df["created_at"] = pd.to_datetime(
    df["created_at"], errors="coerce", utc=True
)
df = df.dropna(subset=["created_at"]).copy()

# Sort chronologically
df = df.sort_values("created_at").reset_index(drop=True)

if df.empty:
    raise ValueError("No opportunities have valid creation dates.")

# Keep identical timestamps in the same split
group_sizes = df.groupby("created_at", sort=True).size()
timestamps = group_sizes.index
cumulative_counts = group_sizes.cumsum()
n = len(df)
num_groups = len(timestamps)

if num_groups < 3:
    raise ValueError(
        "At least three distinct timestamps are required "
        "to create three chronological splits."
    )

# Select boundaries nearest to the desired 70% and 85% sizes.
# Each boundary falls between distinct timestamps.
train_cut = min(
    range(1, num_groups - 1),
    key=lambda k: abs(cumulative_counts.iloc[k - 1] - n * 0.70),
)

validation_cut = min(
    range(train_cut + 1, num_groups),
    key=lambda k: abs(cumulative_counts.iloc[k - 1] - n * 0.85),
)

train_boundary = timestamps[train_cut]
test_boundary = timestamps[validation_cut]

train = df[df["created_at"] < train_boundary].copy()
validation = df[
    (df["created_at"] >= train_boundary)
    & (df["created_at"] < test_boundary)
].copy()
test = df[df["created_at"] >= test_boundary].copy()

# Create output directory and save the splits
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

train.to_csv(OUTPUT_DIR / "opportunities_train.csv", index=False)
validation.to_csv(
    OUTPUT_DIR / "opportunities_validation.csv", index=False
)
test.to_csv(OUTPUT_DIR / "opportunities_test.csv", index=False)

# Report results
print("Chronological split complete")
print(f"Total records: {n}")

for name, split in [
    ("Training", train),
    ("Validation", validation),
    ("Test", test),
]:
    print(f"{name} records: {len(split)}")
    if not split.empty:
        print(
            f"{name} date range: "
            f"{split['created_at'].min()} to "
            f"{split['created_at'].max()}"
        )

# Verify chronological ordering and non-overlapping timestamps
assert not train.empty
assert not validation.empty
assert not test.empty
assert train["created_at"].max() < validation["created_at"].min()
assert validation["created_at"].max() < test["created_at"].min()

print("Chronological ordering checks passed.")
print("Identical timestamps are not split across datasets.")
print(f"Files saved in: {OUTPUT_DIR}")
