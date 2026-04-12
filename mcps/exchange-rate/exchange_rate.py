"""MCP server for ExchangeRate-API v6 (pair + latest endpoints).

Pair conversion JSON (success):
  result, base_code, target_code, conversion_rate,
  optional conversion_result (when amount in URL),
  time_last_update_utc, time_next_update_utc, documentation, terms_of_use

Pair JSON (error):
  result: "error", "error-type": unsupported-code | malformed-request | ...
"""

from typing import Any

import httpx
from decouple import config
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("exchange-rate-mcp")

EXCHANGE_RATE_API_KEY = config("EXCHANGE_RATE_API_KEY")
EXCHANGE_RATE_API_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}"


def _normalize_pair(from_currency: str, to_currency: str) -> tuple[str | None, str | None]:
    a = from_currency.strip().upper()
    b = to_currency.strip().upper()
    if len(a) != 3 or len(b) != 3 or not a.isalpha() or not b.isalpha():
        return None, None
    return a, b


def _format_pair_success(data: dict[str, Any], include_amount_line: bool) -> str:
    rate = data.get("conversion_rate")
    base = data.get("base_code")
    target = data.get("target_code")
    last = data.get("time_last_update_utc", "—")
    nxt = data.get("time_next_update_utc", "—")
    lines = [
        f"Pair: {base} → {target}",
        f"Conversion rate: 1 {base} = {rate} {target}",
        f"Last update (UTC): {last}",
        f"Next update (UTC): {nxt}",
    ]
    if include_amount_line and "conversion_result" in data:
        lines.insert(
            2,
            f"Converted amount: {data.get('conversion_result')} {target}",
        )
    return "\n".join(lines)


def _format_api_error(data: dict[str, Any]) -> str:
    err = data.get("error-type") or data.get("error_type") or "unknown"
    hints = {
        "unsupported-code": "Use ISO 4217 codes supported by ExchangeRate-API.",
        "malformed-request": "Check base/target/amount format.",
        "invalid-key": "Set EXCHANGE_RATE_API_KEY in your environment.",
        "inactive-account": "Confirm your ExchangeRate-API account email.",
        "quota-reached": "Plan request limit reached; upgrade or wait for reset.",
    }
    extra = hints.get(err, "")
    return f"ExchangeRate-API error ({err}). {extra}".strip()


def _format_latest_success(data: dict[str, Any]) -> str:
    base = data.get("base_code", "?")
    rates = data.get("conversion_rates")
    if not isinstance(rates, dict):
        return f"Unexpected latest response shape for base {base}."
    # Show a short preview; full dict can be huge
    sample = list(rates.items())[:15]
    preview = "\n".join(f"  {c}: {v}" for c, v in sample)
    more = f"\n  … and {len(rates) - len(sample)} more codes" if len(rates) > len(sample) else ""
    last = data.get("time_last_update_utc", "—")
    return (
        f"Latest rates for base {base} (UTC last update: {last})\n"
        f"Sample conversion_rates:\n{preview}{more}"
    )


async def _make_request(url: str) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


@mcp.tool()
async def get_rates_from_base(base_currency: str) -> str:
    """Fetch latest conversion_rates for a base currency (v6 /latest/{base}).

    Response uses result: success|error; on success includes base_code and conversion_rates.
    """
    base = base_currency.strip().upper()
    if len(base) != 3 or not base.isalpha():
        return "base_currency must be a 3-letter ISO code (e.g. USD)."

    url = f"{EXCHANGE_RATE_API_URL}/latest/{base}"
    data = await _make_request(url)
    if not data:
        return "Could not reach ExchangeRate-API or invalid HTTP response."

    if data.get("result") == "error":
        return _format_api_error(data)

    if data.get("result") != "success":
        return f"Unexpected response: {data!r}"

    return _format_latest_success(data)


@mcp.tool()
async def convert_currency_amount(
    from_currency: str, to_currency: str, amount: float
) -> str:
    """Convert an amount using the pair endpoint with optional AMOUNT in the path.

    Success JSON includes conversion_rate and conversion_result.
    """
    if amount < 0:
        return "amount must be non-negative."

    a, b = _normalize_pair(from_currency, to_currency)
    if not a or not b:
        return "from_currency and to_currency must be 3-letter ISO codes."

    url = f"{EXCHANGE_RATE_API_URL}/pair/{a}/{b}/{amount}"
    data = await _make_request(url)
    if not data:
        return "Could not reach ExchangeRate-API or invalid HTTP response."

    if data.get("result") == "error":
        return _format_api_error(data)

    if data.get("result") != "success":
        return f"Unexpected response: {data!r}"

    return _format_pair_success(data, include_amount_line=True)


@mcp.tool()
async def get_standard_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Minimal pair rate (no amount): base_code, target_code, conversion_rate only."""
    a, b = _normalize_pair(from_currency, to_currency)
    if not a or not b:
        return "from_currency and to_currency must be 3-letter ISO codes."

    url = f"{EXCHANGE_RATE_API_URL}/pair/{a}/{b}"
    data = await _make_request(url)
    if not data:
        return "Could not reach ExchangeRate-API or invalid HTTP response."

    if data.get("result") == "error":
        return _format_api_error(data)

    if data.get("result") != "success":
        return f"Unexpected response: {data!r}"

    return _format_pair_success(data, include_amount_line=False)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
