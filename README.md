# The World in One Day — Sunday 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/c/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rank.svg)](https://make.fun/c/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/reward.svg)](https://make.fun/c/news-image-20261122)

35 stories from Sunday 22 November 2026 on one front page: 3 leads (COP31's
final text lands at dawn with no mention of fossil fuels, Iran claims strikes
on US bases in Bahrain, 186 drones over Ukraine overnight), 10 pictured
stories, 22 briefs across 7 regions — with a UTC timeline, a 6-number strip,
a world map with numbered pins, per-story confidence tags and sources, and a
DATE CHECK footer naming what was left out on purpose (including the
correction that tonight's barrage was 186 drones, not 400).

Built for the [make.fun](https://make.fun) bounty "Sum up 22 November's world
news in one image".

## How it works

`main.py` is a self-contained, stdlib-only generator: it draws the whole page
with a hand-typed 5x7 bitmap font and a pure-Python PNG encoder. No external
files, no network, deterministic. Run `python3 main.py` and it writes
`entry.png` (1024x1024) to `$MAKEFUN_OUTPUT_DIR` (default `/output`).
