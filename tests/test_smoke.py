"""Smoke test: the whole pipeline on a tiny input, in seconds, with an isolated MLflow store."""

from pathlib import Path

import pytest

from nir_project.config import Settings
from nir_project.pipeline import ExperimentConfig, run_experiment

CONFIG = Path(__file__).resolve().parents[1] / "configs" / "smoke.yaml"


@pytest.fixture
def settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Settings:
    # No .env here, and the mlruns/ folder of the test lands here, not in the checkout.
    monkeypatch.chdir(tmp_path)
    return Settings(mlflow_tracking_uri=f"sqlite:///{tmp_path / 'mlflow.db'}", seed=7)


def test_pipeline_runs_and_logs(settings: Settings) -> None:
    cfg = ExperimentConfig.from_yaml(CONFIG)
    result = run_experiment(cfg, settings, config_path=CONFIG)
    assert result.run_id
    assert result.mse >= 0.0


def test_same_seed_same_metric(settings: Settings) -> None:
    cfg = ExperimentConfig.from_yaml(CONFIG)
    first = run_experiment(cfg, settings)
    second = run_experiment(cfg, settings)
    assert first.mse == second.mse
