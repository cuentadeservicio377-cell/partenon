# Partenon Hero Capability Matrix

| Hero | Profile directory | Config file | Primary tools (Python) | MCP servers | Cron jobs | Key handoffs |
|------|-------------------|-------------|------------------------|-------------|-----------|--------------|
| **Scribe** (Treasurer) | [`hermes/profiles/partenon-tesorero`](../../hermes/profiles/partenon-tesorero) | `.finance` | `google_sheets.py`, `parsers.py`, `templates.py`, `audit.py` | `google_workspace`, `gbrain` | `daily-report.json` (07:00), `weekly-content.json` (Mon 08:00) | Shares budget with Herald; records income from Collector |
| **Herald** (Messenger) | [`hermes/profiles/partenon-mensajero`](../../hermes/profiles/partenon-mensajero) | `.design` | `brand_intake.py`, `copy_generator.py`, `content_calendar.py`, `seo_geo_optimizer.py`, `presentation_builder.py`, `publish_post.py` | `google_workspace`, `gmail`, `social_media`, `open_design`, `gbrain` | `morning-briefing.json` (07:30), `midday-pulse.json` (13:00), `weekly-content.json` (Mon 09:00) | Reads campaign budget from Scribe; coordinates dates with Strategist |
| **Collector** | [`hermes/profiles/partenon-cobrador`](../../hermes/profiles/partenon-cobrador) | `.payments` | `stripe_tools.py` | `stripe`, `google_workspace`, `gbrain` | `daily-collection.json` (09:00), `daily-followups.json` (17:00) | Records payments with Scribe; escalates disputes to Diplomat; fraud to Guardian |
| **Guardian** | [`hermes/profiles/partenon-guardian`](../../hermes/profiles/partenon-guardian) | `.security` | `key_manager.py`, `audit_logger.py`, `policy_manager.py`, `secrets_manager.py`, `gpu_allocator.py` | `gbrain` | `weekly-audit.json` (Mon 09:00) | Audits all profiles; recommends models for sensitive tasks |
| **Strategist** | [`hermes/profiles/partenon-estratega`](../../hermes/profiles/partenon-estratega) | `.ops` | `projects.py`, `tasks.py`, `checklists.py`, `goals.py`, `briefings.py`, `calendar.py` | `google_workspace`, `gmail`, `gbrain` | `morning-briefing.json` (08:00), `midday-pulse.json` (14:00), `weekly-planning.json` (Mon 09:00), `weekly-retro.json` (Sun 20:00) | Syncs milestones with Diplomat; reads budgets from Scribe |
| **Diplomat** | [`hermes/profiles/partenon-diplomatico`](../../hermes/profiles/partenon-diplomatico) | `.relations` | `crm.py`, `followups.py`, `schedule_meeting.py`, `generate_proposal.py`, `sync_contacts.py` | `google_workspace`, `gmail`, `gbrain` | `daily-followups.json` (08:00) | Hands payment plans to Collector; deadlines to Strategist; copy to Herald |
| **Brain** | [`hermes/profiles/partenon-brain`](../../hermes/profiles/partenon-brain) | `.brain` | `gbrain_client.py`, `mcp_hub.py`, `sync.py` | `gbrain` | `daily-memory-sync.json` (02:00) | Indexes learnings from all heroes; feeds onboarding context |

## Status notes

- All profiles can run in **standalone local mode** without Hermes CLI. The tools read local `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations`, and `.brain` files and write to `data/` and `output/`.
- Live integrations (Google Workspace, Stripe, G-Brain) require credentials set in `.env`.
- The intent router in `partenon-core/tools/router.py` maps natural language to the `profile` column above.
