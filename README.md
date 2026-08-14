# Databricks Enterprise ML Starter

A small, working Databricks AI/ML project demonstrating a clean enterprise delivery pattern using **Databricks Serverless**, **scikit-learn**, **MLflow**, automated testing, **GitHub Actions**, and **Databricks Declarative Automation Bundles**.

The project trains a deterministic Iris classification model, records model-quality evidence with MLflow, and deploys and runs successfully on Databricks serverless compute.

## Validated Result

This project has been validated end to end against a live Databricks serverless workspace.

* Local quality gate: `1 passed`
* Bundle validation: `Validation OK!`
* Bundle deployment: `Deployment complete!`
* Databricks job ID: `316912147751440`
* Successful run ID: `942587554288392`
* Successful run ID: `321764149621617`
* Final execution state: `TERMINATED SUCCESS`
* Consecutive successful serverless runs: `2`

Historical failed runs are intentionally retained in Databricks as engineering evidence from earlier dependency and workspace-file experiments.

## What This Project Demonstrates

* Deterministic ML model training with scikit-learn
* Local automated model-quality testing with pytest
* GitHub-based source control
* GitHub Actions CI
* Databricks Declarative Automation Bundle deployment
* Databricks Serverless job execution
* MLflow experiment tracking
* MLflow model artifact logging
* Model signatures and input examples
* Machine-readable training evidence
* Repeatable deployment without a classic cluster
* Separation between local engineering validation and Databricks runtime execution

## Architecture

```text
GitHub Repository
        |
        +-------------------------------+
        |                               |
        v                               v
src/databricks_ml_starter/           tests/
        |                               |
        |                         pytest quality gate
        |                               |
        +---------------+---------------+
                        |
                        v
                  GitHub Actions
                        |
                        v
            Databricks Declarative
               Automation Bundle
                        |
                        v
               Serverless Job
                        |
                        v
          notebooks/01_train_model.py
                        |
             +----------+----------+
             |          |          |
             v          v          v
        scikit-learn   MLflow    Evidence
          training     metrics     JSON
             |          |
             +----------+
                  |
                  v
             MLflow Model
```

## Repository Layout

```text
databricks-enterprise-ml-starter/
├── .github/
│   └── workflows/
│       └── ci.yml
├── notebooks/
│   └── 01_train_model.py
├── resources/
│   └── job.yml
├── src/
│   └── databricks_ml_starter/
│       ├── __init__.py
│       └── model.py
├── tests/
│   └── test_model.py
├── databricks.yml
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── README.md
```

## Runtime Design

The repository intentionally separates the **local engineering path** from the **Databricks Free Edition runtime path**.

### Local Engineering Path

Reusable model logic is maintained under:

```text
src/databricks_ml_starter/
```

That code is exercised by:

```text
tests/test_model.py
```

and validated using pytest and GitHub Actions.

This path provides a conventional Python package structure for local development, automated testing, and future production packaging.

### Databricks Runtime Path

The Databricks training notebook is intentionally self-contained.

This design was selected after validating several approaches against Databricks Free Edition serverless compute.

The final runtime avoids:

* direct Python imports from bundle-managed `/Workspace` source paths
* custom wheel installation from bundle-internal artifact paths
* classic cluster dependencies
* manually supplied cluster IDs

The self-contained notebook approach produced consecutive successful serverless executions and is therefore the validated runtime architecture for this starter.

For a larger enterprise implementation, reusable Python application code should normally be distributed through a governed package or artifact repository rather than duplicated into runtime notebooks.

## Local Validation

Create a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Upgrade pip:

```bash
pip install --upgrade pip
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

Run the quality gate:

```bash
pytest -q
```

Expected result:

```text
1 passed
```

The test validates the following minimum model-quality thresholds:

* Accuracy >= `0.90`
* Macro-F1 >= `0.89`

## Databricks CLI Installation

Install the Databricks CLI on Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sudo sh
```

Verify installation:

```bash
databricks version
```

Example validated version:

```text
Databricks CLI v1.12.1
```

## Databricks Authentication

Authenticate using Databricks OAuth:

