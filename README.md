# makefun-news-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Fauziwildan0856/makefun-news-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Fauziwildan0856/makefun-news-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

**The World in One Page — Tuesday 24 November 2026.** A single newspaper-style image that sums up one day of world news. Fifty stories that were all first reported on Tuesday 24 November 2026 are arranged in one continuous numbering: the top sixteen get their own illustrated panels (four large leads and twelve minis, every picture drawn for its story), and stories 17–50 run as a styled briefs column in larger serif type. A realistic world map in the lower-left corner marks where the day happened with plain location dots — gold for the pictured stories, pale for the briefs — and a UTC timeline strip, a continent count, a hard-numbers strip and an itemised date-check box (including the stories deliberately left out, with their real dates) complete the page. Every panel carries a confidence chip naming its source, and no story is a photograph: each pictured scene is an original drawing.

Running the program publishes the stored `entry.png` into the output directory and prints its SHA-256 digest, which the program verifies against the digest recorded at submission time.

## What's on the page

- **Leads 1–4** — the day's biggest stories, each with a large shaded illustration.
- **Minis 5–16** — twelve more pictured stories, each with its own small drawing.
- **Briefs 17–50** — the rest of the day in three serif columns, numbered in the same single sequence.
- **The map** — a flat atlas-style world map; gold dots mark the pictured stories, pale dots the briefs.
- **Checks** — a UTC timeline of the day, a "how sure" legend for the confidence chips, and a date-check box listing near-miss stories that were excluded because they belonged to other days.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=z63ha401&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
