"""Partenon Slack notification MCP server."""

from mcp.server.fastmcp import FastMCP

from mcp_servers.notifications.slack import notify_task_overdue, send_message

mcp = FastMCP("partenon-slack")


@mcp.tool()
def slack_send_message(channel: str, text: str) -> dict:
    """Send a message to a Slack channel."""
    return send_message(channel, text)


@mcp.tool()
def slack_notify_task_overdue(task_id: str, title: str, due_date: str, channel: str = "#general") -> dict:
    """Notify Slack that a task is overdue."""
    return notify_task_overdue(task_id, title, due_date, channel)


if __name__ == "__main__":
    mcp.run()
