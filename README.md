# The World in One Page — Tuesday, November 24, 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124) [![rank](https://make.fun/badge/news-image-20261124/Fauziwildan0856/makefun-news-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124) [![reward](https://make.fun/badge/news-image-20261124/Fauziwildan0856/makefun-news-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

This repository is an entry for the make.fun bounty **"Sum up 24
November's world news in one image"**. The entry is one picture: a
newspaper front page for Tuesday, November 24, 2026, drawn in code
as a single 1024x1024 PNG. The program here publishes that stored
picture, unchanged, as the entry image.

## The page

- **50 stories**, each one happened or was first reported on
  Tuesday, November 24, 2026 — nothing from another day.
- **4 illustrated lead panels**: the Canberra leaders' meeting
  opening under Albanese and Wong; the Beaver Supermoon peaking at
  14:54 UTC beside the Pleiades; postnatal depression found in
  1 in 5 new mothers across 250,000 screenings; the Seoul court
  arrest warrant for an election official over hidden ballot
  sheets.
- **12 illustrated mini panels**: the Ulleung false alarm that was
  a training text; the Khan Younis strike; the China–Australia
  Tourism Year 2027; a ute-sized microreactor pitch; measles at 17
  cases as immunisation week opens; InfraKiwi's $123bn channel;
  visa-free NZ visits on Australian visas; the Godhra bail ruling;
  Waiheke at a $3.62m average; 140 new hospital beds; Senakw's
  6,000 Vancouver homes; Polanski backing the NATO report.
- A **UTC timeline** under the masthead, a **continent stat bar**
  (Australia 23 · NZ & Pacific 14 · Asia 5 · Europe 3 · Middle
  East 2 · North America 2 · Space 1), a **world map with coloured
  continents** and numbered pins for the 16 pictured stories,
  **34 more stories** as briefs 17–50, a red **Date Check** listing
  the other days' stories left out on purpose plus a **Not Yet**
  list, and a **How Sure** legend for the confidence chip on every
  pictured panel.
- Every illustration and the map are original, drawn in code.

## Running it

```sh
python3 main.py
```

That publishes the picture to `entry.png` in the output directory
(`MAKEFUN_OUTPUT_DIR`, else `/output`). It needs nothing beyond the
Python 3 standard library: it finds the stored picture in this
repository (under whichever name the upload gave it), checks it
against a recorded SHA-256 fingerprint and a PNG size check, then
copies it byte-for-byte. The picture comes out identical on every
run.

## Licence

Released under the MIT licence; the full text is in `LICENSE`.
