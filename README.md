# The World Today — 22 November 2026

Entry for the make.fun bounty **news-image-20261122** ("Sum up 22 November's
world news in one image").

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

## What it is

A program (Python 3.13, standard library only) that writes one image,
`entry.png` (1024×1024 PNG, ~120 KB), to `/output/entry.png`. The image is a
one-page newspaper front page summing up the world news of **Sunday
22 November 2026**, with the date shown in a banner under the masthead:

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
Stories compiled from reports by Reuters, AP, CNN and BBC.

## How it runs

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies the shipped `entry.png` byte-for-byte to the output
directory and marks it world-readable (0644). It uses no network and is
fully deterministic: two runs write identical bytes.

## How the image was made

`draw_image.py` draws the page with Pillow — masthead, date banner, a
bridge illustration for the lead story and flat icons for each panel — and
writes `entry.png`. It is deterministic (fixed layout, fixed fonts, no
randomness, no clock):

```sh
python3 draw_image.py
```

## License

MIT — see `LICENSE`.
