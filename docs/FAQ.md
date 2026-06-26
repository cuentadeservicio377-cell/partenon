# Partenon FAQ

Honest answers to questions entrepreneurs and developers ask about Partenon.

## For entrepreneurs

### 1. What is Partenon in one sentence?

Partenon is an open-source AI agent operating system for small businesses, organized as seven specialized heroes that work inside the tools you already use.

### 2. Does Partenon replace my accountant?

No. The Scribe organizes expenses, budgets, and dashboards, but it does not give tax or legal advice and does not file returns. Use it to prepare clean books you hand to your accountant.

### 3. Do I need a Hermes Agent subscription?

Partenon profiles are designed for the Hermes Agent CLI from Nous Research, which is distributed separately. You can run many local tools and demos without Hermes, but the full agent experience requires it.

### 4. What if I do not use Google Workspace?

Several heroes write local Excel files and JSON instead of Google Sheets. However, the intended shared workspace is Google Workspace. Microsoft 365 or other integrations are not implemented yet.

### 5. Does it handle payments for real?

The Collector can create real Stripe payment links, subscriptions, and invoices when `STRIPE_SECRET_KEY` is configured. In local mode it simulates operations so you can test safely.

### 6. Is my data private?

Credentials live in your `.env` file and are never committed. Data is stored locally in `data/` and optionally in your own Google Workspace and G-Brain database. You control the keys.

### 7. How much technical skill do I need?

To run the 15-minute demo, basic command-line comfort is enough. To connect live Google Workspace and Stripe, you need to create service accounts and API keys, which is intermediate.

### 8. Can I run it without coding?

Not yet. The current interface is the command line, the dashboard, and eventually the Hermes Agent chat. A fully no-code setup is on the roadmap.

### 9. Does it work on Windows?

The Python tools and dashboard are cross-platform. `install.sh` is bash; on Windows use `python scripts/setup_hermes.py` or WSL.

### 10. What does it cost to run?

The open-source software is free. You pay for your own API usage (OpenRouter, OpenAI, NVIDIA, etc.), Google Workspace, Stripe fees, and hosting if you deploy the dashboard.

### 11. Can the heroes make decisions without me?

No hero publishes, charges, sends, or signs without explicit approval unless you explicitly authorize it in the profile file (e.g., `.design` autonomy settings). Even then, the Collector never executes a charge without a recorded invoice or subscription.

### 12. How do I know which hero to ask?

Use natural language. The router in `partenon-core/tools/router.py` sends finance questions to the Scribe, marketing questions to the Herald, payment requests to the Collector, security questions to the Guardian, project questions to the Strategist, relationship questions to the Diplomat, and memory questions to the Brain. See [`HERO_GUIDE.md`](HERO_GUIDE.md) for examples.

### 13. What happens when a hero cannot answer?

The hero asks for missing context or hands off to another hero. For example, the Strategist routes customer communication through the Diplomat, and the Collector escalates unpaid accounts to the Diplomat after three reminders.

### 14. Can I add my own hero?

Yes. Create a new directory under `hermes/profiles/`, add `SOUL.md`, `config.yaml`, `.env.example`, and a `skills/` folder. Follow the pattern in the existing seven profiles.

### 15. Is there a roadmap?

Yes. Current priorities: functional eval loop, live end-to-end integrations, pilot validation, and a marketplace of specialized profiles. See [`README.md`](../README.md) for the full roadmap.

## For developers

### 16. Is the REST API production-ready?

No. `examples/api-server-stub.py` returns documented JSON shapes so front-end work can proceed. A production API is not implemented yet.

### 17. Is the Hermes CLI stub real?

No. It is a learning stub. The real Hermes CLI is distributed by Nous Research.

### 18. Why are there two G-Brain variable names?

`gbrain/server.py` and `gbrain/tools.py` read `GBrain_DATABASE_URL` by default, while `.env.example` uses `GBRAIN_DATABASE_URL`. Set both or the exact variable the component expects until this is standardized.

### 19. How do I run tests?

There is no full test suite yet. You can syntax-check Python files and run the demos:

```bash
python scripts/demo_tesorero.py
cd dashboard && npm run build
```

### 20. How do I contribute?

Fork the repository, create a branch, make your change, run the demo and dashboard build, and open a PR with evidence that both pass. See [`API.md`](API.md) for the module reference.

### 21. What license is Partenon under?

Check the `LICENSE` file at the repository root for the exact license.

### 22. Where do I report a security issue?

Do not open a public issue for security problems. Contact the maintainers privately and rotate any exposed keys immediately.
