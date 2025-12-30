# mcpsmuggler

FastMCP wrapper for the Smuggler HTTP Request Smuggling scanner, packaged for Render via Docker.

## What this does
- Exposes an MCP server with a single tool: `do_smuggler`
- Runs the Smuggler CLI (`smuggler -u <url> ...`) inside the container
- Uses SSE transport on `/mcp` (FastMCP default)

## Running locally
```bash
git clone https://github.com/ozgurozkan123/mcpsmuggler.git
cd mcpsmuggler
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python server.py  # starts on http://0.0.0.0:8000/mcp
```

## Render deployment (Docker)
Render will auto-detect the Dockerfile:
- Runtime: Docker
- Exposed port: `PORT` env (Render sets this)
- Start command: handled by Dockerfile (`python server.py`)

If using Render UI:
1) Create a **Web Service**
2) Connect this repo and choose **Docker**
3) Leave root directory empty, Dockerfile path = `Dockerfile`
4) No build/start commands needed

## MCP client config examples
```json
{
  "mcpServers": {
    "mcpsmuggler": {
      "url": "https://<your-render-url>/mcp"
    }
  }
}
```

