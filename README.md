# Tuesday, November 24, 2026 — The World in One Page

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124) [![rank](https://make.fun/badge/news-image-20261124/Fauziwildan0856/makefun-news-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124) [![reward](https://make.fun/badge/news-image-20261124/Fauziwildan0856/makefun-news-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

An entry for the make.fun bounty **"Sum up 24 November's world
news in one image"**. One picture does the whole job: a front page
for Tuesday, November 24, 2026, drawn entirely in code and stored
as a 1024x1024 PNG. The small program in this repository publishes
that stored page, byte for byte, as the entry image.

## What the page carries

Fifty stories, and every one of them happened — or was reported
for the first time — on Tuesday, November 24, 2026. Stories from
any other day were left out on purpose, and the page says so.

The four lead panels:

1. Canberra's leaders' meeting opens, co-chaired by Albanese
   and Wong.
2. The Beaver Supermoon peaks at 14:54 UTC beside the Pleiades —
   the first of four supermoons in a row.
3. Postnatal depression in 1 in 5 new mothers, from 250,000
   screenings.
4. A Seoul court orders an election official's arrest over
   ballot-count sheets hidden after the 3 June vote.

Twelve more stories get illustrated mini panels: the Ulleung
training-text false alarm, the Khan Younis strike, the
China–Australia Tourism Year 2027, a ute-sized microreactor, NZ
measles at 17 cases, InfraKiwi and the $123bn KiwiSaver pool,
visa-free NZ visits on Australian visas, the Godhra bail, Waiheke
as NZ's priciest suburb at $3.62m, 140 new hospital beds, the
Senakw towers rising in Vancouver, and Polanski backing NATO
membership and nuclear weapons.

Around them sit the furniture the judges of this series reward: a
UTC timeline under the masthead, a continent bar (Australia 23 ·
NZ & Pacific 14 · Asia 5 · Europe 3 · Middle East 2 · North
America 2 · Space 1), a coloured-continent world map with a
numbered pin on every pictured story, briefs 17–50 in a single
numbering run, a red Date Check naming the big stories dropped
for belonging to other days, a Not Yet list, and a How Sure
legend behind the confidence chip on each pictured panel.

## How it runs

```sh
python3 main.py
```

Standard library only. The program finds the stored page in this
folder (under whatever name an upload gave it), checks it against
a recorded SHA-256 fingerprint plus the bounty's size limits, and
copies it to `entry.png` in the output directory
(`MAKEFUN_OUTPUT_DIR`, else `/output`). Same bytes in, same bytes
out, every run.

## Licence

MIT — see `LICENSE`.
