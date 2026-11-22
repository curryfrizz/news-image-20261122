#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper summing up the world news of
Sunday 22 November 2026. Pure Pillow, fully deterministic (no randomness,
no network, no clock). Run: python3 draw_image.py  ->  writes entry.png
beside this file (1024x1024, well under 1 MiB).

Stories (all reported on 22 Nov 2026 round-ups; Reuters / AP / CNN / BBC):
 1. Russia strikes Kyiv's bridges after the Crimean Bridge attack; drones
    hit a Russian cargo ship in the Gulf of Finland; a Russian missile
    crashes in Poland and NATO vows to defend all allied territory.
 2. Iran strikes a US air base in Kuwait and targets Bahrain; tankers are
    hit off Oman as Gulf naval tensions escalate.
 3. A magnitude 6.8 earthquake in Peru's Andes (Junin) sends Lima residents
    into the streets; no deaths or major damage reported at first.
 4. Mexico captures FBI top-ten fugitive cartel boss 'El Chapo Isidro'
    (Fausto Isidro Meza Flores) in Guasave, Sinaloa; clashes kill 11.
 5. COP31 climate talks deadlocked over fossil fuels; the draft deal is
    attacked for ignoring a phase-out and talks push on.
 6. At UN talks, nations agree to pursue an international pact on lethal
    autonomous weapons.
Ticker: Bolsonaro in intensive care in Brazil; AI helps crack a
167-year-old maths problem; Estonia moves to close its Russian border.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 36  # page margin

PAPER = (247, 242, 231)
CARD = (255, 253, 247)
INK = (20, 32, 46)
NAVY = (18, 40, 63)
RED = (178, 34, 40)
GREY = (96, 104, 112)
LINE = (20, 32, 46)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def centered(text, font, y, fill=INK):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return w


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
    w = d.textlength(text, font=f) + 20
    d.rounded_rectangle([x, y, x + w, y + 26], 6, fill=color)
    d.text((x + 10, y + 4), text, font=f, fill=(255, 255, 255))
    return w


def panel(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], 10, fill=CARD, outline=LINE, width=2)


def body(x, y, w, lines, size=20, lh=27, fill=INK):
    f = F(SANS, size)
    for ln in lines:
        for sub in wrap(ln, f, w):
            d.text((x, y), sub, font=f, fill=fill)
            y += lh
    return y


# ---------------------------------------------------------------- masthead
d.line([M, 26, W - M, 26], fill=LINE, width=3)
f_eye = F(SANS_B, 16)
d.text((M, 36), "GLOBAL NEWS IN ONE PICTURE", font=f_eye, fill=RED)
src = "SOURCES: REUTERS - AP - CNN - BBC"
d.text((W - M - d.textlength(src, font=f_eye), 36), src, font=f_eye, fill=GREY)
centered("THE WORLD TODAY", F(SERIF, 76), 58)
d.line([M, 148, W - M, 148], fill=LINE, width=2)
d.line([M, 153, W - M, 153], fill=LINE, width=1)

# ---------------------------------------------------------------- date band
d.rounded_rectangle([M, 164, W - M, 230], 10, fill=NAVY)
centered("SUNDAY - 22 NOVEMBER 2026", F(SERIF, 41), 176, fill=(255, 255, 255))
for cx in (M + 26, W - M - 26):
    d.ellipse([cx - 7, 190, cx + 7, 204], fill=RED)

# ---------------------------------------------------------------- lead story
LX, LY, LW, LH = M, 246, W - 2 * M, 252
panel(LX, LY, LW, LH)
# illustration: bridge over a river, burst, drone (left 300 px)
IX, IY, IW, IH = LX + 14, LY + 14, 292, LH - 28
d.rounded_rectangle([IX, IY, IX + IW, IY + IH], 8, fill=(203, 226, 240))
for i, c in enumerate([(214, 233, 245), (224, 238, 248)]):  # sky bands
    d.rectangle([IX, IY + i * 30, IX + IW, IY + (i + 1) * 30], fill=c)
d.rectangle([IX, IY + IH - 52, IX + IW, IY + IH], fill=(64, 116, 168))  # river
for yy in (IY + IH - 38, IY + IH - 20):  # water lines
    for xx in range(IX + 12, IX + IW - 30, 52):
        d.line([xx, yy, xx + 26, yy], fill=(168, 205, 232), width=3)
