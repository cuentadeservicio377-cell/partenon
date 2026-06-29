# Partenon API — production image
# Multi-stage build: compile dependencies as root, run as non-root.

FROM python:3.12-slim-bookworm AS builder

# Install build tools needed for any source wheels.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first so layer caching works when source changes.
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e '.[workspace,payments,slack,db]'

# Copy the application source and install the package itself.
COPY partenon_core/ ./partenon_core/
COPY mcp_servers/ ./mcp_servers/
COPY partenon_api/ ./partenon_api/
COPY hermes/ ./hermes/
COPY skills/ ./skills/
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY config/ ./config/
COPY distribution.yaml ./

# Runtime image — minimal, non-root.
FROM python:3.12-slim-bookworm AS runner

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system --gid 1000 partenon \
    && adduser --system --uid 1000 --ingroup partenon partenon

WORKDIR /app

# Copy installed site-packages and console scripts from the builder stage.
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application source to the same paths used during the editable install.
COPY --from=builder --chown=partenon:partenon /app/ ./

USER partenon

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "partenon_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
