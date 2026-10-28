
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "anomalous"


def main():
    truth = pd.read_csv(DATA_DIR / "ground_truth.csv")
    detected = pd.read_csv(DATA_DIR / "detected_anomalies.csv")

    # Match a finding to ground truth using anomaly type and entity ID.
    truth_keys = set(
        zip(truth["anomaly_type"], truth["entity_id"].astype(str))
    )
    detected_keys = set(
        zip(
            detected["anomaly_type"],
            detected["entity_id"].astype(str),
        )
    )

    true_positives = len(truth_keys & detected_keys)
    false_positives = len(detected_keys - truth_keys)
    false_negatives = len(truth_keys - detected_keys)

    precision = (
        true_positives / (true_positives + false_positives)
        if true_positives + false_positives else 0
    )

    recall = (
        true_positives / (true_positives + false_negatives)
        if true_positives + false_negatives else 0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    print("Anomaly Detection Evaluation")
    print("=" * 35)
    print(f"Ground-truth cases: {len(truth_keys)}")
    print(f"Detected cases: {len(detected_keys)}")
    print(f"True positives: {true_positives}")
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall:    {recall:.2%}")
    print(f"F1 score:  {f1:.2%}")

    comparison = truth.copy()
    comparison["detected"] = comparison.apply(
        lambda row: (
            row["anomaly_type"], str(row["entity_id"])
        ) in detected_keys,
        axis=1,
    )

    output = DATA_DIR / "ground_truth_evaluation.csv"
    comparison.to_csv(output, index=False)
    print(f"\nCase-by-case evaluation saved to: {output}")


if __name__ == "__main__":
    main()
