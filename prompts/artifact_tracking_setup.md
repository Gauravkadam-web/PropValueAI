# PropValueAI — Artifact Tracking & Fresh-Clone Setup Audit/Fix

You are working on the existing PropValueAI repository:
`D:\PropValueAI`

GitHub repository: `https://github.com/Gauravkadam-web/PropValueAI.git`

## Objective

Fix artifact tracking and make the fresh-clone setup instructions complete and accurate. This is a repository maintenance task only. **Do not start Phase 4 or implement new features.**

## 1. Inspect Before Changing Anything

Inspect the current:
- `.gitignore`
- `README.md`
- `ml/README.md`
- `ml/training/README.md`, if present
- `ml/inference/README.md`
- `ml/training/scripts/train.py`
- `ml/inference/config.py` and artifact-loading logic
- Existing artifact files and their actual Git tracking status

Confirm the actual artifact filenames, generation paths, environment requirements, and whether training creates both `model.joblib` and `metadata.json`.

Do not assume documentation is correct without verifying the code.

## 2. Fix Artifact Tracking

The intended behavior is:

- `ml/inference/artifacts/model.joblib`: allow it to be committed to Git. It is approximately 12.8 MB, so verify its actual size and confirm it is below GitHub's per-file limit.
- `ml/inference/artifacts/metadata.json`: allow it to be committed to Git.
- Preserve `ml/inference/artifacts/.gitkeep` if still needed.
- Continue ignoring Python virtual environments, caches, generated temporary files, and raw datasets as currently intended.

Update `.gitignore` with narrow, explicit rules. Ensure the artifact allowlist actually works despite parent-directory ignore rules.

Check the result using `git check-ignore` and `git status --short --ignored`. Do not force-add files blindly.

## 3. Validate Model Artifacts

Before staging any artifact:

- Confirm `model.joblib` and `metadata.json` exist at the expected paths.
- Confirm the metadata corresponds to the model and reflects the actual training/evaluation process.
- Verify that the inference service can load the existing model and metadata using the documented setup.
- Do not retrain or overwrite the model unless validation proves it is missing or invalid and regeneration is necessary.
- If regeneration is necessary, use the existing approved training pipeline and report the reason.
- Do not edit reported metrics just to make them look better.
- Never load or commit an artifact from an untrusted source.

## 4. Complete Fresh-Clone Documentation

Update the appropriate README files with two clearly separated setup paths.

### Option A — Run the existing model

Document how a developer can:
1. Clone the repository.
2. Set up the supported Python environment and install `ml/inference/requirements.txt`.
3. Confirm the committed artifacts exist.
4. Start the FastAPI inference service using the actual entry point and commands verified from the repository.
5. Verify `/health/live` and `/health/ready`.
6. Test a sample prediction using the actual API contract.

This path should not require the raw training dataset if committed artifacts are available.

### Option B — Regenerate the model

Document how a developer can:
1. Obtain `Pune_House_Data.csv` from the approved source or project owner.
2. Place it at the verified path `ml/training/data/raw/Pune_House_Data.csv`.
3. Set up the training environment and install the correct requirements.
4. Run the existing training script with the verified command.
5. Confirm that both artifacts are generated at the paths expected by the inference service.

Do not invent download URLs or claim the raw dataset is included in Git if it is ignored. Clearly state if manual dataset placement is required.

Mention that the dataset is derived from a Bengaluru benchmark with synthetically substituted locality labels. Preserve the required disclaimer:

“PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.”

## 5. Git Safety

- Do not commit or push automatically.
- Do not change branches, reset commits, rewrite history, or delete files.
- Do not stage unrelated modifications.
- Preserve existing user changes.
- First show the proposed changes and the exact files that would be staged.
- Check `git diff` and `git diff --cached` if anything is staged.
- Keep this task limited to artifact tracking and setup documentation.

## 6. Verification

Run the relevant checks available in the current environment:
- Verify Git ignore/tracking behavior for both artifacts.
- Verify artifact paths and metadata contents.
- Run the existing ML and inference tests if dependencies are available.
- Run the documented inference startup and health checks if practical.
- If any check cannot be run, state why instead of claiming it passed.

## 7. Final Report

Return a concise report containing:

1. Files changed.
2. Whether `model.joblib` and `metadata.json` are now eligible for Git tracking.
3. Whether fresh-clone inference works without downloading the dataset.
4. Exact steps required to regenerate artifacts from the dataset.
5. Tests and checks run, with actual results.
6. Any remaining issues.
7. The exact proposed Git staging commands.

**Stop after completing the changes and verification. Do not commit, push, or begin Phase 4. Wait for my approval.**
