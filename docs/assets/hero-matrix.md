# Partenon Hero Capability Matrix

| Hero | Profile directory | Primary file | Default model | Required MCP servers | Cron jobs | Real tools (Python) | What it produces |
|------|-------------------|--------------|---------------|----------------------|-----------|---------------------|------------------|
| **Scribe** / Treasurer | `hermes/profiles/partenon-tesorero/` | `.finance` | `openrouter/anthropic/claude-opus-4` | `google_workspace`, `gbrain` | Daily report, weekly budget review | `skills/finance/tools/audit.py`, `google_sheets.py`, `parsers.py`, `templates.py` | Expense workbook, margin report, Google Sheets dashboard |
| **Herald** / Messenger | `hermes/profiles/partenon-mensajero/` | `.design` | `openrouter/google/gemini-2.5-flash-preview-05-20` | `google_workspace`, `gbrain`, `gmail`, `social_media`, `open_design` | Morning briefing, midday pulse, weekly content plan | `skills/comms/tools/copy_generator.py`, `content_calendar.py`, `seo_geo_optimizer.py`, `presentation_builder.py`, `publish_post.py`, `brand_intake.py` | Brand brief, content calendar, copy, slide deck |
| **Collector** | `hermes/profiles/partenon-cobrador/` | `.payments` | `openrouter/deepseek/deepseek-chat` | `stripe`, `google_workspace`, `gbrain` | Daily collection review, daily follow-ups | `skills/payments/tools/stripe_tools.py` | Payment links, subscriptions, invoices, collection reminders, fraud flags |
| **Guardian** | `hermes/profiles/partenon-guardian/` | `.security` | `openrouter/anthropic/claude-opus-4` | `gbrain` | Weekly security audit | `skills/security/tools/key_manager.py`, `audit_logger.py`, `policy_manager.py`, `secrets_manager.py`, `gpu_allocator.py` | Key rotation log, permission audit, security event log |
| **Strategist** | `hermes/profiles/partenon-estratega/` | `.ops` | `openrouter/anthropic/claude-opus-4` | `google_workspace`, `gbrain`, `gmail` | Morning briefing, midday pulse, weekly planning, weekly retro | `skills/ops/tools/projects.py`, `tasks.py`, `checklists.py`, `goals.py`, `briefings.py`, `calendar.py`, `email.py`, `notes.py` | Project plan, task list, calendar events, morning briefing |
| **Diplomat** | `hermes/profiles/partenon-diplomatico/` | `.relations` | `openrouter/google/gemini-2.5-flash-preview` | `google_workspace`, `gbrain`, `gmail` | Daily follow-ups | `skills/relations/tools/crm.py`, `followups.py`, `schedule_meeting.py`, `generate_proposal.py`, `log_interaction.py`, `auto_followup.py`, `sync_contacts.py` | CRM sheet, meeting invite, proposal draft, follow-up report |
| **Brain** | `hermes/profiles/partenon-brain/` | `.brain` | `openrouter/anthropic/claude-opus-4` | `gbrain` | Daily memory sync | `skills/memory/tools/gbrain_client.py`, `mcp_hub.py`, `sync.py` | Memory pages, insight summaries, onboarding context |

Legend:

- **Profile directory**: where the Hermes Agent profile lives.
- **Primary file**: the per-company config the hero reads first.
- **Required MCP servers**: declared in `config.yaml`; some are optional depending on integrations.
- **Cron jobs**: JSON schedules in `hermes/profiles/<profile>/cron/`.
- **Real tools**: actual Python files in the repository today; others are stubs or planned.
