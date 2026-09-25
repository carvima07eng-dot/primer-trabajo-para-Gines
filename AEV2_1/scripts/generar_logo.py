"""Genera el logotipo de TechParts S.L.: engranaje con pistas de circuito."""
import math
from PIL import Image, ImageDraw, ImageFont

S = 4  # sobremuestreo para bordes suaves
W, H = 600 * S, 600 * S
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
cx, cy = W // 2, int(H * 0.42)
AZUL, NARANJA, BLANCO = (18, 74, 128), (245, 140, 30), (255, 255, 255)

# Engranaje: 12 dientes
r_ext, r_int, dientes = 200 * S, 165 * S, 12
pts = []
for i in range(dientes * 4):
    a = 2 * math.pi * i / (dientes * 4)
    r = r_ext if (i % 4) in (1, 2) else r_int
    pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
d.polygon(pts, fill=AZUL)
d.ellipse([cx - 120 * S, cy - 120 * S, cx + 120 * S, cy + 120 * S], fill=BLANCO)
d.ellipse([cx - 100 * S, cy - 100 * S, cx + 100 * S, cy + 100 * S], fill=NARANJA)

# Pistas de circuito dentro del engranaje
lw = 9 * S
for dy, x2 in ((-45, 55), (0, 70), (45, 55)):
    y = cy + dy * S
    d.line([(cx - 70 * S, y), (cx + x2 * S - 25 * S, y)], fill=BLANCO, width=lw)
    d.line([(cx + x2 * S - 25 * S, y), (cx + x2 * S, y - (25 * S if dy < 0 else -25 * S if dy > 0 else 0))], fill=BLANCO, width=lw)
    d.ellipse([cx - 82 * S, y - 13 * S, cx - 56 * S, y + 13 * S], fill=BLANCO)

# Texto
try:
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 78 * S)
except OSError:
    f = ImageFont.load_default()
txt = "TechParts"
tw = d.textlength(txt, font=f)
d.text(((W - tw) / 2, 470 * S), txt, font=f, fill=AZUL)

img = img.resize((600, 600), Image.LANCZOS)
img.save("../proyecto/logo_techparts.png")
print("logo generado")
