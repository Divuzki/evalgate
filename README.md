# EvalGate
Run `python evalgate.py candidate` to replay a rejected extractor and `python evalgate.py fixed` to replay its repair. Run `python -m unittest` with Python 3.11+. No keys required.

## Decision record
Compare identical documents field by field. A scan-total regression in a slice with at least five examples blocks release. Smaller slices receive an insufficient-evidence result. The cost denominator counts only entirely correct documents. Recorded latency, cost and output fixtures are synthetic. CI gates the version in release.txt and links individual documents in its summary.

## Review the release
[Pull request and fix](https://github.com/Divuzki/evalgate/pull/1) · [Rejected candidate check](https://github.com/Divuzki/evalgate/actions/runs/45906944160)

## Reuse the action
After checking out your repository, invoke `Divuzki/evalgate@main` with the `corpus` directory and `candidate` basename. For repeatable releases pin a reviewed commit SHA. Supply documents/*.json, baseline.json and the candidate JSON using the committed fixture formats. The gate requires Python 3.11 or later.
