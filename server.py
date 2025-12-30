import asyncio
import os
import re
from fastmcp import FastMCP
from typing import List

mcp = FastMCP("smuggler-mcp")

ansi_pattern = re.compile(r"\x1B\[[0-9;]*[mGK]")

def strip_ansi(text: str) -> str:
    return ansi_pattern.sub("", text)

@mcp.tool()
async def do_smuggler(url: str, smuggler_args: List[str] | None = None) -> str:
    """
    Run Smuggler to detect HTTP Request Smuggling vulnerabilities.

    Args:
        url: Target URL to scan (e.g. https://example.com)
        smuggler_args: Additional arguments passed directly to Smuggler
    Returns:
        Combined stdout/stderr output from Smuggler with ANSI codes stripped.
    """
    args = smuggler_args or []

    smuggler_path = os.getenv("SMUGGLER_PATH", "/opt/smuggler/smuggler.py")
    cmd = ["python3", smuggler_path, "-u", url, *args]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    stdout, _ = await process.communicate()
    output = stdout.decode()

    cleaned = strip_ansi(output)

    return cleaned


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    mcp.run(transport="http", host=host, port=port, path="/mcp/")
