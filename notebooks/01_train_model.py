# Databricks notebook source
# MAGIC %md
# MAGIC # Databricks Enterprise ML Starter
# MAGIC Trains a small scikit-learn classifier and logs reproducible evidence to MLflow.

# COMMAND ----------

import json
import os
import sys
from pathlib import Path

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.datasets import load_iris

# Support both Databricks Repos/Workspace files and local execution.
repo_root = Path.cwd().parent
src_path = repo_root / "src"

if not src_path.exists():
    raise RuntimeError(
        f"Expected project source directory was not found: {src_path}. "
        f"Current working directory: {Path.cwd()}"
    )

sys.path.insert(0, str(src_path))

from databricks_ml_starter.model import train_model

# COMMAND ----------

random_state = int(os.getenv("RANDOM_STATE", "42"))
n_estimators = int(os.getenv("N_ESTIMATORS", "100"))

mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "/Shared/databricks-enterprise-ml-starter"))

with mlflow.start_run(run_name="iris-random-forest") as run:
    result = train_model(random_state=random_state, n_estimators=n_estimators)
    iris = load_iris(as_frame=True)
    signature = infer_signature(iris.data, result.model.predict(iris.data))

    mlflow.log_params(
        {
            "random_state": random_state,
            "n_estimators": n_estimators,
            "dataset": "sklearn.datasets.load_iris",
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
    }
    mlflow.log_dict(evidence, "evidence/training_summary.json")

print(json.dumps(evidence, indent=2))
