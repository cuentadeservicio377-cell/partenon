# Partenon Hero Guide

This guide is a technical reference for each of the seven Partenon hero profiles. It is written for operators and developers who want to know exactly which files, functions, and environment variables each hero uses.

For a quick overview, see [`docs/assets/hero-matrix.md`](assets/hero-matrix.md). For a founder-focused rollout plan, see [`docs/ENTREPRENEUR_PLAYBOOK.md`](ENTREPRENEUR_PLAYBOOK.md).

---

## How to read this guide

- **Profile directory**: where the Hermes Agent distribution lives.
- **Config file**: the per-company file the hero reads and writes.
- **Tools**: real Python functions in the repository.
- **MCP servers**: external context servers declared in `partenon-core/config/mcp/servers.yaml` or the profile `config.yaml`.
- **Cron jobs**: scheduled tasks under `hermes/profiles/<profile>/cron/`.
- **Commands/prompts**: copy-paste examples. You can run the Python tools directly or ask Hermes to run them.

---

## 1. Scribe (Treasurer) — `partenon-tesorero`

**Role**: finance, budgets, vendors, dashboards.

**Profile directory**: [`hermes/profiles/partenon-tesorero`](../hermes/profiles/partenon-tesorero)  
**Config file**: `.finance` (see [`templates/.finance.example`](../hermes/profiles/partenon-tesorero/templates/.finance.example))  
**Skill docs**: [`skills/finance/SKILL.md`](../hermes/profiles/partenon-tesorero/skills/finance/SKILL.md)

### Real tools

| Tool file | Function | What it does |
|-----------|----------|--------------|
| `tools/google_sheets.py` | `GoogleSheets.create_dashboard(title)` | Creates or opens a master finance spreadsheet with sheets for Income, Fixed Costs, Variable Costs, Vendors, Budget vs Actual, Alerts. |
| `tools/google_sheets.py` | `GoogleSheets.append_rows(spreadsheet_id, range, rows)` | Appends transactions to a sheet. |
| `tools/parsers.py` | `ExpenseParser.parse_excel(filepath)` | Reads Excel/CSV expenses, infers category and fixed/variable type. |
| `tools/parsers.py` | `infer_category(description)` | Returns one of: rent, payroll, technology, marketing, materials, logistics, services, taxes, maintenance, other. |
| `tools/templates.py` | `Templates.create_budget(filepath, period, line_items)` | Generates a budget-vs-actual Excel file. |
| `tools/templates.py` | `Templates.create_vendors(filepath)` | Generates a vendor directory. |
| `tools/templates.py` | `Templates.create_cash_flow(filepath, months)` | Generates a cash-flow projection. |
| `tools/audit.py` | `Audit.run_daily_report(output_path)` | Produces cash flow + anomaly report. |
| `tools/audit.py` | `Audit.run_weekly_review(output_path)` | Compares budgets against actuals by area. |

### MCP servers and env vars

- **MCP**: `google_workspace`, `gbrain`.
- **Required env**: `OPENROUTER_API_KEY`, `GOOGLE_SERVICE_ACCOUNT_JSON`.
- **Optional env**: `PARTENON_TESORERO_CURRENCY` (default `MXN`), `PARTENON_TESORERO_SHEET_ID`.

### Cron jobs

- `cron/daily-report.json` — runs `audit.run_daily_report` at 07:00.
- `cron/weekly-content.json` — runs `audit.run_weekly_review` on Mondays at 08:00.

### Example prompts

1. `Scribe, create a finance dashboard called "Example Finances" and seed the headers.`
2. `Parse last month's expenses from data/june_expenses.xlsx and classify them.`
3. `Record a $450 fixed cost for office rent paid to Example Coworking on 2026-06-01.`
4. `Run the weekly budget review and export it to output/weekly_review.json.`
5. `Which variable expenses are over budget this month?`

### Integration points

- Reads campaign budgets for the Herald from `.finance[budgets]`.
- Records confirmed payments sent by the Collector.
- Sends anomaly alerts to the Guardian if suspicious amounts appear.

---

## 2. Herald (Messenger) — `partenon-mensajero`

**Role**: brand voice, content, campaigns, copy, SEO/GEO, presentations.

