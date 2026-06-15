# CLAUDE.md -- InstagramDataScraper

## 1. Project Identity

**Name:** InstagramDataScraper -- Instagram Profile URL Extractor
**Role:** Selenium-based tool to extract Instagram profile URLs from feeds, hashtags, and follower lists with smart filtering and dedup.
**Author:** SoClose Society (https://soclose.co)
**License:** MIT

### Stack

- **Language:** Python 3.10+
- **Browser:** Selenium 4.25+ with webdriver-manager
- **Parsing:** BeautifulSoup4, lxml
- **Config:** python-dotenv
- **Architecture:** Monolithic (single main.py, 240 LOC)

### Critical Files

- `main.py` -- All logic (240 LOC, monolithic)
- `.env` -- Instagram credentials (optional, can enter at runtime)

## 2-5. Standard Workflow

- Enter plan mode for non-trivial tasks
- Test with a small feed before bulk scraping
- Verify excluded paths filter works (no /explore/, /settings/, etc. in output)
- Track tasks in `tasks/todo.md`, lessons in `tasks/lessons.md`

## 6. Project-Specific Rules

### Dev Commands
```bash
pip install -r requirements.txt
cp .env.example .env  # Optional: fill credentials
python main.py        # Interactive mode (prompts for creds + output file)
```

### Environment Variables (optional)
- INSTA_USERNAME -- Instagram login
- INSTA_PASSWORD -- Instagram password

### Config Constants (hardcoded in main.py)
- MAX_STALE_ITERATIONS=500
- SCROLL_PAUSE_MIN=0.8, SCROLL_PAUSE_MAX=2.0
- SCROLL_AMOUNT=600
- SAVE_INTERVAL=50
- EXCLUDED_PATHS -- /explore/, /accounts/, /reels/, /stories/, etc.

### Known Fragile Areas
- Instagram DOM changes break extraction silently
- Login can fail with 2FA or suspicious activity challenges
- Monolithic design -- all 240 lines in one file

## Neo Connector (auto)
Ce projet expose `NEO_CONNECTOR.md` : le manifeste machine-lisible de TOUS ses
endpoints/auth/env, consommé par NeoBot pour se câbler automatiquement.
- RÈGLE : à chaque ajout/suppression/modif d'un endpoint, d'une auth ou d'une env var,
  régénère le manifeste via `/neo-connector` (ou le prompt dans .claude/skills/neo-connector).
- Ne jamais éditer NEO_CONNECTOR.md à la main : il est généré.
- Le hook pre-commit (.git/hooks/pre-commit) avertit si des routes ont changé sans MAJ du manifeste.
- NOTE (ce repo) : pas d'API HTTP -- CLI Selenium pur. Le manifeste documente l'absence de surface réseau ; ce projet ne doit PAS être câblé comme outil HTTP Neo.

## 7. Core Principles

- Simplicity First, No Laziness, Minimal Impact
- Never use em dashes (use -- instead)
- Never remove EXCLUDED_PATHS filter
