# Databricks notebook source
# MAGIC %md
# MAGIC # Databricks Enterprise ML Starter
# MAGIC
# MAGIC Small serverless-compatible ML workload using scikit-learn and MLflow.
# MAGIC The Databricks runtime notebook is intentionally self-contained so
# MAGIC Databricks Free Edition does not depend on custom wheel installation.

# COMMAND ----------

import json
import os
from dataclasses import dataclass

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
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


def train_model(
    random_state: int = 42,
    n_estimators: int = 100,
) -> TrainingResult:
    """Train a deterministic Iris classifier and return evaluation evidence."""

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


# COMMAND ----------

random_state = int(os.getenv("RANDOM_STATE", "42"))
n_estimators = int(os.getenv("N_ESTIMATORS", "100"))

mlflow.set_experiment(
    os.getenv(
        "MLFLOW_EXPERIMENT_NAME",
        "/Shared/databricks-enterprise-ml-starter",
    )
)

with mlflow.start_run(run_name="iris-random-forest") as run:
    result = train_model(
        random_state=random_state,
        n_estimators=n_estimators,
    )

    iris = load_iris(as_frame=True)

    signature = infer_signature(
        iris.data,
        result.model.predict(iris.data),
    )

    mlflow.log_params(
        {
            "random_state": random_state,
            "n_estimators": n_estimators,
            "dataset": "sklearn.datasets.load_iris",
            "compute": "databricks-serverless",
        }
    )

    mlflow.log_metrics(
        {
            "accuracy": result.accuracy,
            "f1_macro": result.f1_macro,
            "train_rows": result.train_rows,
            "test_rows": result.test_rows,
        }
    )

    mlflow.sklearn.log_model(
        sk_model=result.model,
        name="model",
        signature=signature,
        input_example=iris.data.head(3),
    )

    evidence = {
        "run_id": run.info.run_id,
        "accuracy": result.accuracy,
        "f1_macro": result.f1_macro,
        "model": "RandomForestClassifier",
        "dataset": "Iris",
        "compute": "Databricks Serverless",
    }

    mlflow.log_dict(
        evidence,
        "evidence/training_summary.json",
    )

print(json.dumps(evidence, indent=2))