deck_y = IY + IH - 62
d.rectangle([IX + 8, deck_y, IX + IW - 8, deck_y + 9], fill=(52, 62, 74))  # deck
for tx in (IX + 52, IX + IW - 66):  # towers
    d.rectangle([tx, deck_y - 74, tx + 12, deck_y], fill=(52, 62, 74))
for tx in (IX + 58, IX + IW - 60):  # cables
    d.line([tx, deck_y - 74, IX + 30, deck_y], fill=(52, 62, 74), width=2)
    d.line([tx, deck_y - 74, IX + IW - 30, deck_y], fill=(52, 62, 74), width=2)
cx, cy = IX + IW - 62, deck_y - 6  # burst at the far end of the bridge
for ang in range(0, 360, 30):
    import math
    x2 = cx + 30 * math.cos(math.radians(ang))
    y2 = cy + 30 * math.sin(math.radians(ang))
    d.line([cx, cy, x2, y2], fill=(232, 119, 34), width=4)
d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=RED)
dx, dy = IX + 52, IY + 34  # quadcopter drone silhouette
d.line([dx - 20, dy - 12, dx + 20, dy + 12], fill=INK, width=4)
d.line([dx - 20, dy + 12, dx + 20, dy - 12], fill=INK, width=4)
for (rx, ry) in [(dx - 22, dy - 14), (dx + 22, dy - 14), (dx - 22, dy + 14), (dx + 22, dy + 14)]:
    d.ellipse([rx - 7, ry - 3, rx + 7, ry + 3], fill=INK)
d.ellipse([dx - 8, dy - 6, dx + 8, dy + 6], fill=INK)

TX = LX + IW + 40
TW = LX + LW - TX - 18
tag(TX, LY + 18, "EUROPE - WAR", RED)
d.text((TX, LY + 56), "Russia-Ukraine war", font=F(SERIF, 42), fill=INK)
d.text((TX, LY + 104), "widens across Europe", font=F(SERIF, 42), fill=INK)
body(TX, LY + 162, TW, [
    "- Moscow hits Kyiv's bridges after Crimean Bridge attack",
    "- Drones hit a Russian cargo ship in the Gulf of Finland",
    "- Russian missile crashes in Poland; NATO pledges defence",
], size=20, lh=28)

# ---------------------------------------------------------------- row of two
RY, RH = 514, 196
PW = (W - 2 * M - 16) // 2

def icon_gulf(x, y):
    d.rounded_rectangle([x, y, x + 76, y + 76], 10, fill=(16, 92, 102))
    d.polygon([(x + 16, y + 52), (x + 60, y + 52), (x + 52, y + 64), (x + 24, y + 64)], fill=(255, 255, 255))
    d.rectangle([x + 30, y + 40, x + 46, y + 52], fill=(255, 255, 255))
    d.polygon([(x + 48, y + 12), (x + 62, y + 26), (x + 40, y + 30)], fill=(255, 214, 120))
    d.polygon([(x + 44, y + 26), (x + 34, y + 38), (x + 50, y + 36)], fill=(232, 119, 34))

def icon_quake(x, y):
    d.rounded_rectangle([x, y, x + 76, y + 76], 10, fill=(146, 96, 24))
    d.polygon([(x + 6, y + 56), (x + 28, y + 22), (x + 44, y + 56)], fill=(255, 255, 255))
    d.polygon([(x + 30, y + 56), (x + 50, y + 28), (x + 68, y + 56)], fill=(226, 214, 190))
    pts = [(x + 6, y + 68), (x + 22, y + 68), (x + 28, y + 60), (x + 36, y + 72),
           (x + 44, y + 62), (x + 50, y + 68), (x + 70, y + 68)]
    d.line(pts, fill=(255, 235, 190), width=3)

def story(x, y, w, h, tag_text, color, icon, head, lines):
    panel(x, y, w, h)
    icon(x + 14, y + 14)
    tag(x + 104, y + 16, tag_text, color)
    d.text((x + 104, y + 48), head, font=F(SERIF, 26), fill=INK)
    body(x + 16, y + 102, w - 32, lines, size=19, lh=26)

story(M, RY, PW, RH, "MIDDLE EAST", (16, 92, 102), icon_gulf,
      "Iran strikes widen Gulf conflict",
      ["- Iran hits US base in Kuwait, targets Bahrain",
       "- Tankers struck off Oman amid naval tension",
       "- Saudi Arabia intercepts Houthi missiles"])
