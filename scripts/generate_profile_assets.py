from __future__ import annotations

from pathlib import Path
from random import Random

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
W = 1600


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    paths = {
        "display": r"C:\Windows\Fonts\bahnschrift.ttf",
        "bold": r"C:\Windows\Fonts\segoeuib.ttf",
        "regular": r"C:\Windows\Fonts\segoeui.ttf",
        "mono": r"C:\Windows\Fonts\consola.ttf",
    }
    return ImageFont.truetype(paths[name], size=size)


DISPLAY = font("display", 112)
BOLD_56 = font("bold", 56)
BOLD_38 = font("bold", 38)
BOLD_30 = font("bold", 30)
REG_30 = font("regular", 30)
REG_26 = font("regular", 26)
REG_24 = font("regular", 24)
REG_22 = font("regular", 22)
MONO_22 = font("mono", 22)
MONO_18 = font("mono", 18)


INK = (242, 240, 232)
MUTED = (159, 168, 174)
SUBTLE = (82, 91, 98)
BLUE = (56, 201, 255)
GOLD = (202, 169, 91)
GREEN = (111, 223, 175)
BG = (5, 7, 10)
PANEL = (14, 18, 22)


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def add_noise(img: Image.Image, seed: int, opacity: int = 16) -> Image.Image:
    rng = Random(seed)
    noise = Image.new("RGBA", img.size, (0, 0, 0, 0))
    px = noise.load()
    for y in range(img.height):
        for x in range(img.width):
            v = rng.randint(0, opacity)
            px[x, y] = (255, 255, 255, v)
    return Image.alpha_composite(img.convert("RGBA"), noise)


def gradient_base(width: int, height: int) -> Image.Image:
    img = Image.new("RGBA", (width, height), BG + (255,))
    px = img.load()
    for y in range(height):
        for x in range(width):
            nx = x / width
            ny = y / height
            glow_a = max(0, 1 - ((nx - 0.14) ** 2 / 0.065 + (ny - 0.20) ** 2 / 0.20))
            glow_b = max(0, 1 - ((nx - 0.86) ** 2 / 0.11 + (ny - 0.82) ** 2 / 0.16))
            r = int(BG[0] + 20 * glow_a + 10 * glow_b)
            g = int(BG[1] + 26 * glow_a + 19 * glow_b)
            b = int(BG[2] + 28 * glow_a + 30 * glow_b)
            px[x, y] = (r, g, b, 255)
    return img


