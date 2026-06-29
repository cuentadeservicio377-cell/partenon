# Gateway Setup Guide

This guide configures the Partenon Hermes gateway so users can talk to the heroes through Telegram and Email.

## What the gateway does

- Parses slash commands (`/s`, `/h`, `/c`, `/g`, `/st`, `/d`, `/b`) and full profile names.
- Routes attachments to the right hero (spreadsheets to Scribe, images to Herald, contracts to Diplomat).
- Guards inbound messages with allow-lists and rate limits.
- Runs the progressive onboarding conversation when a new user first contacts Partenon.

## Prerequisites

- A running Partenon installation.
- Python 3.10+ and the project virtual environment activated.
- The `mcp` package installed (`pip install -e .` or `uv pip install -e .`).

## 1. Telegram bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the prompts to create a bot.
3. Copy the bot token (looks like `123456:ABC-DEF...`).
4. Optionally set a username for the bot, e.g. `@partenon_gateway_bot`.

## 2. Environment variables

Copy `.env.example` to `.env` if you have not already:

```bash
cp .env.example .env
```

Add the gateway variables:

```bash
# Telegram adapter
TELEGRAM_BOT_TOKEN=123456:YOUR_BOT_TOKEN_HERE
TELEGRAM_ALLOWED_USERS=123456789,987654321

# Email adapter
EMAIL_ACCOUNT=partenon@example.com
EMAIL_PASSWORD=your-app-password

# Shared gateway guard
GATEWAY_ALLOWED_USERS=owner@example.com,123456789
GATEWAY_RATE_LIMIT_PER_MINUTE=30
```

Notes:

- `TELEGRAM_ALLOWED_USERS` is a comma-separated list of Telegram user IDs. The bot will deny everyone else.
- `GATEWAY_ALLOWED_USERS` can be used for the Email adapter or as a fallback list.
- If neither `GATEWAY_ALLOWED_USERS` nor `TELEGRAM_ALLOWED_USERS` is set, the gateway denies all requests by default.
- For Gmail, use an app-specific password instead of your account password.

## 3. Gateway configuration file

The template is at `config/hermes_gateway.yaml`. It uses env references so you do not commit secrets:

```yaml
gateway:
  default_profile: partenon-scribe
  adapters:
    telegram:
      enabled: true
      bot_token: "${TELEGRAM_BOT_TOKEN}"
      allowed_users: "${TELEGRAM_ALLOWED_USERS}"
    email:
      enabled: true
      account: "${EMAIL_ACCOUNT}"
      password: "${EMAIL_PASSWORD}"
      allowed_users: "${GATEWAY_ALLOWED_USERS}"
  guard:
    rate_limit_per_minute: "${GATEWAY_RATE_LIMIT_PER_MINUTE:-30}"
```

Customize `default_profile` if you want messages without a profile hint to go to a different hero.

## 4. Select a Partenon profile

The gateway skill is auto-loaded by every Partenon profile. Choose the profile that best matches the primary channel:

```bash
hermes profile use hermes/profiles/partenon-scribe
```

For a general-purpose inbound channel, `partenon-scribe` is a safe default because the gateway will still route commands to the correct hero.

## 5. Run the gateway

From the project root:

```bash
source .venv/bin/activate
hermes gateway setup --config config/hermes_gateway.yaml
hermes gateway run
```

If `hermes gateway` is not available, run the adapter directly:

```bash
python -m mcp_servers.gateway.telegram_adapter
```

## 6. First interaction

Send a direct message to the bot:

```text
Hello
```

The gateway will start the onboarding conversation:

```text
Welcome to Partenon. What is your company name?
```

After collecting company name, industry, team size, and main pain point, the gateway creates the workspace and first missions.

## 7. Routing examples

```text
/s register client Acme Inc
/h create a summer campaign
/c generate payment link 250 USD
/g rotate my OpenAI key
/st what do we have pending this week?
/d follow up with vendor Beta Supply
/b remember we decided to use Stripe
```

## 8. Troubleshooting

- **"No allowed users configured"**: Add at least one user ID to `TELEGRAM_ALLOWED_USERS` or `GATEWAY_ALLOWED_USERS`.
- **"Bot must be mentioned in a group chat"**: In groups, tag the bot (`@partenon_gateway_bot`) or add `@botname` for testing.
- **"Rate limit reached"**: Increase `GATEWAY_RATE_LIMIT_PER_MINUTE` or wait one minute.
- **Onboarding not persisting**: Verify `GBRAIN_DATABASE_URL` points to a writable SQLite or PostgreSQL database.