story(M + PW + 16, RY, PW, RH, "SOUTH AMERICA - DISASTER", (146, 96, 24), icon_quake,
      "6.8 quake shakes Peru's Andes",
      ["- Lima residents rush into the streets",
       "- No deaths or major damage reported yet",
       "- Epicentre deep in the Junin highlands"])

# ---------------------------------------------------------------- row of two
RY2, RH2 = 726, 158

def icon_cuffs(x, y):
    d.rounded_rectangle([x, y, x + 76, y + 76], 10, fill=NAVY)
    d.ellipse([x + 12, y + 26, x + 40, y + 54], outline=(255, 255, 255), width=5)
    d.ellipse([x + 36, y + 26, x + 64, y + 54], outline=(255, 255, 255), width=5)
    d.line([x + 33, y + 24, x + 43, y + 24], fill=(255, 214, 120), width=5)
    d.polygon([(x + 38, y + 8), (x + 42, y + 16), (x + 50, y + 17), (x + 44, y + 22),
               (x + 46, y + 30), (x + 38, y + 25), (x + 30, y + 30), (x + 32, y + 22),
               (x + 26, y + 17), (x + 34, y + 16)], fill=(255, 214, 120))

def icon_climate(x, y):
    d.rounded_rectangle([x, y, x + 76, y + 76], 10, fill=(38, 102, 62))
    d.rectangle([x + 12, y + 44, x + 44, y + 64], fill=(255, 255, 255))
    d.rectangle([x + 18, y + 28, x + 26, y + 44], fill=(255, 255, 255))
    d.rectangle([x + 32, y + 24, x + 40, y + 44], fill=(255, 255, 255))
    for (ex, ey, r) in [(22, 18, 6), (36, 12, 7), (50, 18, 5)]:
        d.ellipse([x + ex - r, y + ey - r, x + ex + r, y + ey + r], fill=(206, 226, 210))
    d.ellipse([x + 52, y + 40, x + 66, y + 66], outline=(255, 214, 120), width=4)
    d.line([x + 59, y + 58, x + 59, y + 46], fill=RED, width=4)

story(M, RY2, PW, RH2, "AMERICAS - CRIME", NAVY, icon_cuffs,
      "Cartel kingpin captured",
      ["- FBI top-ten fugitive 'El Chapo Isidro'",
       "- seized in Sinaloa; clashes kill 11"])
story(M + PW + 16, RY2, PW, RH2, "CLIMATE - COP31", (38, 102, 62), icon_climate,
      "Climate talks deadlocked",
      ["- Draft deal ignores fossil-fuel phase-out",
       "- Negotiators push on to rescue agreement"])

# ---------------------------------------------------------------- UN strip
UY = 900
panel(M, UY, W - 2 * M, 56)
d.rounded_rectangle([M + 12, UY + 10, M + 48, UY + 46], 8, fill=(84, 96, 120))
d.rectangle([M + 22, UY + 20, M + 38, UY + 34], outline=(255, 255, 255), width=3)
d.line([M + 30, UY + 20, M + 30, UY + 14], fill=(255, 255, 255), width=3)
d.ellipse([M + 27, UY + 10, M + 33, UY + 16], fill=(255, 214, 120))
d.ellipse([M + 25, UY + 25, M + 29, UY + 29], fill=(255, 214, 120))
d.ellipse([M + 31, UY + 25, M + 35, UY + 29], fill=(255, 214, 120))
f_un = F(SANS, 20)
d.text((M + 62, UY + 8), "UNITED NATIONS", font=F(SANS_B, 16), fill=RED)
un_text = "Nations agree to pursue a global pact on lethal autonomous weapons"
d.text((M + 62, UY + 28), un_text, font=f_un, fill=INK)

# ---------------------------------------------------------------- ticker
TY = 970
d.text((M, TY), "ALSO TODAY", font=F(SANS_B, 17), fill=RED)
tick = ("Bolsonaro in intensive care in Brazil  -  AI helps crack a 167-year-old "
        "maths problem  -  Estonia to shut its border with Russia")
f_tick = F(SANS, 17)
lines = wrap(tick, f_tick, W - 2 * M - 130)
d.text((M + 130, TY), lines[0], font=f_tick, fill=INK)
if len(lines) > 1:
    d.text((M + 130, TY + 21), lines[1], font=f_tick, fill=INK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
