# Databricks Enterprise ML Starter

A small, working Databricks AI/ML project that demonstrates a clean enterprise delivery pattern without unnecessary platform complexity. It trains an Iris classifier with scikit-learn, tracks the run with MLflow, packages the model as an MLflow model artifact, emits a compact evidence record, and can be deployed as a Databricks job with a Declarative Automation Bundle.

## What this proves

- **Reproducible training:** deterministic train/test split and model seed.
- **MLflow observability:** parameters, quality metrics, model artifact, signature, input example, and training evidence are logged to MLflow.
- **Quality gate:** automated test requires accuracy of at least 0.90 and macro-F1 of at least 0.89.
- **Separation of concerns:** reusable model logic lives under `src/`; the Databricks notebook is orchestration only.
- **Deployment-as-code:** `databricks.yml` and `resources/job.yml` define a deployable Databricks job.
- **Safe starter scope:** no production data, external API keys, secrets, or privileged integrations are required.

## Architecture

```text
GitHub Repository
      |
      +-- src/databricks_ml_starter/model.py
      |       |  deterministic ML logic
      |       v
      +-- notebooks/01_train_model.py
      |       |  orchestration + MLflow logging
      |       v
      |    Databricks MLflow Experiment
      |       +-- params
      |       +-- metrics
      |       +-- model + signature
      |       +-- evidence/training_summary.json
      |
      +-- tests/test_model.py
      |       +-- local quality gate
      |
      +-- databricks.yml + resources/job.yml
              +-- Databricks job deployment
```

## Repository layout

```text
databricks-enterprise-ml-starter/
├── databricks.yml
├── resources/
│   └── job.yml
├── notebooks/
│   └── 01_train_model.py
├── src/
│   └── databricks_ml_starter/
│       ├── __init__.py
│       └── model.py
├── tests/
│   └── test_model.py
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── README.md
```

## Quick start: local validation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest -q
```

The test trains the model locally and validates the minimum model-quality gate.

## Quick start: Databricks workspace

### Option A — Run the notebook directly

1. Add this repository to Databricks Git folders / workspace files.
2. Use a Databricks Runtime that supports Python, scikit-learn, and MLflow.
3. Open `notebooks/01_train_model.py` as a Databricks source notebook.
4. Attach compute and run all cells.
5. Open the MLflow experiment at `/Shared/databricks-enterprise-ml-starter`.

Expected logged evidence includes `accuracy`, `f1_macro`, row counts, model parameters, a model artifact, signature/input example, and `evidence/training_summary.json`.

### Option B — Deploy as a Databricks bundle

Install and authenticate the Databricks CLI, then provide an existing cluster ID:

```bash
export BUNDLE_VAR_cluster_id="<your-cluster-id>"
databricks bundle validate
databricks bundle deploy -t dev
databricks bundle run ml_training_job -t dev
```

Using an existing cluster keeps this starter cloud-neutral and avoids hard-coding AWS, Azure, or GCP node types into the repository.

## MLflow evidence contract

Each successful run records:

| Evidence | Purpose |
|---|---|
| Parameters | Reproduce the training configuration |
| Accuracy + macro-F1 | Model quality evidence |
| Train/test row counts | Basic data-split traceability |
| MLflow model artifact | Portable model packaging |
| Model signature | Input/output contract |
| Input example | Operational validation aid |
| `training_summary.json` | Compact machine-readable audit evidence |

## Enterprise controls intentionally represented

This is a starter, but the repository structure maps cleanly to larger platform controls:

- **Source control:** all ML logic and deployment configuration are versioned.
- **Reproducibility:** deterministic seed and explicit dependencies.
- **Model traceability:** MLflow run ID links configuration, metrics, and model artifacts.
- **Quality enforcement:** automated threshold test before promotion.
- **Least privilege:** no credentials are committed; Databricks authentication stays outside source control.
- **Portability:** job configuration references an existing cluster instead of embedding provider-specific infrastructure.

## Production hardening path

For a real enterprise workload, extend this starter with Unity Catalog model registration, governed tables/Volumes, service principals, cluster policies or serverless controls, CI/CD bundle deployment, environment-specific targets, feature/data validation, model approval gates, lineage, drift monitoring, secrets management, and centralized audit telemetry.

## GitHub commit

```bash
git init
git add .
git commit -m "feat: add Databricks enterprise ML starter"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Reference documentation

- Databricks Declarative Automation Bundles: https://docs.databricks.com/aws/en/dev-tools/bundles/
- Databricks MLflow models: https://docs.databricks.com/aws/en/mlflow/models
- MLflow scikit-learn integration: https://mlflow.org/docs/latest/ml/traditional-ml/sklearn/guide/

## License

Use this starter under your organization’s preferred repository license and security policy.
