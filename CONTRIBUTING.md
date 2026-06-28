# Contributing to Partenon

Thank you for helping make Partenon better.

## Development setup

1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in real credentials for the services you use (OpenRouter, Google Workspace, Stripe, etc.).
3. Install Python dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Install dashboard dependencies:
   ```bash
   cd dashboard
   npm install
   ```
5. Run the test suite:
   ```bash
   python3 -m pytest tests/
   cd dashboard && npx tsc --noEmit
   ```

## No secrets or PII in commits

- Never commit `.env`, service-account JSON files, API keys, or real customer data.
- Use fictional `.example.com` / `.example.test` data in examples, tests, and docs.
- If you add sample names, emails, phones, or tax IDs, make them obviously fake.

## Before opening a pull request

1. Run tests and the type checker.
2. Run a secret scan (e.g., `git-secrets` or `truffleHog`) and confirm no credentials are leaked.
3. Update relevant docs (`docs/`, `README.md`, `CHANGELOG.md`) if the change is user-visible.
4. Keep changes focused and minimal.

## Adding a hero skill

1. Create the skill under `hermes/profiles/partenon-<hero>/skills/<skill>/`.
2. Add a `SKILL.md` describing inputs, outputs, and examples.
3. Provide unit tests or a runnable `__main__` demo.
4. Register the skill in the profile's `config.yaml` if required.
5. Update `docs/CAPABILITIES.md` and `docs/HERO_GUIDE.md` with the new capability.

## Questions

Open an issue or reach out to the maintainers. See `SECURITY.md` for sensitive reports.
