"""Server-Sent Events stream route."""

import asyncio

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import StreamingResponse

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.events import get_bus

router = APIRouter(prefix="/stream", tags=["stream"])


@router.get("")
async def stream_events(
    request: Request,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> StreamingResponse:
    """Stream live mission, cron, and event updates to the dashboard."""
    bus = get_bus()
    queue = bus.subscribe()

    # Send an initial connected event so the client knows the stream is alive.
    await queue.put({
        "type": "stream.connected",
        "payload": {"workspace_id": ctx.workspace_id},
        "timestamp": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
    })

    async def event_generator():
        try:
            async for line in bus.stream(queue):
                yield line
        except asyncio.CancelledError:
            bus.unsubscribe(queue)
            raise
        finally:
            bus.unsubscribe(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
        status_code=status.HTTP_200_OK,
    )
