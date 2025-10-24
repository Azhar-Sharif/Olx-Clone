## Branching model
- We use **GitFlow**:
  - `main` = production/stable
  - `develop` = integration branch
  - Features from `develop`: `feature/<name>`

## Commits
- Keep commits **atomic** and descriptive.
- Prefer Conventional Commit styles where helpful:
  - `feat: ...`, `fix: ...`, `chore: ...`, `docs: ...`, `build: ...`, `ci: ...`, `test: ...`, `style: ...`

## Pre-commit hooks
- Install once: `pre-commit install` and `pre-commit install --hook-type pre-push`
- Hooks:
  - On commit: `black`, `isort`, `flake8`
  - On pre-push: `pytest --cov` with **≥60%** coverage

## Tests
- Add/adjust tests for your changes.
- Run locally: `pytest`

## Pull Requests
- Open PRs **into `develop`**
- **At least 1 review required**

## Docker (dev)
- Run app: `docker compose up -d`
- Stop: `docker compose down`

## Secrets
- Never commit secrets.
- Use `.env` (untracked) and update `.env.example`.
