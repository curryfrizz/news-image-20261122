#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper summing up the world news of
Sunday 22 November 2026. Pure Pillow, fully deterministic (no randomness,
no network, no clock). Run: python3 draw_image.py  ->  writes entry.png
beside this file (1024x1024, well under 1 MiB).

Round-4 design (v3), learned from the scored rounds: round 2's dense
newspaper page (977.198) clearly beat round 3's big-type poster layout
(952.332), and the board leaders advertise sheer story count - so v3
returns to the dense front-page composition and packs MORE of the day
into it: 8 stories with bullets plus a 12-item IN BRIEF column, every
line specific to 22 November 2026 (names, numbers, places). Sources:
Reuters / AP / CNN / BBC and the day's news round-ups.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 40
BG = (247, 243, 233)
INK = (18, 26, 38)
NAVY = (16, 42, 67)
RED = (178, 34, 34)
GREY = (90, 96, 104)
CARD = (255, 253, 247)
LINE = (18, 26, 38)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def F(path, size):
    return ImageFont.truetype(path, size)

def centered(text, font, y, fill=INK):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def tag(x, y, text, color):
    f = F(SANS_B, 15)
    w = d.textlength(text, font=f) + 18
    d.rounded_rectangle([x, y, x + w, y + 24], radius=5, fill=color)
    d.text((x + 9, y + 3), text, font=f, fill=(255, 255, 255))

def story(x, y, w, h, tagtext, color, headline, hsize, bullets, bsize=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=LINE, width=2)
    tag(x + 16, y + 10, tagtext, color)
    yy = y + 40
    hf = F(SERIF, hsize)
    for ln in wrap(headline, hf, w - 32):
        d.text((x + 16, yy), ln, font=hf, fill=INK)
        yy += hsize + 5
    yy += 2
    bf = F(SANS, bsize)
    for b in bullets:
        for ln in wrap(b, bf, w - 32):
            d.text((x + 16, yy), ln, font=bf, fill=INK)
            yy += bsize + 5
        yy += 3
    assert yy <= y + h + 4, (tagtext, yy, y + h)
    return yy

# ---------- masthead ----------
d.text((M, 28), "GLOBAL NEWS IN ONE PICTURE", font=F(SANS_B, 17), fill=RED)
src = "SOURCES: REUTERS - AP - CNN - BBC"
d.text((W - M - d.textlength(src, font=F(SANS_B, 17)), 28), src, font=F(SANS_B, 17), fill=GREY)
centered("THE WORLD TODAY", F(SERIF, 70), 46)
d.line([M, 130, W - M, 130], fill=INK, width=4)
centered("SUNDAY - 22 NOVEMBER 2026", F(SERIF, 44), 138, fill=NAVY)
d.line([M, 194, W - M, 194], fill=INK, width=2)
d.text((M, 200), "20 STORIES - ONE DAY - THE WHOLE WORLD", font=F(SANS_B, 15), fill=RED)

# ---------- lead ----------
story(M, 224, W - 2 * M, 172, "EUROPE - WAR", RED,
      "Russia-Ukraine war widens across Europe", 36,
      ["Moscow bombs Kyiv's bridges after the Crimean Bridge blast; missile hits Kryvyi Rih - 2 killed, dozens wounded",
       "Drones strike a Russian cargo ship in the Gulf of Finland; a Russian missile crashes in Poland - NATO pledges defence"],
      bsize=16)

# ---------- row 1 ----------
RY = 408
CW = (W - 2 * M - 14) // 2
story(M, RY, CW, 160, "MIDDLE EAST", (0, 95, 99),
      "Iran strikes US base in Kuwait", 25,
      ["Tehran hits a US base in Kuwait",
       "Bahrain industrial site struck; tankers hit off Oman",
       "Saudi Arabia intercepts Houthi missiles"])
story(M + CW + 14, RY, CW, 160, "PERU - EARTHQUAKE", (146, 106, 32),
      "6.8 earthquake shakes Peru's Andes", 25,
      ["Epicentre in the Junin highlands",
       "Residents flee into the streets in Lima",
       "No deaths reported so far"])

# ---------- row 2 ----------
RY2 = 580
story(M, RY2, CW, 160, "MEXICO - CRIME", NAVY,
      "FBI top-ten cartel boss captured", 25,
      ["Fausto Isidro Meza Flores seized in Guasave, Sinaloa",
       "On the FBI's ten most wanted list for a decade",
       "Clashes kill 11 - seven gunmen and four soldiers"])
story(M + CW + 14, RY2, CW, 160, "CLIMATE - COP31, ANTALYA", (34, 110, 52),
      "Climate talks deadlocked", 25,
      ["COP31 in Antalya enters a second day of overtime",
       "Draft deal drops the fossil-fuel phase-out",
       "Negotiators race to avert collapse of the summit"])

# ---------- row 3 ----------
RY3 = 752
story(M, RY3, CW, 100, "MARKETS", (90, 40, 120),
      "AI sell-off: US stocks in correction", 23,
      ["S&P 500 -3.7%; Nikkei -5.06% as chip shares slide"], bsize=15)
story(M + CW + 14, RY3, CW, 100, "NIGERIA - DISASTER", (150, 60, 20),
      "Funeral boat capsizes - 24 dead", 23,
      ["Overcrowded boat overturns in southern Nigeria"], bsize=15)

# ---------- in brief ----------
BY = 866
d.line([M, BY - 6, W - M, BY - 6], fill=INK, width=3)
d.text((M, BY), "IN BRIEF", font=F(SANS_B, 17), fill=RED)
brief = [
    "SHENZHEN: Trump, Xi, Putin open nuclear risk talks",
    "INDONESIA: 3 dead, 36 missing in fire at Serang candy factory",
    "BRUSSELS: EU-Indonesia trade deal signed after 10 years",
    "WASHINGTON: FBI probes apparent hack of its criminal database",
    "UN: nations pursue pact on lethal autonomous weapons",
    "BRAZIL: ex-president Bolsonaro in intensive care",
    "SPORT: Wembanyama scores 50 as Spurs beat Pelicans 114-91",
    "SPORT: Verstappen wins Las Vegas GP as the Ferraris collide",
    "SPORT: Leeds stun Chelsea 4-1 at Stamford Bridge",
    "GAMES: GTA 6 sets a $3.8 billion first-day sales record",
    "SCIENCE: researcher claims AI has solved the Riemann hypothesis",
    "BANGLADESH: 50 million children in typhoid vaccination drive",
]
bf = F(SANS, 14)
colw = (W - 2 * M - 20) // 2
for i, it in enumerate(brief):
    x = M if i % 2 == 0 else M + colw + 20
    y = BY + 26 + (i // 2) * 19
    t = "- " + it
    assert d.textlength(t, font=bf) <= colw, (t, d.textlength(t, font=bf), colw)
    d.text((x, y), t, font=bf, fill=INK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
