#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Pure Pillow, no network, deterministic: the same script always writes the
same bytes. The image is a newspaper front page: masthead with the date,
a lead story (Nvidia's first results since Jensen Huang resigned) with a
drawn chip illustration, two mid stories (Trump in Manila, Ukraine) and
three more (U.S. chip curbs, Canada-China trade, U.S. measles status),
plus an "also" strip. Every fact was checked against reporting from
18 November 2026 (BBC, Reuters, AP, NYT, CNBC/LSEG via trade press).
Attributed claims stay attributed ("U.S. intelligence reports..." style
is avoided here; the WSJ report is named as the Wall Street Journal's).
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 232)
INK = (24, 24, 24)
NAVY = (20, 38, 60)
RED = (178, 36, 28)
GREEN = (18, 110, 60)
GOLD = (200, 160, 40)
RULE = (118, 108, 92)
GREY = (64, 64, 64)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, fnt, max_w):
    """Greedy word wrap; returns the lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, fnt, fill, max_w, leading):
    """Draw a wrapped paragraph; returns y below the last line."""
    for line in wrap_text(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def frame(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255),
                outline=INK, width=2)


def tag(d, x, y, text, color=RED, size=20):
    f = F(SANS_B, size)
    d.text((x, y), text, font=f, fill=color)
    return y + size + 7


def head(d, x, y, text, max_w, size=34):
    return block(d, x, y, text, F(SERIF_B, size), INK, max_w,
                 int(size * 1.14))


def body(d, x, y, text, max_w, size=21):
    return block(d, x, y, text, F(SANS, size), (42, 42, 42), max_w,
                 int(size * 1.32))


# ------------------------------------------------------------------ art
def draw_chip(d, x0, y0, x1, y1):
    """Stylised GPU chip on a dark board, with a rising chart."""
    d.rectangle([x0, y0, x1, y1], fill=(16, 28, 22))
    # circuit traces
    for yy in range(y0 + 18, y1 - 18, 26):
        d.line([x0 + 10, yy, x0 + 60, yy], fill=(34, 80, 52), width=2)
        d.line([x1 - 60, yy, x1 - 10, yy], fill=(34, 80, 52), width=2)
    # the chip itself
    cx0, cy0, cx1, cy1 = x0 + 88, y0 + 34, x1 - 88, y1 - 96
    for px in range(cx0 + 14, cx1 - 10, 26):
        d.rectangle([px, cy0 - 12, px + 8, cy0], fill=(150, 160, 150))
        d.rectangle([px, cy1, px + 8, cy1 + 12], fill=(150, 160, 150))
    for py in range(cy0 + 14, cy1 - 10, 26):
        d.rectangle([cx0 - 12, py, cx0, py + 8], fill=(150, 160, 150))
        d.rectangle([cx1, py, cx1 + 12, py + 8], fill=(150, 160, 150))
    d.rectangle([cx0, cy0, cx1, cy1], fill=(44, 62, 50),
                outline=(190, 200, 190), width=3)
    d.rectangle([cx0 + 18, cy0 + 18, cx1 - 18, cy1 - 18],
                outline=(120, 160, 130), width=2)
    d.text(((cx0 + cx1) // 2, (cy0 + cy1) // 2 - 14), "NVDA",
           font=F(SANS_B, 34), fill=(220, 230, 220), anchor="ma")
    # rising chart line across the chip
    pts = [(cx0 + 26, cy1 - 34), (cx0 + 76, cy1 - 58),
           (cx0 + 118, cy1 - 48), (cx0 + 168, cy1 - 84),
           (cx1 - 26, cy1 - 108)]
    d.line(pts, fill=(110, 220, 140), width=5, joint="curve")
    d.ellipse([pts[-1][0] - 6, pts[-1][1] - 6,
               pts[-1][0] + 6, pts[-1][1] + 6], fill=(110, 220, 140))
    # figures below the chip
    d.text((x0 + 14, y1 - 74), "$115.8bn",
           font=F(SANS_B, 44), fill=(120, 230, 150))
    d.text((x0 + 14, y1 - 30), "REVENUE  +103% ON A YEAR AGO",
           font=F(SANS_B, 17), fill=(200, 210, 200))


def draw_summit_flags(d, x, y, s):
    """Three small flags: United States, China, Russia."""
    # United States: stripes + blue canton
    fx = x
    for i in range(7):
        d.rectangle([fx, y + i * 4, fx + s, y + i * 4 + 4],
                    fill=(178, 36, 28) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, y, fx + int(s * 0.42), y + 16], fill=(40, 70, 140))
    d.rectangle([fx, y, fx + s, y + 28], outline=INK, width=2)
    # China: red field, one yellow star
    fx = x + s + 14
    d.rectangle([fx, y, fx + s, y + 28], fill=(222, 41, 16),
                outline=INK, width=2)
    star = []
    scx, scy, sr = fx + 14, y + 12, 7
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = sr if k % 2 == 0 else sr * 0.42
        star.append((scx + rr * math.cos(ang), scy + rr * math.sin(ang)))
    d.polygon(star, fill=(255, 220, 60))
    # Russia: white-blue-red tricolour
    fx = x + 2 * (s + 14)
    for i, c in enumerate(((255, 255, 255), (30, 90, 180), (200, 30, 30))):
        d.rectangle([fx, y + i * 9, fx + s, y + i * 9 + 10], fill=c)
    d.rectangle([fx, y, fx + s, y + 28], outline=INK, width=2)


def draw_plane(d, x, y, s, color):
    """Small airliner silhouette, nose down, with a smoke trail behind."""
    # smoke puffs trailing to the left, level with the plane
    for (ox, oy, r) in ((-30, 4, 8), (-48, 8, 11), (-66, 12, 13)):
        d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r],
                  fill=(150, 150, 150))
    # fuselage, tilted
    d.polygon([(x, y), (x + s, y - s * 0.32), (x + s + 12, y - s * 0.30),
               (x + s + 4, y - s * 0.12), (x + 8, y + 6)], fill=color)
    # wing and tail
    d.polygon([(x + s * 0.42, y - s * 0.10), (x + s * 0.62, y + s * 0.34),
               (x + s * 0.74, y + s * 0.30), (x + s * 0.58, y - s * 0.16)],
              fill=color)
    d.polygon([(x + s * 0.82, y - s * 0.24), (x + s * 0.96, y - s * 0.52),
               (x + s + 8, y - s * 0.48), (x + s * 0.94, y - s * 0.20)],
              fill=color)


# ------------------------------------------------------------------ page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((W // 2, 12), "THE WORLD IN ONE IMAGE",
           font=F(SANS_B, 20), fill=GOLD, anchor="ma")
    d.text((W // 2, 40), "WEDNESDAY 18 NOVEMBER 2026",
           font=F(SERIF_B, 46), fill=(255, 255, 255), anchor="ma")
    d.line([24, 112, W - 24, 112], fill=RULE, width=2)

    # ---- lead story: Nvidia
    frame(d, 24, 122, 1000, 430)
    y = tag(d, 48, 136, "BUSINESS  —  LEAD STORY")
    y = head(d, 48, y, "NVIDIA DOUBLES SALES IN FIRST POST-HUANG REPORT",
             532, size=34)
    y += 8
    y = body(d, 48, y,
             "Revenue of $115.8bn, up 103% on a year ago and ahead of "
             "forecasts; $130bn guided for this quarter.",
             532, size=20)
    body(d, 48, y + 6,
         "Interim chief Colette Kress leads the call. The board will "
         "not reinstate Huang; the WSJ reports a U.S. civil inquiry.",
         532, size=20)
    draw_chip(d, 600, 140, 976, 412)

    # ---- row 2: two half-width stories
    # Trump in Manila
    frame(d, 24, 442, 500, 668)
    y = tag(d, 44, 456, "DIPLOMACY")
    draw_summit_flags(d, 330, 456, 40)
    y = head(d, 44, y, "TRUMP LANDS IN MANILA FOR ASEAN SUMMIT",
             432, size=28)
    body(d, 44, y + 4,
         "He meets Quad leaders in Manila, then flies to Shenzhen for "
         "Thursday's talks with Xi and Putin; Kim Jong Un may join.",
         432, size=19)

    # Ukraine
    frame(d, 524, 442, 1000, 668)
    y = tag(d, 544, 456, "WAR IN UKRAINE")
    draw_plane(d, 896, 470, 44, RED)
    y = head(d, 544, y, "KERCH BRIDGE HIT AGAIN; KYIV BRIDGES STRUCK",
             432, size=28)
    body(d, 544, y + 4,
         "Ukraine hits the Crimea crossing again; Russia strikes two "
         "Kyiv bridges; a plane crashes in Siberia, killing all 19.",
         432, size=19)

    # ---- row 3: three stories
    stories = [
        (24, 344, "TECH & TRADE",
         "U.S. SHUTS CHINA'S BACK DOOR TO AI CHIPS",
         "A new rule forces data centres in five countries to get a "
         "licence before advanced AI chips reach Chinese customers; "
         "Beijing vows countermeasures."),
        (356, 676, "TRADE",
         "CANADA AND CHINA EXTEND TRADE DEALS",
         "Beijing cuts tariffs on more Canadian pork and seafood as "
         "Xi meets Carney ahead of the APEC summit."),
        (688, 1000, "HEALTH",
         "U.S. LOSES MEASLES-FREE STATUS",
         "After 26 years, the U.S. loses its measles elimination "
         "status amid record cases — more than 5,400 this year."),
    ]
    for x0, x1, kick, headline_text, text in stories:
        frame(d, x0, 680, x1, 952)
        y = tag(d, x0 + 20, 694, kick, size=18)
        y = head(d, x0 + 20, y, headline_text, x1 - x0 - 40, size=24)
        body(d, x0 + 20, y + 4, text, x1 - x0 - 40, size=18)

    # ---- footer strip
    d.rectangle([0, 964, W, H], fill=NAVY)
    d.text((W // 2, 978),
           "ALSO: Five EU states plan a Rwanda hub  \u2022  Google flags "
           "first AI cyberattack  \u2022  Imran Khan fears for his life",
           font=F(SANS, 16), fill=(255, 255, 255), anchor="ma")
    return img


if __name__ == "__main__":
    build().save("entry.png", optimize=True)
    print("wrote entry.png")