**Profile directory**: [`hermes/profiles/partenon-mensajero`](../hermes/profiles/partenon-mensajero)  
**Config file**: `.design` (see [`templates/.design.example`](../hermes/profiles/partenon-mensajero/templates/.design.example))  
**Skill docs**: [`skills/comms/SKILL.md`](../hermes/profiles/partenon-mensajero/skills/comms/SKILL.md)

### Real tools

| Tool file | Function | What it does |
|-----------|----------|--------------|
| `tools/brand_intake.py` | `interactive_intake(path)` or `generate_design_from_dict(answers)` | Creates or updates `.design`. |
| `tools/content_calendar.py` | `generate_calendar(topic, channels, days, brand_context)` | Builds a pillar-based content calendar and saves it to `output/campaigns/<id>/content-calendar.json`. |
| `tools/copy_generator.py` | `generate_copy(piece_type, topic, channel)` | Generates ad, email, post, or landing copy and checks for banned patterns. |
| `tools/seo_geo_optimizer.py` | `analyze(topic, content)` | Returns keywords, SEO recommendations, and GEO recommendations. |
| `tools/presentation_builder.py` | `build_presentation(topic)` | Returns a 6-slide proposal structure. |
| `tools/publish_post.py` | `publish(channel, copy, media)` | Validates a post and records it as published or pending approval. |
| `tools/schedule_content.py` | `schedule_posts(calendar_path)` | Builds a posting schedule from a content calendar. |

### MCP servers and env vars

- **MCP**: `google_workspace`, `gmail`, `social_media`, `open_design`, `gbrain`.
- **Required env**: `OPENROUTER_API_KEY`.
- **Optional env**: `GMAIL_ACCESS_TOKEN`, social tokens (`LINKEDIN_ACCESS_TOKEN`, `TWITTER_BEARER_TOKEN`, etc.), WordPress/SSH vars.

### Cron jobs

- `cron/morning-briefing.json` — 07:30 daily: reads `.design`, calendar, generates post ideas.
- `cron/midday-pulse.json` — 13:00 daily: reads social metrics and recommends adjustments.
- `cron/weekly-content.json` — Mon 09:00: generates weekly calendar and base copy.

### Example prompts

1. `Herald, run the brand interview and fill .design for my agency.`
2. `Generate a 14-day content calendar about "payment automation for SMEs" for LinkedIn and Instagram.`
3. `Write three ad variants for "free cash-flow diagnostic" on LinkedIn.`
4. `Run an SEO/GEO analysis for "construction cost control software" and save the report.`
5. `Build a 6-slide pitch deck for "Operations OS for coffee shops".`

### Integration points

- Reads budget limits from the Scribe before proposing campaigns.
- Sends campaign dates to the Strategist for calendar blocking.
- Asks the Diplomat for client-facing language before sending formal proposals.

---

## 3. Collector — `partenon-cobrador`

**Role**: payments, subscriptions, invoices, reminders, revenue tracking, fraud monitoring.

**Profile directory**: [`hermes/profiles/partenon-cobrador`](../hermes/profiles/partenon-cobrador)  
**Config file**: `.payments` (see [`templates/.payments.example`](../hermes/profiles/partenon-cobrador/templates/.payments.example))  
**Skill docs**: [`skills/payments/SKILL.md`](../hermes/profiles/partenon-cobrador/skills/payments/SKILL.md)

### Real tools

| Tool file | Function | What it does |
|-----------|----------|--------------|
| `tools/stripe_tools.py` | `create_payment_link(product, price)` | Creates a Stripe payment link or a local-mode placeholder. |
| `tools/stripe_tools.py` | `create_subscription(customer, price)` | Creates a subscription in Stripe or local JSON. |
| `tools/stripe_tools.py` | `create_invoice(customer, items)` | Creates a finalized Stripe invoice or local record. |
| `tools/stripe_tools.py` | `send_payment_reminder(customer)` | Records a reminder in `.payments` (delegates to Gmail MCP in production). |
| `tools/stripe_tools.py` | `record_payment(intent)` | Records a confirmed payment and marks it for Treasurer sync. |
| `tools/stripe_tools.py` | `generate_income_report(start_date, end_date)` | Returns total collected, pending, overdue, by customer and product. |
| `tools/stripe_tools.py` | `read_overdue_payments()` / `classify_risk()` | Buckets overdue accounts into low/medium/high risk. |
| `tools/stripe_tools.py` | `monitor_fraud(charge)` | Flags unusually large amounts, failed/disputed charges, missing emails. |

### MCP servers and env vars

