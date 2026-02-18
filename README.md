# Instagram Profile Scraper

> **Collect Instagram profile URLs at scale — automated scrolling, smart filtering, clean CSV export.**
> Open-source tool by **[SoClose Society](https://soclose.co)** — Digital solutions & software development studio.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green.svg)](https://selenium.dev)
[![SoClose Society](https://img.shields.io/badge/SoClose-Society-purple.svg)](https://soclose.co)

---

## Why This Tool?

Need to build a prospect list, analyze followers, or study engagement patterns? Manually copying Instagram profiles is slow and tedious. This scraper automates the entire process — login, scroll, extract, deduplicate, export — in one command.

**Built for:**
- Growth hackers & digital marketers building lead lists
- Data analysts studying social media patterns
- Researchers collecting public profile datasets
- Developers learning Selenium browser automation

---

## Features

| Feature | Description |
|---|---|
| **One-command setup** | Clone, install, run — scraping in under 2 minutes |
| **Smart login** | Automated Instagram authentication via Selenium |
| **Infinite scroll** | Continuous feed scrolling with auto-stop detection |
| **Profile filtering** | Extracts only profile URLs, skips /explore/, /reels/, /settings/ etc. |
| **Deduplication** | Built-in `set()` ensures zero duplicate profiles |
| **Human-like delays** | Randomized scroll timing (0.8s–2.0s) to mimic real behavior |
| **Auto-save** | Progress saved every 50 iterations — never lose data |
| **Graceful stop** | Press `Ctrl+C` anytime — all collected data is saved |
| **Secure credentials** | `.env` file support — credentials never in code |
| **Clean CSV output** | Full Instagram URLs, sorted alphabetically, UTF-8 encoded |
| **Detailed logging** | Real-time progress with iteration count and stale detection |

---

## Quick Start

### Prerequisites

- **Python 3.10+** — [Download](https://python.org/downloads/)
- **Google Chrome** — Latest stable version
- **Git** — [Download](https://git-scm.com/)

### Install

```bash
git clone https://github.com/soclosesociety/InstagramDataScraper.git
cd InstagramDataScraper
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
```

Edit `.env`:

```env
INSTA_USERNAME=your_username_or_email
INSTA_PASSWORD=your_password
```

> Skip the `.env` file to enter credentials at runtime instead.

### Run

```bash
python main.py
```

**What happens:**
1. Chrome opens and logs in to Instagram
2. You navigate to the page you want to scrape (feed, hashtag, explore...)
3. Press **ENTER** to start
4. The scraper scrolls and collects profile links automatically
5. Results are saved to a `.csv` file

Press **Ctrl+C** at any time to stop and save.

---

## Output Format

```csv
ProfileLink
https://www.instagram.com/alice/
https://www.instagram.com/bob/
https://www.instagram.com/charlie/
```

---

## How It Works

```
┌──────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌───────────┐
│ Chrome opens │───>│ Login to     │───>│ Scroll & extract │───>│ Export to │
│ via Selenium │    │ Instagram    │    │ profile links    │    │ CSV file  │
└──────────────┘    └──────────────┘    └─────────────────┘    └───────────┘
                                               │
                                        ┌──────┴──────┐
                                        │ Deduplicate │
                                        │ + filter    │
                                        └─────────────┘
```

1. **Selenium** opens Chrome and handles authentication
2. **BeautifulSoup** parses the page HTML and extracts `<a>` tags
3. Profile URLs are filtered (only `/username/` patterns, no `/explore/` etc.)
4. A `set` ensures each profile appears only once
5. Randomized delays between scrolls avoid detection
6. Auto-stops after 500 stale iterations (no new profiles found)

---

## Configuration

Edit the constants at the top of [main.py](main.py):

| Variable | Default | Description |
|---|---|---|
| `MAX_STALE_ITERATIONS` | 500 | Stop after N iterations with no new links |
| `SCROLL_PAUSE_MIN` | 0.8s | Minimum delay between scrolls |
| `SCROLL_PAUSE_MAX` | 2.0s | Maximum delay between scrolls |
| `SCROLL_AMOUNT` | 600 | Pixels to scroll down per iteration |
| `SAVE_INTERVAL` | 50 | Save to CSV every N iterations |

---

## Project Structure

```
InstagramDataScraper/
├── main.py              # Core scraper script
├── requirements.txt     # Python dependencies
├── .env.example         # Credential template
├── .gitignore           # Git ignore rules
├── CONTRIBUTING.md      # Contribution guidelines
├── LICENSE              # MIT License
├── pyproject.toml       # Python project metadata
└── README.md            # Documentation
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| [Python 3.10+](https://python.org) | Core language |
| [Selenium 4.x](https://selenium.dev) | Browser automation |
| [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io) | HTML parsing |
| [lxml](https://lxml.de) | Fast HTML parser backend |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |
| [webdriver-manager](https://pypi.org/project/webdriver-manager/) | Automatic ChromeDriver setup |

---

## More Open-Source Tools by SoClose Society

We build and share automation tools for the community. Explore our other projects:

| Project | Description | Stars |
|---|---|---|
| [PinterestBulkPostBot](https://github.com/soclosesociety/PinterestBulkPostBot) | Automated Pinterest posting tool | 11 |
| [LinkedinDataScraper](https://github.com/soclosesociety/LinkedinDataScraper) | LinkedIn contact data extraction | 2 |
| [BOT_GoogleMap_Scrapping](https://github.com/soclosesociety/BOT_GoogleMap_Scrapping) | Google Maps data scraper | 3 |
| [BOT-Facebook_Bulk_Invite](https://github.com/soclosesociety/BOT-Facebook_Bulk_Invite_Friend_To_FB_Group) | Facebook group invitation automation | 4 |
| [FreeWorkDataScraper](https://github.com/soclosesociety/FreeWorkDataScraper) | Freelance job posting scraper | 1 |

**[View all 15+ repositories](https://github.com/soclosesociety)**

---

## Disclaimer

> This tool is provided **for educational and research purposes only**.
> Scraping Instagram may violate their [Terms of Service](https://help.instagram.com/581066165581870).
> The authors are not responsible for any misuse or consequences resulting from the use of this tool.
> Always respect platform policies and applicable laws in your jurisdiction.

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## About SoClose Society

**[SoClose Society](https://soclose.co)** is a digital solutions & software development studio. We build open-source automation tools and share them with the developer community.

- **Website:** [soclose.co](https://soclose.co)
- **GitHub:** [github.com/soclosesociety](https://github.com/soclosesociety)
- **Contact:** [contact@soclose.co](mailto:contact@soclose.co)
- **LinkedIn:** [SoClose Agency](https://linkedin.com/company/soclose-agency)
- **Twitter/X:** [@SoCloseAgency](https://twitter.com/SoCloseAgency)

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong><a href="https://soclose.co">SoClose Society</a></strong><br/>
  Digital solutions & software development studio<br/><br/>
  <a href="https://github.com/soclosesociety/InstagramDataScraper">Star this repo</a> if you find it useful!
</p>