def draw_microgrid(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for x in range(80, width, 80):
        alpha = 34 if x % 240 == 0 else 18
        draw.line((x, 0, x, height), fill=(85, 102, 112, alpha), width=1)
    for y in range(70, height, 70):
        alpha = 30 if y % 210 == 0 else 16
        draw.line((0, y, width, y), fill=(85, 102, 112, alpha), width=1)


def text(draw: ImageDraw.ImageDraw, xy, value, fnt, fill=INK, anchor=None, spacing=8):
    draw.multiline_text(xy, value, font=fnt, fill=fill, anchor=anchor, spacing=spacing)


def draw_label(draw: ImageDraw.ImageDraw, x: int, y: int, value: str, color=BLUE) -> None:
    text(draw, (x, y), value.upper(), MONO_18, color)
    draw.line((x, y + 28, x + 92, y + 28), fill=color + (220,), width=2)


def make_hero() -> None:
    img = gradient_base(W, 620)
    img = add_noise(img, 11, 10)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_microgrid(draw, W, 620)

    draw.rectangle((0, 0, W, 620), outline=(219, 223, 220, 82), width=2)
    draw.rectangle((58, 54, W - 58, 566), outline=(219, 223, 220, 48), width=1)
    draw.line((98, 498, 725, 498), fill=GOLD + (210,), width=3)
    draw.line((810, 130, W - 98, 130), fill=BLUE + (170,), width=2)

    for i, x in enumerate(range(1010, 1465, 74)):
        draw.ellipse((x, 266, x + 8, 274), fill=(BLUE if i % 2 else GOLD) + (220,))
        draw.line((x + 4, 274, x + 4, 418), fill=(82, 104, 116, 150), width=1)

    draw_label(draw, 98, 88, "profile / systems")
    text(draw, (98, 172), "PRAYER7777777", DISPLAY, INK)
    text(draw, (106, 300), "compact cloud systems, agent workflows,\nautomation, and model-facing tools", REG_30, (204, 211, 210), spacing=10)

    rounded_rect(draw, (98, 420, 708, 474), 8, (10, 15, 18, 178), (204, 169, 91, 130))
    text(draw, (124, 435), "CLOUDFLARE WORKERS  /  MCP  /  TYPESCRIPT  /  PYTHON", MONO_18, (231, 224, 203))

    draw_label(draw, 1010, 182, "operating mode", GOLD)
    rows = [
        ("READ", "existing constraints"),
        ("BUILD", "runnable artifacts"),
        ("SHIP", "clean deployment paths"),
        ("LEAVE", "a visible trail"),
    ]
    y = 240
    for code, desc in rows:
        text(draw, (1010, y), code, MONO_22, INK)
        text(draw, (1138, y), desc, REG_22, MUTED)
        draw.line((1010, y + 42, 1444, y + 42), fill=(95, 105, 112, 90), width=1)
        y += 58

    text(draw, (W - 98, 522), "small systems / clean edges / no wasted motion", MONO_18, (184, 190, 190), anchor="ra")
    img.save(ASSETS / "profile-hero.png")


def project_card(draw, box, index, label, name, desc, accent):
    x1, y1, x2, y2 = box
    rounded_rect(draw, box, 10, PANEL + (235,), (115, 125, 132, 130), 1)
    draw.line((x1 + 30, y1 + 34, x1 + 122, y1 + 34), fill=accent + (230,), width=3)
    text(draw, (x2 - 30, y1 + 24), f"0{index}", MONO_22, (104, 112, 118), anchor="ra")
    text(draw, (x1 + 30, y1 + 62), label.upper(), MONO_18, MUTED)
    text(draw, (x1 + 30, y1 + 112), name, BOLD_38, INK)
    text(draw, (x1 + 30, y1 + 172), desc, REG_24, (202, 208, 207), spacing=8)


def make_systems() -> None:
    img = gradient_base(W, 900)
    img = add_noise(img, 29, 8)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_microgrid(draw, W, 900)

    draw.rectangle((0, 0, W, 900), outline=(219, 223, 220, 82), width=2)
    text(draw, (90, 74), "SELECTED SYSTEMS", BOLD_56, INK)
    text(draw, (92, 146), "work that points toward smaller infrastructure, clearer interfaces, and practical automation", REG_26, MUTED)
    draw.line((92, 205, W - 92, 205), fill=(212, 217, 211, 86), width=1)

    cards = [
        ((90, 250, 760, 520), 1, "remote mcp / search", "GrokSearch", "Cloudflare-native search direction\nwith fewer servers and direct access.", BLUE),
        ((840, 250, 1510, 520), 2, "model reasoning", "model-council", "Compare model outputs and make\nmulti-model judgment inspectable.", GOLD),
        ((90, 560, 760, 830), 3, "cloud service", "cloud-mail", "Mail and cloud-service experiments\nwith usable deployment paths.", GREEN),
        ((840, 560, 1510, 830), 4, "mcp wrapper", "newapi-mcp", "Small wrapper experiment for New API\nstyle services and agent-facing access.", (214, 136, 255)),
    ]
    for args in cards:
        project_card(draw, *args)

    img.save(ASSETS / "profile-systems.png")


def make_footer() -> None:
    img = gradient_base(W, 310)
    img = add_noise(img, 47, 8)
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle((0, 0, W, 310), outline=(219, 223, 220, 82), width=2)

    labels = [
        ("Cloudflare Workers", BLUE),
        ("MCP", GOLD),
        ("GitHub Actions", GREEN),
        ("TypeScript", (214, 136, 255)),
        ("Python", (255, 219, 120)),
        ("PowerShell", (120, 190, 255)),
        ("Docker", (130, 214, 255)),
        ("Linux", (210, 216, 216)),
    ]
    text(draw, (88, 64), "STACK", BOLD_38, INK)
    x, y = 88, 145
    for label, accent in labels:
        bbox = draw.textbbox((0, 0), label, font=MONO_22)
        w = bbox[2] - bbox[0] + 36
        rounded_rect(draw, (x, y, x + w, y + 48), 8, (16, 21, 26, 235), accent + (150,), 1)
        text(draw, (x + 18, y + 12), label, MONO_22, (235, 238, 235))
        x += w + 16
        if x > 1380:
            x, y = 88, y + 70
    text(draw, (W - 88, 252), "prototype -> harden -> document -> deploy", MONO_18, MUTED, anchor="ra")

    img.save(ASSETS / "profile-stack.png")


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    make_hero()
    make_systems()
    make_footer()


if __name__ == "__main__":
    main()
