#!/usr/bin/env python3
"""Compose the 19 Nov 2026 world-news poster (1024x1024) from the generated
background photo + crisp real text. Output is deterministic: same bytes every run."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BG = "/home/hatch/workspace/make-fun/news-image-20261118/bg18.png"
OUT = "/home/hatch/workspace/make-fun/news-image-20261118/entry.png"

W, H = 1024, 1024
NAVY = (13, 21, 38)
AMBER = (245, 176, 65)
WHITE = (255, 255, 255)
GREY = (196, 205, 219)
RULE = (70, 90, 120)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

F_TITLE = font("DejaVuSerif-Bold.ttf", 64)
F_KICK = font("DejaVuSans-Bold.ttf", 26)
F_SUB = font("DejaVuSans.ttf", 24)
F_HEAD = font("DejaVuSans-Bold.ttf", 25)
F_BODY = font("DejaVuSans.ttf", 21)
F_TICK = font("DejaVuSans.ttf", 19)
F_NUM = font("DejaVuSans-Bold.ttf", 30)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

bg = Image.open(BG).convert("RGB")
# crop photo to 1024x560 (top band)
bw, bh = bg.size
scale = max(1024 / bw, 480 / bh)
bg = bg.resize((int(bw * scale) + 1, int(bh * scale) + 1), Image.LANCZOS)
x0 = (bg.width - 1024) // 2
bg = bg.crop((x0, 0, x0 + 1024, 480))
bg = bg.filter(ImageFilter.GaussianBlur(0.6))

canvas = Image.new("RGB", (W, H), NAVY)
canvas.paste(bg, (0, 0))
d = ImageDraw.Draw(canvas, "RGBA")

# dark gradient over photo for header legibility
for y in range(0, 480):
    a = int(150 * (1 - y / 480) ** 1.5) + 40
    d.rectangle([0, y, 1024, y + 1], fill=(8, 12, 24, a))
d.rectangle([0, 440, 1024, 480], fill=(8, 12, 24, 160))

# header
d.text((48, 36), "THE WORLD TODAY", font=F_KICK, fill=AMBER)
d.text((48, 78), "18 NOVEMBER 2026", font=F_TITLE, fill=WHITE)
d.text((48, 158), "WEDNESDAY  —  WORLD NEWS IN ONE IMAGE", font=F_SUB, fill=GREY)
d.rectangle([48, 210, 976, 212], fill=AMBER)

stories = [
    ("01", "US AND IRAN TRADE STRIKES",
     "US hits a missile site on Qeshm Island after Iran strikes US bases in Bahrain and Kuwait."),
    ("02", "TRUMP–XI–PUTIN SUMMIT SET",
     "Three leaders to meet in Shenzhen at APEC on Thursday; nuclear arms and Ukraine on the agenda."),
    ("03", "NVIDIA SHAKE-UP",
     "Founder Jensen Huang resigns; acting CEO Colette Kress promises earlier pay rises at first all-hands."),
    ("04", "COP31 CLIMATE TALKS",
     "Delegates push for a deal as negotiations enter a decisive phase."),
    ("05", "FED SIGNALS MORE HIKES",
     "Minutes show most officials expect further rate rises if inflation stays high."),
]

y = 500
for num, head, body in stories:
    d.text((48, y), num, font=F_NUM, fill=AMBER)
    d.text((110, y + 2), head, font=F_HEAD, fill=WHITE)
    lines = wrap(d, body, F_BODY, 1024 - 110 - 48)
    by = y + 34
    for ln in lines[:2]:
        d.text((110, by), ln, font=F_BODY, fill=GREY)
        by += 25
    y = max(by + 8, y + 92)
    if num != "05":
        d.line([48, y - 6, 976, y - 6], fill=RULE, width=1)

# footer ticker
d.rectangle([0, 975, 1024, 1024], fill=(8, 12, 24))
d.text((48, 987), "ALSO: GTA VI rollout begins  •  Voyager 1 reaches a light-day  •  Estonia to close Russia border Dec 1",
       font=F_TICK, fill=GREY)

canvas.save(OUT, "JPEG", quality=90, optimize=True, progressive=False)
import os
print("saved", OUT, os.path.getsize(OUT), "bytes", canvas.size)
