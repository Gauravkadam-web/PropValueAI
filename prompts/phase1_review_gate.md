# PropValueAI — Phase 1 Final Review and Dataset Approval Gate

Phase 1 implementation is complete, but it has NOT yet been approved for transition to Phase 2.

Read `AGENTS.md`, `docs/dataset-evaluation.md`, `docs/dataset-validation-report.md`, and the current Git diff before proceeding.

## Tasks

### 1. Verify Dataset Provenance

Investigate the claim that `ml/training/data/raw/Pune_House_Data.csv` is derived from the standard Bengaluru House Price dataset.

- Identify the original dataset and its source.
- Compare column names, representative records, value patterns, and available provenance information.
- Determine whether Pune locality names are authentic observations or mapped labels.
- Separate verified evidence from inference.
- Do not describe this dataset as genuine Pune market data unless the evidence supports that claim.

### 2. Verify Licensing

- Inspect the candidate repository's actual license and dataset attribution.
- Investigate the original dataset's license or usage restrictions where possible.
- Do not infer MIT or public-domain status from public accessibility alone.
- Record any unresolved licensing uncertainty.
- If licensing cannot be verified, state that clearly.

### 3. Recommend the Appropriate Dataset Use

Assess these options:

A. Use the current dataset for an educational regression demonstration, with explicit limitations.

B. Find a more credible dataset with verifiable Pune market relevance and appropriate usage rights.

C. Retain the current dataset for experimentation while keeping genuine Pune market prediction as an unvalidated future objective.

Recommend an option based on evidence. Explain what claims the eventual model can and cannot support.

Do not download additional large datasets or merge sources automatically.

### 4. Review Phase 1 Files and Git State

- Inspect all Phase 1 changes and the untracked `prompts/` directory.
- Verify the raw dataset and `.venv` remain excluded from Git.
- Review the modified `ml/training/requirements.txt`.
- Confirm the inspection script and documentation are consistent.
- Do not delete files, stage changes, commit, or push.
- Do not change unrelated Phase 0 files.

### 5. Update Documentation if Necessary

If evidence changes the current conclusions, update:
- `docs/dataset-evaluation.md`
- `docs/dataset-validation-report.md`

Document source attribution, provenance confidence, licensing status, dataset limitations, and the recommended decision. Preserve the original findings where appropriate and clearly identify corrections.

## Strict Restrictions

Do NOT train a model, perform Phase 2 preprocessing, create model artifacts, build APIs, or change the project architecture.

Do NOT claim that any dataset is approved until its suitability and usage rights have been assessed adequately.

## Final Report

Report:
1. Provenance verification results.
2. License verification results.
3. Recommended dataset strategy and rationale.
4. Documentation changes made.
5. Remaining uncertainties.
6. Final Git status and diff summary.
7. Whether Phase 1 is ready for explicit approval.

Stop and wait for my approval before starting Phase 2.
