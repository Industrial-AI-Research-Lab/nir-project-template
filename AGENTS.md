# AGENTS.md

Instructions for LLM assistants working in this repository. People: read README.md first.
If `.agents/overlay/AGENTS.md` exists, follow it too; this file wins on conflict.

## Project

Semester research project (NIR). Python >= 3.12, uv, MLflow with a local SQLite store by default.
Package `src/nir_project/` (rename once with `make rename NAME=<package>`). Experiments run as
scripts: `uv run python -m nir_project --config configs/<name>.yaml`.

## Commands

- Install: `uv sync`. CI uses `uv sync --locked`; run `uv lock` after changing dependencies.
- Check: `make check` = ruff format --check, ruff check, mypy, pytest. Formatting: `make fmt`.
- One experiment: `make run`. MLflow UI: `make mlflow`.

## Checks

Before finishing a task, run `make check` and make it pass. Never commit with `--no-verify`.
The Stop hook in `.claude/settings.json` runs the same check while the working tree is dirty.

## Branches and pull requests

- Branch `<type>/<short-description>`; types feat, fix, refactor, docs, test, chore, exp.
  One branch per change; never rewrite pushed history on `main`.
- PR title `<type>: short description`. Template sections: Plan (the student writes it by hand),
  Done (you write it from the diff before Draft is removed), How to reproduce, `Closes #N`.
  Never edit Plan or the Closes line; never remove Draft, resolve threads or merge.
- Commit subject in the imperative, up to 50 characters; the body says what changed and why.

## Decisions

Architecture decisions go to `docs/adr/NNNN-short-title.md`, copied from `docs/adr/0000-template.md`.
You draft the record when asked, from the discussion, the PR thread and the code; the student reviews
it. Never edit an accepted record; a change is a new record that supersedes it.

## Experiments

- Every run goes to MLflow: `mlflow.set_experiment`, tags `stage`, `dataset`, `model_family`, `pr`;
  params and final metrics logged explicitly; the config file as an artifact.
- The seed comes from `SEED`; run from a committed checkout so the commit is recorded.
- A results row is commit, config path, seed, run id, metrics; keep it in `results/` or in the PR.
  Never put a number in a table or a PR without the run id behind it.

## Never commit

`.env` and any secret, raw data, model weights, files over a few tens of MB, generated logs,
`mlruns/`, personal agent files (`*.local.*`, `CLAUDE.local.md`, `.claude/settings.local.json`).

## Meetings and tasks

Meeting records: `docs/meetings/YYYY-MM-DD.md` from the template in that folder. Experiments are
issues opened from the Experiment form; the PR that closes one carries `Closes #N`.
