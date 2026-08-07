# Stock Bloc Quant Terminal — Backend Data Contract

This repository serves as the automated data backend and single source of truth for the Stock Bloc terminal (https://stock-bloc.ai.studio).

## Data Endpoints & Refresh Schedule

| Endpoint / File | Refresh Frequency | Primary Sources | Description |
| :--- | :--- | :--- | :--- |
| `sec_intel_data.json` | Daily (Midnight UTC) | SEC EDGAR API | Institutional 13F-HR filings, 10-K, and 10-Q disclosures for top funds. |
| `market_watchlist_data.json` | Daily / Hourly | Yahoo Finance API & RSS | Real-time quotes, 24h % change, 7D sparklines, and live headlines for 31 tickers. |
| `dyson_swarm_data.json` | Daily (Midnight UTC) | Skyrocket LL2 API & SpaceX IR | Starlink active fleet counts, photovoltaic harvest GW, and launch manifests. |
| `intel_news_feed.json` | Daily (Midnight UTC) | YouTube RSS | Curated video intel featuring @stockbloc, @alexwg, @allin, and @peterdiamandis. |

## Raw JSON Links (Agent Surface)

- **SEC Intel:** `https://raw.githubusercontent.com/Jaywestphilly/stock-bloc-backend/main/sec_intel_data.json`
- **Market Watchlist:** `https://raw.githubusercontent.com/Jaywestphilly/stock-bloc-backend/main/market_watchlist_data.json`
- **Dyson Swarm:** `https://raw.githubusercontent.com/Jaywestphilly/stock-bloc-backend/main/dyson_swarm_data.json`
- **Intel Feed:** `https://raw.githubusercontent.com/Jaywestphilly/stock-bloc-backend/main/intel_news_feed.json`
