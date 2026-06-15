# NEO_CONNECTOR -- InstagramDataScraper
- service: instagramscraper
- base_url_prod: N/A (no network service -- local CLI tool)
- auth: none (no HTTP surface); the tool itself logs into Instagram with INSTA_USERNAME / INSTA_PASSWORD via Selenium
- env_required: [INSTA_USERNAME, INSTA_PASSWORD]   # both optional -- prompted at runtime if unset (main.py get_credentials)
- generated_at:

## Endpoints

NONE. This repo exposes **no HTTP API, webhook, SSE, WebSocket, cron, or queue**.

Proof from code:
- `requirements.txt` / `pyproject.toml`: only beautifulsoup4, lxml, python-dotenv, selenium, webdriver-manager. No web framework (no flask / fastapi / aiohttp / uvicorn / express / tornado / sanic / bottle).
- `main.py`: a single Selenium browser-automation script. Sole entry point is `main()` (line 557), invoked via `if __name__ == "__main__"` (line 609) or the console script `instagram-scraper = "main:main"` (`pyproject.toml` line 51).
- Grep for `flask|fastapi|aiohttp|uvicorn|@app.|@router|express|app.(get|post|listen)|websocket|sse|webhook|http.server` across `*.py`: no matches (the only `dismissed`/dialog hits are unrelated variable names).
- It is a **client** of the public Instagram web app (navigates `https://www.instagram.com/...` in a Chrome session); it does not serve anything.

### CLI interface (for reference only -- NOT a Neo HTTP tool)
Invocation: `python main.py [flags]` (interactive: prompts for credentials and/or output name; can pause for manual navigation).

| flag | type | required | description |
|------|------|----------|-------------|
| `--target` | str | no | Instagram username; auto-opens that profile's Followers modal and scrapes it (main.py line 546, 583). If omitted, runs interactive feed/page mode (line 588: prompts "Navigate to the page... press ENTER"). |
| `--output` | str | no | Output CSV name without extension (line 547). Default: `<target>_followers` if `--target` set, else interactive prompt -> `instagram_profiles` (lines 564-569). |
| `--max-minutes` | float | no | Hard time cap; saves and exits gracefully when reached (lines 548-553, 435). |

Output: a CSV file `<name>.csv` written to cwd with a single column `ProfileLink` of full `https://www.instagram.com/<user>/` URLs (save_to_csv, lines 282-289). Saved incrementally every `SAVE_INTERVAL`=25 iterations and on Ctrl+C / completion. Resumable: re-reads an existing CSV to dedup (load_existing_csv, lines 292-304).

Runtime behavior notes (not callable surface): interactive stdin prompts (credentials line 192-193, navigate-then-ENTER line 588), a visible non-headless Chrome window, manual challenge/2FA solving (login lines 235-247), and human-pacing sleeps -- all of which make this unsuitable for unattended HTTP-tool invocation.

## Flows
None (no async generate->poll->result network flow). The internal CLI flow is:
1. `create_driver()` launches Chrome with a persistent profile (`.chrome_profile/`).
2. `is_logged_in()` -> if not, `login()` with env or prompted credentials (manual challenge/2FA solving supported).
3. Either `open_followers_modal(--target)` OR wait for the user to navigate manually and press ENTER.
4. `scrape_profiles()` scrolls + `extract_profile_links()` (BeautifulSoup), dedups, saves CSV every 25 iters.
5. Final CSV saved on completion / time cap / Ctrl+C.

## Gaps
None material for connector purposes. There is no service to connect to.
- Env vars are sourced via `load_dotenv()` + `os.getenv` (main.py lines 54, 192-193); `.env` is gitignored. Var **names** (INSTA_USERNAME, INSTA_PASSWORD) are confirmed in `.env.example`.

---

## Recap for NeoBot wiring
- Endpoints found: **0 HTTP/webhook/SSE/WS**. Covered vs new: N/A.
- **DO NOT wire this repo as Neo HTTP tools.** It is a local, interactive, browser-driven CLI scraper with no network API. Any integration would have to be a subprocess/CLI invocation (e.g. `python main.py --target <user> --output <name> --max-minutes <n>`) on a host with Chrome + a logged-in Instagram session, and would still require human intervention for login challenges -- so it is not a good fit for automated tool-calling. Per CLAUDE.md rules, prefer NOT exposing it.
