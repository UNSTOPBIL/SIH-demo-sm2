import json
import os
import random
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report

def get_storage_temp_code(storage_type: str) -> int:
    st = str(storage_type).lower()
    if "frozen" in st:
        return 0
    elif "chilled" in st:
        return 1
    return 2  # ambient

def is_perishable_product(storage_type: str, respiration_class: str) -> int:
    st = str(storage_type).lower()
    rc = str(respiration_class).lower()
    if st != "ambient" or any(k in rc for k in ["high", "moderate"]):
        return 1
    return 0

def train_and_export_model():
    seed_path = os.path.join(os.path.dirname(__file__), "..", "data", "commodities_seed.json")
    model_path = os.path.join(os.path.dirname(__file__), "model.joblib")

    with open(seed_path, "r", encoding="utf-8") as f:
        commodities = json.load(f)

    print(f"[+] Loaded {len(commodities)} original seed commodities from {seed_path}")

    # Synthesize realistic jittered dataset
    random.seed(42)
    np.random.seed(42)

    rows = []
    # Original records
    for item in commodities:
        rows.append({
            "commodity_id": item["id"],
            "moisture_pct": float(item["moisture_pct"]),
            "fat_oil_pct": float(item["fat_oil_pct"]),
            "ph_value": float(item["ph_value"]),
            "is_perishable": is_perishable_product(item["storage_type"], item["respiration_class"]),
            "shelf_life_days": float(item["shelf_life_days"]),
            "storage_temp_code": get_storage_temp_code(item["storage_type"]),
            "primary_material": item["primary_material"]
        })

    # Expand to ~90 samples using bounded physical jitter
    samples_per_commodity = 4
    for item in commodities:
        for _ in range(samples_per_commodity):
            moisture = max(0.1, min(98.0, item["moisture_pct"] + random.uniform(-0.8, 0.8)))
            fat = max(0.0, min(99.9, item["fat_oil_pct"] + random.uniform(-0.6, 0.6)))
            ph = max(2.5, min(8.5, item["ph_value"] + random.uniform(-0.15, 0.15)))
            shelf_life = max(3.0, item["shelf_life_days"] + random.uniform(-4, 4))

            rows.append({
                "commodity_id": item["id"],
                "moisture_pct": round(moisture, 2),
                "fat_oil_pct": round(fat, 2),
                "ph_value": round(ph, 2),
                "is_perishable": is_perishable_product(item["storage_type"], item["respiration_class"]),
                "shelf_life_days": round(shelf_life, 1),
                "storage_temp_code": get_storage_temp_code(item["storage_type"]),
                "primary_material": item["primary_material"]
            })

    df = pd.DataFrame(rows)
    print(f"[+] Synthesized dataset with {len(df)} total physical samples")

    feature_cols = [
        "moisture_pct",
        "fat_oil_pct",
        "ph_value",
        "is_perishable",
        "shelf_life_days",
        "storage_temp_code"
    ]

    X = df[feature_cols]
    y = df["primary_material"]

    # Stratified 5-Fold Cross Validation with Decision Tree
    clf = DecisionTreeClassifier(
        criterion="gini",
        max_depth=12,
        min_samples_split=2,
        random_state=42
    )

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(clf, X, y, cv=skf, scoring="accuracy")
    mean_acc = float(np.mean(scores))
    std_acc = float(np.std(scores))

    print(f"[+] 5-Fold Stratified Cross-Validation Accuracy: {mean_acc * 100:.2f}% (+/- {std_acc * 100:.2f}%)")

    # Fit final model
    clf.fit(X, y)

    # Classification report
    y_pred = clf.predict(X)
    report = classification_report(y, y_pred, zero_division=0)
    print("\n[+] Final Training Set Evaluation:")
    print(report)

    # Save artifact
    payload = {
        "model": clf,
        "feature_cols": feature_cols,
        "classes": list(clf.classes_),
        "cv_accuracy_mean": mean_acc,
        "cv_accuracy_std": std_acc,
        "num_samples": len(df)
    }

    joblib.dump(payload, model_path)
    print(f"[OK] Successfully exported trained model artifact to {model_path}")
    return payload

if __name__ == "__main__":
    train_and_export_model()
