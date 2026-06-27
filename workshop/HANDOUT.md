# Partenon Hermes Onboarding Workshop — Participant Handout

## One-sentence summary

Partenon is a system of seven specialized AI heroes that share a single business context. Hermes is the company itself. Each hero handles one domain: money, message, money-in, security, operations, relationships, and memory.

## The seven heroes

| Hero | Domain | Typical first question |
|---|---|---|
| Scribe (Tesorero) | Finance | "How much money do I have?" |
| Herald (Mensajero) | Communications | "What should I post this week?" |
| Collector (Cobrador) | Payments | "Send an invoice to this client." |
| Guardian (Guardian) | Security | "Who has access to what?" |
| Strategist (Estratega) | Operations | "What is the next priority?" |
| Diplomat (Diplomatico) | Relationships | "When do I follow up?" |
| Brain (Cerebro) | Memory | "What did we decide last month?" |

## Onboarding flow

1. **Pick the first hero.** Usually Scribe for product/cash businesses, Strategist for service/project businesses, or Guardian for SaaS/security-heavy businesses.
2. **Run the brand interview.** The Herald asks six questions and writes `.design`.
3. **Create the first project.** The Strategist adds tasks and checklists.
4. **Add clients/vendors and a milestone.** The Diplomat builds the relationship map.
5. **Issue a payment link or invoice.** The Collector stores the transaction.
6. **Plan communications.** The Herald generates a content calendar.
7. **Review keys and access.** The Guardian audits credentials.

## Files the system creates

| File | Created by | Why it matters |
|---|---|---|
| `.finance` | Scribe | Budgets, actuals, alerts |
| `.design` | Herald | Brand voice, colors, audiences |
| `.payments` | Collector | Payment links, subscriptions, invoices |
| `.security` | Guardian | API keys, access inventory |
| `.ops` | Strategist | Projects, tasks, checklists |
| `.relations` | Diplomat | Clients, vendors, milestones |
| `.brain` | Brain | Memory, decisions, summaries |

## Real business examples

The workshop includes five case studies:

- **Joe Coffee Company** — New York coffee shop / roaster
- **Single Grain** — digital marketing agency
- **SpawGlass** — Texas commercial construction contractor
- **Tracksmith** — athletic apparel retail / e-commerce
- **Buffer** — bootstrapped social-media SaaS

## Green, yellow, red

- **Green:** works out of the box after install.
- **Yellow:** works locally; needs live credentials or third-party account.
- **Red:** not implemented; requires engineering.

Use `workshop/checklists/PRODUCTION_READINESS.md` to score your own business.

## Quick commands to try

```bash
# Route a question to a hero
python3 workshop/simulations/sim_runner.py route "organize my numbers"

# Run a brand interview
python3 workshop/simulations/sim_runner.py design joe \
  "Joe Coffee Company" food "New York, NY" \
  "On-site roasted coffee and cafe service" \
  "New York coffee lovers and remote workers" \
  "Roast small batches, serve classic drinks, and host local events" \
  direct informal "Owner" instagram,facebook

# Create the first project
python3 workshop/simulations/sim_runner.py project joe \
  "Launch cold-brew subscription" "Local subscriber" 2026-09-01 12000 food

# Add a payment link
python3 workshop/simulations/sim_runner.py payment-link joe \
  "Cold Brew Subscription" 2800 usd

# Generate a morning briefing
python3 workshop/simulations/sim_runner.py briefing joe morning

# Audit keys
python3 workshop/simulations/sim_runner.py keys
```

## Common pitfalls

- Trying to activate all seven heroes at once. Start with two or three.
- Forgetting to create `config/company.yaml` for live Google/Stripe integrations.
- Treating the Collector as accounting. It handles money-in; the Scribe tracks books.
- Expecting automatic memory sharing without G-Brain wired.

## Further reading

- `docs/ENTREPRENEUR_PLAYBOOK.md`
- `docs/HERO_GUIDE.md`
- `workshop/guides/HERMES_ONBOARDING.md`
- `workshop/checklists/PRODUCTION_READINESS.md`
