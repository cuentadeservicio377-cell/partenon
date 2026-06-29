"""Shared observability helpers for the Partenon API.

Provides structured logging and Prometheus metrics wiring. The logger uses
structlog when JSON format is requested (``PARTENON_LOG_FORMAT=json``) and
falls back to a plain console renderer otherwise.
"""

import logging
import os
import sys
from typing import Any

import structlog
from prometheus_fastapi_instrumentator import Instrumentator


def configure_logging() -> None:
    """Configure structured logging for the API."""
    json_format = os.environ.get("PARTENON_LOG_FORMAT", "text").lower() == "json"

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if json_format:
        structlog.configure(
            processors=shared_processors
            + [
                structlog.processors.dict_tracebacks,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        structlog.configure(
            processors=shared_processors
            + [
                structlog.dev.ConsoleRenderer(colors=sys.stderr.isatty()),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )

    # Also attach structlog processors to the standard library logging handlers
    # so third-party libraries emit consistent records.
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    structlog.stdlib.recreate_defaults()


def get_logger(name: str = "partenon") -> structlog.stdlib.BoundLogger:
    """Return a configured structured logger."""
    return structlog.get_logger(name)


def setup_metrics(app: Any) -> None:
    """Instrument the FastAPI app and expose Prometheus metrics on /metrics."""
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
