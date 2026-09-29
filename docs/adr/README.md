# Decision log

One file per decision: `NNNN-short-title.md`, a four-digit consecutive number that is never reused.
Copy `0000-template.md`; the title names the problem and the chosen solution.

- The record is drafted by your LLM assistant at the moment of the decision, from the discussion,
  the PR thread and the code; you review it like code.
- It is born in the feature branch as `proposed`, is reviewed in the PR and becomes `accepted`
  in the same PR before merge. A rejected record is merged too, with the reason.
- An accepted record is never edited; a change is a new record that supersedes the old one,
  linked both ways.
- What deserves a record: repository structure and data flow; a library, framework or tool;
  an interface or data contract; the baseline, the primary metric, the dataset and its split;
  a direction closed by a negative result. A single hyperparameter run is an MLflow run, not a record.
- Link the MLflow experiment or run that motivated the decision.
