# Human Evaluation Benchmark for AI Support Assistants

A 40-case benchmark for comparing two language models on customer-support tasks. The fictional Northstar Outfitters policy gives reviewers a shared source of truth for checking return decisions, delivery issues, cancellation requests, privacy, and unsupported promises.

This repository includes the benchmark and review tools. The worked examples are illustrative. Run the evaluation to produce your own results.

## Files

| File | Contents |
| --- | --- |
| [data/policy.md](data/policy.md) | Fictional policy with six numbered clauses |
| [data/prompts.csv](data/prompts.csv) | 40 prompts with required checks and reference answers |
| [data/responses.template.csv](data/responses.template.csv) | Blank input for collecting one model's responses |
| [rubric.md](rubric.md) | Scoring anchors, pairwise decision rules, and failure tags |
| [examples/annotated-cases.md](examples/annotated-cases.md) | Three worked comparisons with corrected answers |
| [evaluate.py](evaluate.py) | Python CLI for blinded review and summary statistics |

## Run the evaluation

Use Python 3.9 or later. The CLI uses only the standard library. Model responses can be collected manually in chat or through an API you already have access to.

1. Pick two models. Record their exact names or versions, the date, and any settings you control. Use the same settings where possible and start a fresh conversation for each case. Send each model the same instructions, policy, and customer message. Keep the required checks and reference answers for grading.

   ```text
   You are a support assistant for Northstar Outfitters.
   Answer the customer using only the policy below.
   Follow the customer's format requests when compatible with the policy.

   [Paste data/policy.md here]

   Customer message:
   [Paste the prompt field here]
   ```

2. Make one copy of the response template per model. Paste the raw answers into the `response` column, preserving the `id` column. Save both as UTF-8 CSV files. A spreadsheet editor can preserve commas and line breaks inside cells when exporting.

   ```bash
   mkdir -p runs
   cp data/responses.template.csv runs/model_1.csv
   cp data/responses.template.csv runs/model_2.csv
   # Fill both CSV files, then run:
   python3 evaluate.py prepare runs/model_1.csv runs/model_2.csv runs/first
   ```

3. Fill the six scores, both primary failure tags, the pairwise winner, and the justification in `runs/first/review.csv`. Leave `key.csv` unopened until grading is finished. For stronger blinding, have someone else collect responses and give the reviewer only the review sheet. A solo reviewer who has already seen the raw outputs may recognize them even after shuffling.

4. Generate the summary after grading. Map `model_1` and `model_2` back to their recorded names.

   ```bash
   python3 evaluate.py report runs/first
   ```

## Publish your results

Add a `results/` folder with the scorecard and a short report. Include model names, collection settings, how you blinded responses, who graded them, model wins and ties, mean scores by dimension, and the counts of primary failure tags. Include three real failure cases with evidence from the answers, the applicable policy clauses, and your corrected responses. Include raw responses if you can share them.

The sample covers one fictional policy. Report the results for these cases and document limitations such as single-reviewer grading or recognizable model outputs.

## Upload this project to GitHub

Unzip the download, create an empty GitHub repository named `llm-evaluation-benchmark`, and upload the contents of this folder. Alternatively, run these commands from the unzipped project folder after replacing `YOUR-USERNAME`.

```bash
git init -b main
git add .
git commit -m "Add customer support LLM evaluation benchmark"
git remote add origin https://github.com/YOUR-USERNAME/llm-evaluation-benchmark.git
git push -u origin main
```
