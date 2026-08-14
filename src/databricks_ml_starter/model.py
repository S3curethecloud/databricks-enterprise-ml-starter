from __future__ import annotations

from dataclasses import dataclass

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


@dataclass(frozen=True)
class TrainingResult:
    model: RandomForestClassifier
    accuracy: float
    f1_macro: float
    train_rows: int
    test_rows: int


def train_model(random_state: int = 42, n_estimators: int = 100) -> TrainingResult:
    """Train a deterministic Iris classifier and return model + evaluation metrics."""
    iris = load_iris(as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.20,
        random_state=random_state,
        stratify=iris.target,
    )

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    return TrainingResult(
        model=model,
        accuracy=float(accuracy_score(y_test, predictions)),
        f1_macro=float(f1_score(y_test, predictions, average="macro")),
        train_rows=len(X_train),
        test_rows=len(X_test),
    )
