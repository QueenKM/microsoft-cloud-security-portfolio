#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO_ROOT / "shared-assets" / "portfolio-preview.png"

SOURCES = [
    (
        "Project 01 · Cloud Security Lab",
        REPO_ROOT / "projects/01-cloud-security-lab/artifacts/screenshots/07-sentinel-overview.png",
    ),
    (
        "Project 03 · Power BI + Azure Data Pipeline",
        REPO_ROOT / "projects/03-power-bi-azure-data-pipeline/artifacts/02-dashboard-preview.png",
    ),
    (
        "Project 05 · Cyber Risk Assessment Tool",
        REPO_ROOT / "projects/05-cyber-risk-assessment-tool/artifacts/01-main-dashboard.png",
    ),
    (
        "Project 06 · Teams Governance Toolkit",
        REPO_ROOT / "projects/06-teams-governance-toolkit/artifacts/02-governance-overview.png",
    ),
]


def load_font(size: int, bold: bool = False):
    candidates = []
    if bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/Library/Fonts/Arial Bold.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/Library/Fonts/Arial.ttf",
            ]
        )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def fit_cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = image.size
    scale = max(target_w / src_w, target_h / src_h)
    resized = image.resize((int(src_w * scale), int(src_h * scale)))
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def main() -> None:
    canvas = Image.new("RGB", (1800, 1280), "#08111E")
    draw = ImageDraw.Draw(canvas)

    title_font = load_font(54, bold=True)
    subtitle_font = load_font(26)
    chip_font = load_font(20, bold=True)

    draw.text((56, 40), "Microsoft Cloud Security Portfolio", font=title_font, fill="#F8FAFC")
    draw.text(
        (56, 110),
        "Azure security, Zero Trust, analytics, governance, and practical security software in one connected portfolio.",
        font=subtitle_font,
        fill="#A6B8D3",
    )

    positions = [
        (56, 180, 868, 646),
        (932, 180, 1744, 646),
        (56, 710, 868, 1176),
        (932, 710, 1744, 1176),
    ]

    for (label, source), box in zip(SOURCES, positions):
        x1, y1, x2, y2 = box
        draw.rounded_rectangle(box, radius=30, fill="#101827", outline="#1E293B", width=3)
        if source.exists():
            image = Image.open(source).convert("RGB")
            preview = fit_cover(image, (x2 - x1 - 20, y2 - y1 - 84))
            canvas.paste(preview, (x1 + 10, y1 + 10))
        chip_box = (x1 + 18, y2 - 62, x1 + 390, y2 - 18)
        draw.rounded_rectangle(chip_box, radius=18, fill="#0E1F38", outline="#22456B", width=2)
        draw.text((x1 + 34, y2 - 50), label, font=chip_font, fill="#D8E8FB")

    footer = "Shared scenario: Astera University · Interview-ready artifacts with live Azure evidence, governance docs, generated analytics assets, and desktop app demos."
    draw.rounded_rectangle((56, 1210, 1744, 1256), radius=18, fill="#0E1A2E")
    draw.text((72, 1221), footer, font=load_font(19), fill="#B8C7DA")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT_PATH)
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