```bash
databricks auth login \
  --host https://<workspace-host> \
  --profile databricks-free
```

Replace `<workspace-host>` with the root Databricks workspace URL.

Example format:

```text
https://dbc-xxxxxxxx-xxxx.cloud.databricks.com
```

Do not include paths such as:

```text
/compute
/workspace
/sql
```

and do not include query parameters.

Verify the authentication profile:

```bash
databricks auth profiles
```

Verify the authenticated identity:

```bash
databricks current-user me \
  --profile databricks-free
```

Inspect authentication configuration:

```bash
databricks auth describe \
  --profile databricks-free
```

Authentication credentials and OAuth tokens must never be committed to source control.

## Validate the Databricks Bundle

From the repository root:

```bash
databricks bundle validate \
  -t dev \
  --profile databricks-free
```

Expected result:

```text
Validation OK!
```

## Deploy

Deploy the bundle:

```bash
databricks bundle deploy \
  -t dev \
  --profile databricks-free
```

Expected terminal result:

```text
Deployment complete!
```

The bundle deploys the notebook and Databricks job definition into the authenticated workspace.

## Run the ML Job

Execute the deployed training job:

```bash
databricks bundle run ml_training_job \
  -t dev \
  --profile databricks-free
```

Expected final state:

```text
TERMINATED SUCCESS
```

## Inspect Job History

List recent Databricks job runs:

```bash
databricks jobs list-runs \
  --profile databricks-free
```

Inspect only this project's deployed job:

```bash
databricks jobs list-runs \
  --job-id 316912147751440 \
  --profile databricks-free
```

The validated environment produced two consecutive successful runs:

```text
321764149621617  SUCCESS
942587554288392  SUCCESS
```

Earlier failed runs are retained because they document the engineering iterations used to reach the final architecture.

## Model

The starter uses the following ML workload:

```text
Dataset: Iris
Algorithm: RandomForestClassifier
Train/test split: 80/20
Random state: 42
Estimators: 100
```

The workload is deliberately small.

The objective is to demonstrate Databricks ML engineering patterns rather than model complexity or dataset scale.

No production datasets, GPUs, external APIs, API keys, or application secrets are required.

## MLflow Evidence Contract

Each successful training run records evidence through MLflow.

| Evidence                | Purpose                                 |
| ----------------------- | --------------------------------------- |
| `random_state`          | Reproduce model and data split behavior |
| `n_estimators`          | Reproduce model configuration           |
| Dataset identifier      | Training-source traceability            |
| Compute identifier      | Runtime-context traceability            |
| Accuracy                | Model-quality evidence                  |
| Macro-F1                | Balanced model-quality evidence         |
| Train row count         | Training-volume evidence                |
| Test row count          | Evaluation-volume evidence              |
| MLflow model artifact   | Portable model representation           |
| Model signature         | Input/output contract                   |
| Input example           | Operational validation aid              |
| `training_summary.json` | Machine-readable execution evidence     |
| MLflow run ID           | Links the model to execution evidence   |

The MLflow experiment is configured as:

```text
/Shared/databricks-enterprise-ml-starter
```

## Enterprise Controls Represented

Although intentionally small, the repository demonstrates patterns that map cleanly to larger enterprise ML platforms.

### Source Control

ML code, tests, CI configuration, notebook logic, and Databricks deployment configuration are version controlled.

### Reproducibility

The training split and Random Forest model use deterministic seeds.

### Automated Quality Gates

Model-quality thresholds are tested with pytest before changes are promoted.

### Deployment as Code

Databricks job resources are defined declaratively using:

```text
databricks.yml
resources/job.yml
```

### Authenticated Platform Access

Databricks CLI access is authenticated using an explicit named profile.

### Serverless Compute

The workload executes without requiring users to create or maintain a classic Databricks cluster.

### Model Traceability

MLflow connects model artifacts, metrics, parameters, signatures, and execution evidence to a specific run ID.

### Evidence Generation

Each successful training execution emits machine-readable evidence through MLflow.

### Secret Hygiene

