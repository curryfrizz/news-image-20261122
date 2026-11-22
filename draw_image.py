#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper summing up the world news of
Sunday 22 November 2026. Pure Pillow, fully deterministic (no randomness,
no network, no clock). Run: python3 draw_image.py  ->  writes entry.png
beside this file (1024x1024, well under 1 MiB).

Round-3 design: the date and the headlines stay legible at ~300px, the
specific names, numbers and places sit inside the big type, five hero
stories plus a compact 'MORE OF THE DAY' breadth strip, no decorative
icons. Stories (all reported on 22 Nov 2026 round-ups; Reuters / AP /
CNN / BBC): Russia-Ukraine war widens (Kyiv bridges bombed after the
Crimean Bridge blast, drones hit a Russian cargo ship in the Gulf of
Finland, a Russian missile crashes in Poland, NATO pledges defence);
Iran strikes a US base in Kuwait and targets Bahrain, tankers hit off
Oman, Saudi Arabia intercepts Houthi missiles; magnitude 6.8 earthquake
in Peru's Junin highlands, Lima residents flee, no deaths reported;
FBI top-ten cartel boss 'El Chapo Isidro' captured in Sinaloa, clashes
kill 11; COP31 climate talks deadlocked over the fossil-fuel phase-out;
plus UN autonomous-weapons pact, Bolsonaro in intensive care, AI cracks
a 167-year-old maths problem, Estonia to shut its border with Russia.
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
    f = F(SANS_B, 19)
    w = d.textlength(text, font=f) + 24
    d.rounded_rectangle([x, y, x + w, y + 30], radius=6, fill=color)
    d.text((x + 12, y + 4), text, font=f, fill=(255, 255, 255))

def card(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD, outline=LINE, width=2)

def bullets(x, y, text, size, maxw, lh=None):
    f = F(SANS, size)
    lh = lh or (size + 7)
    for ln in wrap(text, f, maxw):
        d.text((x, y), ln, font=f, fill=INK)
        y += lh
    return y

# ---------- masthead ----------
d.line([M, 26, W - M, 26], fill=INK, width=4)
d.text((M, 38), "GLOBAL NEWS IN ONE PICTURE", font=F(SANS_B, 18), fill=RED)
src = "SOURCES: REUTERS - AP - CNN - BBC"
d.text((W - M - d.textlength(src, font=F(SANS_B, 18)), 38), src, font=F(SANS_B, 18), fill=GREY)
centered("THE WORLD TODAY", F(SERIF, 88), 58)
d.line([M, 162, W - M, 162], fill=INK, width=2)
d.line([M, 168, W - M, 168], fill=INK, width=4)

# ---------- date band ----------
d.rounded_rectangle([M, 182, W - M, 258], radius=12, fill=NAVY)
centered("SUNDAY - 22 NOVEMBER 2026", F(SERIF, 54), 193, fill=(255, 255, 255))

# ---------- lead story ----------
LY = 272
card(M, LY, W - 2 * M, 234)
tag(M + 24, LY + 18, "EUROPE - WAR", RED)
d.text((M + 24, LY + 56), "Russia-Ukraine war widens:", font=F(SERIF, 49), fill=INK)
d.text((M + 24, LY + 110), "missile crashes in Poland", font=F(SERIF, 49), fill=INK)
bullets(M + 24, LY + 172,
        "Moscow bombs Kyiv's bridges after the Crimean Bridge blast - drones hit a Russian cargo ship in the Gulf of Finland - NATO pledges defence",
        size=22, maxw=W - 2 * M - 48)

# ---------- row 1 ----------
RY = 520
CW = (W - 2 * M - 16) // 2
card(M, RY, CW, 200)
tag(M + 20, RY + 15, "MIDDLE EAST", (0, 95, 99))
d.text((M + 20, RY + 52), "Iran strikes US base", font=F(SERIF, 36), fill=INK)
d.text((M + 20, RY + 92), "in Kuwait", font=F(SERIF, 36), fill=INK)
bullets(M + 20, RY + 140, "Tehran targets Bahrain - tankers hit off Oman - Saudi Arabia intercepts Houthi missiles",
        size=20, maxw=CW - 40)

X2 = M + CW + 16
card(X2, RY, CW, 200)
tag(X2 + 20, RY + 15, "PERU - EARTHQUAKE", (146, 106, 32))
d.text((X2 + 20, RY + 52), "6.8 quake shakes", font=F(SERIF, 36), fill=INK)
d.text((X2 + 20, RY + 92), "Peru's Andes", font=F(SERIF, 36), fill=INK)
bullets(X2 + 20, RY + 140, "Epicentre in the Junin highlands - Lima residents flee - no deaths reported",
        size=20, maxw=CW - 40)

# ---------- row 2 ----------
RY2 = 734
card(M, RY2, CW, 118)
tag(M + 20, RY2 + 12, "MEXICO - CRIME", NAVY)
d.text((M + 20, RY2 + 46), "FBI top-ten cartel boss", font=F(SERIF, 31), fill=INK)
d.text((M + 20, RY2 + 80), "'El Chapo Isidro' captured", font=F(SERIF, 31), fill=INK)

card(X2, RY2, CW, 118)
tag(X2 + 20, RY2 + 12, "CLIMATE - COP31", (34, 110, 52))
d.text((X2 + 20, RY2 + 46), "Climate talks deadlocked", font=F(SERIF, 31), fill=INK)
d.text((X2 + 20, RY2 + 80), "over fossil-fuel phase-out", font=F(SERIF, 31), fill=INK)

# ---------- breadth strip ----------
SY = 868
d.line([M, SY, W - M, SY], fill=INK, width=3)
d.text((M, SY + 10), "MORE OF THE DAY", font=F(SANS_B, 20), fill=RED)
f = F(SANS, 20)
items = [
    "UN: nations pursue pact on autonomous weapons",
    "Brazil: Bolsonaro in intensive care",
    "AI cracks a 167-year-old maths problem",
    "Estonia to shut its border with Russia",
    "Sinaloa clashes kill 11 in cartel raid",
    "COP31: push to rescue climate agreement",
]
colw = (W - 2 * M - 24) // 2
for i, it in enumerate(items):
    x = M if i % 2 == 0 else M + colw + 24
    y = SY + 44 + (i // 2) * 33
    t = "- " + it
    assert d.textlength(t, font=f) <= colw, (t, d.textlength(t, font=f), colw)
    d.text((x, y), t, font=f, fill=INK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