- **MCP**: `stripe`, `google_workspace`, `gbrain`.
- **Required env**: `STRIPE_SECRET_KEY`, `OPENROUTER_API_KEY`.
- **Optional env**: `STRIPE_WEBHOOK_SECRET`, `GOOGLE_SERVICE_ACCOUNT_JSON`.

### Cron jobs

- `cron/daily-collection.json` — 09:00 daily: pending payments, upcoming due dates, failed subscriptions, reminders.
- `cron/daily-followups.json` — 17:00 daily: overdue accounts, risk classification, follow-up scheduling, fraud review.

### Example prompts

1. `Collector, create a payment link for "Initial consultation" priced at $1,500 MXN.`
2. `Create a monthly subscription for user1@example.test at $500 MXN/month.`
3. `Invoice client@example.test for two line items: strategy $25,000, implementation $40,000.`
4. `Generate the income report for 2026-06-01 to 2026-06-30.`
5. `Review recent charges for fraud flags and alert the Guardian if needed.`

### Integration points

- Syncs every confirmed payment to the Scribe.
- Escalates unresponsive accounts to the Diplomat after three contacts.
- Sends fraud alerts to the Guardian.

---

## 4. Guardian — `partenon-guardian`

**Role**: API keys, models, permissions, audit logging.

**Profile directory**: [`hermes/profiles/partenon-guardian`](../hermes/profiles/partenon-guardian)  
**Config file**: `.security` (see [`templates/.security.example`](../hermes/profiles/partenon-guardian/templates/.security.example))  
**Skill docs**: [`skills/security/SKILL.md`](../hermes/profiles/partenon-guardian/skills/security/SKILL.md)

### Real tools

| Tool file | Function | What it does |
|-----------|----------|--------------|
| `tools/key_manager.py` | `list_keys()` | Lists provider keys with masked fingerprints and rotation status. |
| `tools/key_manager.py` | `rotate_key(provider)` / `rotate_keys(providers)` | Updates the env var reference and timestamps. The actual key must be replaced manually. |
| `tools/key_manager.py` | `audit_access(profile)` | Returns canonical tools/MCP/files for a profile and flags violations. |
| `tools/key_manager.py` | `validate_access(profile, resource, action)` | Returns allow/deny with reason. |
| `tools/key_manager.py` | `get_model_recommendation(task)` | Recommends provider/model for a task type. |
| `tools/policy_manager.py` | `set_policies(profile, permissions)` | Writes an RBAC policy JSON for operator review. |
| `tools/secrets_manager.py` | `manage_secrets(action, key_id, value)` | Vault-style CRUD for secret references. |
| `tools/audit_logger.py` | `audit_log(event_type, profile, resource, action, status)` | Appends JSON Lines events to `data/audit/security.log`. |
| `tools/audit_logger.py` | `get_audit_logs(...)` | Reads and filters audit logs. |
| `tools/gpu_allocator.py` | `allocate_gpu(profile, model_name, requested_gpus)` | Returns a deterministic GPU allocation object for NVIDIA use. |

### MCP servers and env vars

- **MCP**: `gbrain`.
- **Required env**: `OPENROUTER_API_KEY`.
- **Optional env**: `NVIDIA_API_KEY`, `OPENAI_API_KEY`, `KIMI_API_KEY`, `STRIPE_SECRET_KEY` (for rotation tracking).

### Cron jobs

- `cron/weekly-audit.json` — Mon 09:00: lists keys, audits all seven profiles, flags pending rotations.

### Example prompts

1. `Guardian, list all API keys and flag any that need rotation.`
2. `Audit the permissions for partenon-cobrador and tell me if anything is excessive.`
3. `Rotate the Stripe secret key and log the rotation event.`
4. `Recommend a model for a security audit task.`
5. `Show the last 50 audit log entries for the Collector profile.`

### Integration points

- Audits every profile against `.security` templates.
- Writes rotation and access events to the Brain/G-Brain under `security/events`.
- Alerts the Strategist if a profile request is blocked for more than 48 hours.

---

## 5. Strategist — `partenon-estratega`

**Role**: projects, tasks, calendar, goals, briefings, operations.

**Profile directory**: [`hermes/profiles/partenon-estratega`](../hermes/profiles/partenon-estratega)  
**Config file**: `.ops` (see [`templates/.ops.example`](../hermes/profiles/partenon-estratega/templates/.ops.example))  
**Skill docs**: [`skills/ops/SKILL.md`](../hermes/profiles/partenon-estratega/skills/ops/SKILL.md)

