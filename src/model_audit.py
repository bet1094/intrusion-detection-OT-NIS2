"""
Evaluación robusta del modelo Random Forest sobre CICIDS2017.

Aborda el problema documentado en el informe de auditoría:
el 100% de accuracy del notebook principal es consecuencia de
duplicación de flujos entre train y test con split aleatorio.

Este script aplica:
  - Deduplicación
  - Split estratificado
  - Validación cruzada k=5
  - Comparación contra DummyClassifier y LogisticRegression
  - Reporte por clase y matriz de confusión

Uso:
    python src/model_audit.py --data data/friday.csv.zip
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline

FEATURES = [
    "Flow Duration", "Total Fwd Packet", "Total Bwd packets",
    "Flow Bytes/s", "Flow Packets/s", "Packet Length Mean",
    "Protocol", "Dst Port", "Fwd Packet Length Mean",
    "Bwd Packet Length Mean",
]


def load_and_clean(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    print(f"[load] filas={len(df):,} columnas={df.shape[1]}")
    return df


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=FEATURES + ["Label"]).reset_index(drop=True)
    print(f"[dedup] {before:,} -> {len(df):,} ({before - len(df):,} duplicados eliminados)")
    return df


def evaluate(df: pd.DataFrame) -> None:
    X = df[FEATURES]
    le = LabelEncoder()
    y = le.fit_transform(df["Label"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "DummyClassifier (baseline)": DummyClassifier(strategy="most_frequent"),
        "LogisticRegression": Pipeline([
            ("sc", StandardScaler()),
            ("lr", LogisticRegression(max_iter=500, n_jobs=-1, class_weight="balanced")),
        ]),
        "RandomForest (default)": RandomForestClassifier(
            n_estimators=100, random_state=42, n_jobs=-1
        ),
        "RandomForest (balanced)": RandomForestClassifier(
            n_estimators=100, random_state=42, n_jobs=-1, class_weight="balanced"
        ),
    }

    for name, model in models.items():
        print("\n" + "=" * 70)
        print(f"Modelo: {name}")
        print("=" * 70)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        print(classification_report(y_test, y_pred, target_names=le.classes_, digits=4))
        print("Matriz de confusion:")
        print(confusion_matrix(y_test, y_pred))

        if "RandomForest" in name:
            skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            scores = cross_val_score(model, X, y, cv=skf, scoring="f1_macro", n_jobs=-1)
            print(f"\nCV macro-F1 (k=5): {scores.mean():.4f} +/- {scores.std():.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    args = parser.parse_args()

    df = load_and_clean(args.data)
    df = deduplicate(df)
    evaluate(df)


if __name__ == "__main__":
    main()
