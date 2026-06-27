# Partenon Workshop Handout

## What is Partenon?

Partenon is an AI agent operating system for small businesses. Your company is called **Hermes**. Specialized agents called **heroes** handle finance, marketing, payments, security, operations, relationships, and memory.

## The Seven Heroes

| Hero | Role | File | Starts with |
|------|------|------|-------------|
| Scribe | Finance | `.finance` | Numbers, margins, vendors |
| Herald | Communications | `.design` | Brand, content, calendar |
| Collector | Payments | `.payments` | Invoices, subscriptions, links |
| Guardian | Security | `.security` | API keys, access, audits |
| Strategist | Operations | `.ops` | Projects, tasks, deadlines |
| Diplomat | Relations | `.relations` | Clients, vendors, milestones |
| Brain | Memory | `.brain` | Decisions, learnings, context |

## Install in 3 Commands

```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon
./install.sh
```

Verify:

```bash
python3 scripts/demo_tesorero.py
```

Start dashboard:

```bash
cd dashboard
npm install
npm run dev
```

Login: `admin` / `partenon`

## Pick Your First Heroes

| Business type | Start here |
|---------------|------------|
| Coffee shop / food | Scribe → Strategist → Herald → Collector |
| Marketing agency | Strategist → Diplomat → Scribe → Herald → Collector |
| Construction / events | Strategist → Diplomat → Scribe → Guardian |
| Retail / e-commerce | Scribe → Collector → Herald → Strategist |
| SaaS / tech startup | Guardian → Scribe → Collector → Strategist → Brain |

## Create Your Config Files

```bash
cp hermes/profiles/partenon-tesorero/templates/.finance.example .finance
cp hermes/profiles/partenon-mensajero/templates/.design.example .design
cp hermes/profiles/partenon-estratega/templates/.ops.example .ops
cp hermes/profiles/partenon-cobrador/templates/.payments.example .payments
cp hermes/profiles/partenon-diplomatico/templates/.relations.example .relations
cp hermes/profiles/partenon-guardian/templates/.security.example .security
cp hermes/profiles/partenon-brain/templates/.brain.example .brain
```

## First 30 Days

| Week | Mission | Hero |
|------|---------|------|
| 1 | Upload expenses and see your margin | Scribe |
| 2 | Create your first project and checklist | Strategist |
| 3 | Register top clients or vendors | Diplomat |
| 4 | Set up one payment link or subscription | Collector |

## Important: Start Small

- Do not activate all seven heroes on day one.
- Fill one config file completely before adding another.
- Never store real API keys in `.security` or config files — use `.env`.

## Live vs. Local

| Feature | Works locally | Needs real credentials |
|---------|---------------|------------------------|
| Expense parsing | Yes | — |
| Excel workbook | Yes | — |
| Google Sheets | — | Google service account |
| Payment link placeholder | Yes | — |
| Real Stripe link | — | Stripe secret key |
| Content drafts | Yes | — |
| Social auto-publish | — | Social platform APIs |
| Local memory stub | Yes | — |
| Persistent G-Brain memory | — | G-Brain binary/MCP |

## Resources

- Repo: https://github.com/cuentadeservicio377-cell/partenon
- Live site: https://hermespartenon.online/
- Playbook: `docs/ENTREPRENEUR_PLAYBOOK.md`
- Hero guide: `docs/HERO_GUIDE.md`
- Quickstart: `docs/QUICKSTART.md`
- Gaps: `MISSING_IMPLEMENTATION.md`

## One-Sentence Reminder

**Hermes is your company. Pick the heroes that remove the most friction. Run one mission at a time.**