### Real tools

| Tool file | Function | What it does |
|-----------|----------|--------------|
| `tools/projects.py` | `Projects.create_project(name, client_id, delivery_date, amount)` | Creates a project in `data/projects.json`. |
| `tools/projects.py` | `Projects.update_status(project_id, status)` | Moves project through planned/in_progress/paused/completed/canceled/delivered. |
| `tools/tasks.py` | `Tasks.create_task(project_id, title, assignee, due_date, priority)` | Creates a task in `data/tasks.json`. |
| `tools/tasks.py` | `Tasks.complete_task(task_id, comment)` | Marks a task done. |
| `tools/checklists.py` | `Checklists.create_project_checklist(project_id, industry)` | Generates phase checklists from templates (events, legal, consulting, retail). |
| `tools/goals.py` | `GoalsEngine.create_goal(title, type, department, target, kpi_source)` | Creates an OKR-like goal with optional auto-tracking. |
| `tools/briefings.py` | `Briefings.generate_morning_briefing(user_name)` | Returns a text briefing with goals, critical tasks, pipeline, finances. |
| `tools/calendar.py` | `Calendar.create_event(title, start, end, attendees)` | Creates a calendar record. |
| `tools/email.py` | `Email.send_email(to, subject, body)` | Drafts/records an email. |

### MCP servers and env vars

- **MCP**: `google_workspace`, `gmail`, `gbrain`.
- **Required env**: `OPENROUTER_API_KEY`, `GOOGLE_SERVICE_ACCOUNT_JSON`.

### Cron jobs

- `cron/morning-briefing.json` — Mon-Fri 08:00.
- `cron/midday-pulse.json` — Mon-Fri 14:00.
- `cron/weekly-planning.json` — Mon 09:00.
- `cron/weekly-retro.json` — Sun 20:00.

### Example prompts

1. `Strategist, create a project "Website redesign" for client CLI-001 with delivery on 2026-10-15 and amount $25,000.`
2. `Create a checklist for PROJ-001 using the consulting template.`
3. `Assign "Confirm catering" to Ana with high priority and due 2026-07-01.`
4. `Set a weekly goal: close 2 contracts, tracked from pipeline.contracted.`
5. `Generate the morning briefing for today.`

### Integration points

- Reads Scribe budgets before committing to project spending.
- Syncs client milestones with the Diplomat.
- Sends campaign dates to the Herald.
- Alerts when tasks are blocked for more than 48 hours.

---

## 6. Diplomat — `partenon-diplomatico`

**Role**: clients, vendors, contracts, follow-ups, proposals, CRM.

**Profile directory**: [`hermes/profiles/partenon-diplomatico`](../hermes/profiles/partenon-diplomatico)  
**Config file**: `.relations` (see [`templates/.relations.example`](../hermes/profiles/partenon-diplomatico/templates/.relations.example))  
**Skill docs**: [`skills/relations/SKILL.md`](../hermes/profiles/partenon-diplomatico/skills/relations/SKILL.md)

### Real tools

| Tool file | Function | What it does |
|-----------|----------|--------------|
| `tools/crm.py` | `RelationsCRM.add_client(name, ...)` / `add_vendor(...)` | Adds entities to `.relations`. |
| `tools/crm.py` | `RelationsCRM.add_milestone(entity_id, description, date)` | Adds a milestone. |
| `tools/crm.py` | `RelationsCRM.confirm_milestone(milestone_id)` | Marks a milestone confirmed in writing. |
| `tools/crm.py` | `RelationsCRM.add_communication(entity_id, channel, subject, summary, next_step)` | Logs a call/email/meeting. |
| `tools/crm.py` | `RelationsCRM.rate_relationship(entity_id, rating, reason)` | Rates A/B/C/D. |
| `tools/crm.py` | `RelationsCRM.get_relationship_summary(entity_id)` | Returns activity, milestones, rating. |
| `tools/followups.py` | `run_daily_followups(alert_days, channels)` | Returns pending reminders and milestones. |
| `tools/schedule_meeting.py` | `schedule_meeting(attendees, date, duration)` | Creates a meeting record and calendar payload. |
| `tools/generate_proposal.py` | `generate_proposal(client_id, scope_items, ...)` | Drafts a proposal from `.relations` data. |
| `tools/sync_contacts.py` | `sync_contacts(provider, api_key)` | Exports/imports `.relations` contacts to HubSpot or Salesforce payloads. |

