"""Configuration read from the environment and `.env`.

Every value that differs between machines lives here and in `.env.example`.
A wrong value fails at start, not in the middle of a run.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Values from `.env` or the environment, validated once at start."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    mlflow_tracking_uri: str = "sqlite:///mlflow.db"
    mlflow_experiment_name: str = "nir-project"
    seed: int = 42
    data_dir: Path = Path("data")
    results_dir: Path = Path("results")


def load_settings() -> Settings:
    """Read the settings once; pass the object around instead of reading os.environ."""
    return Settings()