No credentials, OAuth tokens, passwords, cloud keys, or API secrets are committed to the repository.

## Engineering Lessons from Validation

Several implementation approaches were tested during end-to-end validation.

### 1. Direct Workspace Module Import

The initial design attempted to import reusable Python code directly from the bundle-managed workspace path:

```text
/Workspace/.../.bundle/.../files/src/
```

Under Databricks Free Edition serverless compute, this produced workspace-file access errors.

### 2. Python Wheel Packaging

The Python package was successfully built as:

```text
databricks_enterprise_ml_starter-0.1.0-py3-none-any.whl
```

and uploaded through the Databricks bundle.

This demonstrated that the project was packageable.

### 3. Serverless Environment Wheel Installation

The wheel was then attached through a Databricks serverless job environment.

Although one execution succeeded, a later execution returned an artifact permission error while attempting to install the wheel from the bundle's internal workspace artifact location.

This made the runtime insufficiently repeatable for the Free Edition starter.

### 4. Self-Contained Serverless Notebook

The final design removed custom runtime artifact installation and executes the ML workload directly within the Databricks notebook.

This configuration produced consecutive successful executions and is therefore the validated runtime path for this project.

## Why Keep `src/`?

Even though the validated Databricks Free Edition runtime uses a self-contained notebook, the repository intentionally retains:

```text
src/databricks_ml_starter/
```

This provides:

* clean local Python engineering structure
* reusable model logic
* local unit and quality testing
* an upgrade path toward packaged production workloads
* separation between development validation and Free Edition runtime constraints

A production implementation would normally avoid duplicating logic between source modules and runtime notebooks by introducing a governed package distribution mechanism.

## GitHub Actions

The repository includes:

```text
.github/workflows/ci.yml
```

The workflow runs the automated pytest quality gate on repository changes.

This ensures model-quality validation is performed independently of the Databricks runtime.

## Security Notes

* Never commit Databricks OAuth tokens.
* Never commit `~/.databrickscfg`.
* Never commit `~/.databricks/token-cache.json`.
* Never store production secrets in notebooks.
* Keep production datasets out of this starter repository.
* Use service principals or workload identities for production automation.
* Apply least privilege to production jobs and data.
* Use governed artifact repositories for production dependencies.
* Use centralized audit logging in production environments.

## Production Hardening Path

A production enterprise implementation should extend this starter with:

* Unity Catalog
* governed tables
* governed Volumes
* service principals
* workload identity
* production artifact repositories
* environment-specific bundle targets
* CI/CD deployment identities
* model registration
* model approval gates
* data-quality validation
* feature validation
* lineage
* model monitoring
* drift detection
* centralized audit telemetry
* secrets management
* policy enforcement
* least-privilege workspace permissions
* production observability
* rollback controls
* promotion controls
* environment isolation

Production Python code should be delivered through a governed package or artifact mechanism rather than duplicated into notebooks.

## Useful Commands

Run local tests:

```bash
pytest -q
```

Validate the Databricks bundle:

```bash
databricks bundle validate \
  -t dev \
  --profile databricks-free
```

Deploy:

```bash
databricks bundle deploy \
  -t dev \
  --profile databricks-free
```

Run the ML job:

```bash
databricks bundle run ml_training_job \
  -t dev \
  --profile databricks-free
```

Inspect run history:

```bash
databricks jobs list-runs \
  --profile databricks-free
```

Check Git status:

```bash
git status
```

## Scope

This repository is an educational and architectural starter.

It demonstrates a real, functioning Databricks ML delivery path while deliberately avoiding the complexity of a full production MLOps platform.

The primary goal is to demonstrate:

```text
GitHub
   ↓
Automated Tests
   ↓
Databricks Bundle
   ↓
Serverless Compute
   ↓
scikit-learn Training
   ↓
MLflow Model + Metrics + Evidence
```

## Reference Documentation

* Databricks Declarative Automation Bundles
* Databricks Serverless Compute
* Databricks Jobs
* Databricks MLflow
* MLflow scikit-learn integration

## License

Use this starter under your organization's preferred repository license and security policy.