### MCP servers and env vars

- **MCP**: `google_workspace`, `gmail`, `gbrain`.
- **Required env**: `OPENROUTER_API_KEY`, `GOOGLE_SERVICE_ACCOUNT_JSON`.
- **Optional env**: `CRM_PROVIDER`, `CRM_API_KEY`, `HUBSPOT_ACCESS_TOKEN`, Salesforce vars.

### Cron jobs

- `cron/daily-followups.json` — 08:00 daily: pending follow-ups, milestones, reminders.

### Example prompts

1. `Diplomat, register client "Example Inc" with contact contact@example.test and rating B.`
2. `Add a milestone "Proposal delivery" for Example Inc on 2026-06-30.`
3. `Log yesterday's call with Example Inc: scope adjusted, new version due June 28.`
4. `Run daily follow-ups and draft reminder emails for anyone with a milestone in 3 days.`
5. `Generate a proposal for CLI-001 including strategy and implementation.`

### Integration points

- Hands agreed payment plans to the Collector.
- Sends deadline changes to the Strategist for capacity validation.
- Shares client-facing copy with the Herald for review.

---

## 7. Brain — `partenon-brain`

**Role**: collective memory, context, conflict detection, onboarding context.

**Profile directory**: [`hermes/profiles/partenon-brain`](../hermes/profiles/partenon-brain)  
**Config file**: `.brain` (see [`templates/.brain.example`](../hermes/profiles/partenon-brain/templates/.brain.example))  
**Skill docs**: [`skills/memory/SKILL.md`](../hermes/profiles/partenon-brain/skills/memory/SKILL.md)

### Real tools

| Tool file | Function | What it does |
|-----------|----------|--------------|
| `tools/gbrain_client.py` | `GBrainClient.put_page(slug, content, tags)` | Saves a page to G-Brain. |
| `tools/gbrain_client.py` | `GBrainClient.get_page(slug)` | Retrieves a page. |
| `tools/gbrain_client.py` | `GBrainClient.search(query)` | Hybrid text search across pages. |
| `tools/gbrain_client.py` | `GBrainClient.conflicts(profile)` | Detects contradictory decisions. |
| `tools/mcp_hub.py` | `share_context(context_type, data, access)` | Publishes shared context for other heroes. |
| `tools/mcp_hub.py` | `find_patterns(pattern, sources)` | Searches for a pattern across sources. |
| `tools/mcp_hub.py` | `orchestrate_agents(agents, task)` | Saves an orchestration plan. |
| `tools/mcp_hub.py` | `generate_insight(pattern, sources)` | Produces an insight report. |
| `tools/sync.py` | `collect_learnings(since_hours)` / `collect_decisions(status)` | Gathers recent validated outputs. |
| `tools/sync.py` | `index_in_gbrain(items)` | Indexes a batch with tags and links. |

### MCP servers and env vars

- **MCP**: `gbrain`.
- **Required env**: `GBRAIN_DATABASE_URL` (note: `gbrain/server.py` reads `GBrain_DATABASE_URL`), `OPENROUTER_API_KEY`.

### Cron jobs

- `cron/daily-memory-sync.json` — 02:00 daily: collects learnings and decisions, indexes them in G-Brain.

### Example prompts

1. `Brain, index yesterday's decision: "We will not offer fixed-price projects under $5,000."`
2. `Search for previous learnings about cash-flow management.`
3. `Are there any contradictions between Strategist decisions and Scribe proposals?`
4. `Generate an insight report on projects that repeatedly miss deadlines.`
5. `Prepare onboarding context for a new Diplomat joining the company.`

### Integration points

- Every hero writes validated learnings to the Brain.
- The Brain answers context questions before the heroes act.
- It flags conflicts to the Strategist for resolution.

---

## Running a profile tool directly

Most tools have a `main()` entry point so you can test them without Hermes:

```bash
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/templates.py
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/content_calendar.py "automation for SMEs" linkedin,instagram 7
python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py
python3 hermes/profiles/partenon-estratega/skills/ops/tools/briefings.py
python3 hermes/profiles/partenon-diplomatico/skills/relations/tools/crm.py
python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py
```

For the full list of available tools per profile, inspect the `skills/<skill>/tools/` directory.
