# Frankfurter MCP

[MCP](https://modelcontextprotocol.io) server for currency conversion using the [Frankfurter v1](https://www.frankfurter.dev/v1/) HTTP API (`api.frankfurter.dev/v1`, `base` + `symbols` for latest rates; no API key).

## Tools

- **convert_currency** — Convert an amount between two ISO 4217 currencies.
- **get_exchange_rate** — Mid-market rate for 1 unit of source → target.
- **list_supported_currencies** — Supported currency codes and names.

## Run (stdio)

```bash
cd mcps/frankfurter-mcp
uv sync
uv run python frankfurter.py
```

Register in your MCP client with `command` + `cwd` pointing at this directory.
