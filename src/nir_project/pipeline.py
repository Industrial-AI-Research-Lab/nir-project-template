"""One experiment end to end: data, model, metric, MLflow run.

Replace the synthetic data and the least-squares model with your own, but keep the shape:
one seed from the settings, one run per call, parameters and metrics logged explicitly.
"""

from __future__ import annotations

import random
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mlflow
import numpy as np
import yaml
from numpy.typing import NDArray

from nir_project.config import Settings

Array = NDArray[np.float64]


@dataclass(frozen=True)
class ExperimentConfig:
    """Everything that changes between runs and therefore must be logged."""

    name: str
    n_samples: int
    n_features: int
    noise: float
    stage: str = "baseline"
    dataset: str = "synthetic"
    model_family: str = "least-squares"

    @classmethod
    def from_yaml(cls, path: Path) -> ExperimentConfig:
        with path.open(encoding="utf-8") as fh:
            raw: dict[str, Any] = yaml.safe_load(fh)
        return cls(**raw)


@dataclass(frozen=True)
class RunResult:
    run_id: str
    mse: float


def set_seed(seed: int) -> np.random.Generator:
    """Seed every source of randomness the project uses; return the generator to pass around."""
    random.seed(seed)
    return np.random.default_rng(seed)


def make_data(rng: np.random.Generator, cfg: ExperimentConfig) -> tuple[Array, Array]:
    x = rng.normal(size=(cfg.n_samples, cfg.n_features))
    true_w = rng.normal(size=cfg.n_features)
    y = x @ true_w + cfg.noise * rng.normal(size=cfg.n_samples)
    return x, y


def fit_and_score(x: Array, y: Array) -> float:
    """Least squares on the first half of the data, mean squared error on the second half."""
    half = len(y) // 2
    w, *_ = np.linalg.lstsq(x[:half], y[:half], rcond=None)
    pred = x[half:] @ w
    return float(np.mean((pred - y[half:]) ** 2))


def current_commit() -> str:
    """Short commit of the checkout the run started from; 'unknown' outside a checkout."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return out.stdout.strip()


def run_experiment(
    cfg: ExperimentConfig, settings: Settings, config_path: Path | None = None
) -> RunResult:
    """Run one experiment and record it in MLflow."""
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)
    rng = set_seed(settings.seed)
    x, y = make_data(rng, cfg)

    with mlflow.start_run(run_name=cfg.name) as run:
        mlflow.set_tags(
            {
                "stage": cfg.stage,
                "dataset": cfg.dataset,
                "model_family": cfg.model_family,
                "commit": current_commit(),
            }
        )
        mlflow.log_params(
            {
                "seed": settings.seed,
                "n_samples": cfg.n_samples,
                "n_features": cfg.n_features,
                "noise": cfg.noise,
            }
        )
        if config_path is not None:
            mlflow.log_artifact(str(config_path))
        mse = fit_and_score(x, y)
        mlflow.log_metric("mse", mse)
        return RunResult(run_id=str(run.info.run_id), mse=mse)
