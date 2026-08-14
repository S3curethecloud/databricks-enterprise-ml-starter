from databricks_ml_starter.model import train_model


def test_train_model_meets_quality_gate():
    result = train_model(random_state=42, n_estimators=50)
    assert result.train_rows == 120
    assert result.test_rows == 30
    assert result.accuracy >= 0.90
    assert result.f1_macro >= 0.89
