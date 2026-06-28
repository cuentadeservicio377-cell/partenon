# Contributing to Partenon

Thank you for considering a contribution. This document covers the basics of getting started and submitting changes.

## Development environment

1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in your own credentials. Never commit `.env`.
3. Install Python dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. For the Next.js dashboard:
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```
5. Run the test suite:
   ```bash
   python3 -m pytest tests/
   ```

## No secrets or PII in commits

- Do not commit API keys, passwords, tokens, or service-account JSON files.
- Do not commit real names, emails, phone numbers, tax IDs, or addresses.
- Use obviously fictional data such as `*.example.com`, `*.example.test`, or `*.local`.
- If you add sample data, follow the patterns already used in `data/` and `workshop/simulations/`.

## Before submitting a pull request

1. Run the tests:
   ```bash
   python3 -m pytest tests/
   ```
2. Type-check the dashboard:
   ```bash
   cd dashboard && npx tsc --noEmit
   ```
3. Scan your diff for secrets or PII:
   ```bash
   git diff --name-only
   git diff | grep -Ei "(password|secret|token|key|api_key|@[a-z0-9.-]+\.(com|net|org))"
   ```
4. Update relevant documentation if your change affects user-facing behavior.

## How to add a hero skill

1. Choose the hero profile under `hermes/profiles/partenon-<hero>/skills/<skill>/`.
2. Add the tool file under `tools/` with a clear docstring and a `main()` entry point for manual testing.
3. Update the skill `SKILL.md` with the new tool, inputs, outputs, and an example prompt.
4. If the skill needs new environment variables, add commented placeholders to `.env.example`.
5. Add or update tests under `tests/` if the skill touches core data formats.

## Questions

Open an issue or reach out to the maintainers. For security matters, see `SECURITY.md`.
