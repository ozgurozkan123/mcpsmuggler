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
            Examples:
              -m GET      -> specify HTTP method
              -v host.com -> virtual host
              -x          -> exit on first finding
              -t 10       -> set socket timeout
    Returns:
        Combined stdout/stderr output from Smuggler with ANSI codes stripped.
    """
    args = smuggler_args or []

    # Prefer installed console script; fallback to module invocation
    base_cmd = ["smuggler", "-u", url]
    cmd = base_cmd + args

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    stdout, _ = await process.communicate()
    output = stdout.decode()

    cleaned = strip_ansi(output)

    # Non-zero exit still returns output for debugging
    return cleaned


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    mcp.run(transport="sse", host=host, port=port, path="/mcp")
