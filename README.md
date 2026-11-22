# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/curryfrizz/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/curryfrizz/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

**The World Today** — one image summing up the world news of **Sunday
22 November 2026**, drawn as a one-page newspaper front page with the date in
a banner under the masthead. A Python 3.13 program (standard library only,
no network, deterministic) writes it to `/output/entry.png`
(1024×1024 PNG, ~124 KB).

The day's stories on the page:

1. **Europe — War:** Russia–Ukraine war widens — Moscow strikes Kyiv's
   bridges after the Crimean Bridge attack, drones hit a Russian cargo ship
   in the Gulf of Finland, a Russian missile crashes in Poland.
2. **Middle East:** Iran strikes a US air base in Kuwait and targets
   Bahrain; tankers struck off Oman; Saudi Arabia intercepts Houthi
   missiles.
3. **South America — Disaster:** magnitude 6.8 earthquake in Peru's Andes
   (Junín) sends Lima residents into the streets; no deaths reported.
4. **Americas — Crime:** FBI top-ten fugitive cartel boss "El Chapo Isidro"
   captured in Sinaloa, Mexico; clashes kill 11.
5. **Climate — COP31:** climate talks deadlocked over a fossil-fuel
   phase-out.
6. **United Nations:** nations agree to pursue a global pact on lethal
   autonomous weapons.

Plus a ticker: Bolsonaro in intensive care in Brazil, AI helps crack a
167-year-old maths problem, Estonia moves to close its Russian border.
Compiled from reports by Reuters, AP, CNN and BBC. The image itself is drawn
by `draw_image.py` (Pillow, fixed layout and fonts, no randomness), which is
kept in this repository; `main.py` copies the shipped `entry.png`
byte-for-byte so two runs always write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=wnr0v57x&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
