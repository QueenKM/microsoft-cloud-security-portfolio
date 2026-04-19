#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "artifacts" / "01-iac-baseline-overview.png"


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


def wrap_text(draw, text, xy, font, fill, max_width, line_gap=6):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y = bbox[3] + line_gap


def box(draw, rect, title, bullets, accent):
    x1, y1, x2, y2 = rect
    draw.rounded_rectangle(rect, radius=24, fill="#101827", outline="#1E293B", width=2)
    draw.rounded_rectangle((x1 + 18, y1 + 18, x1 + 104, y1 + 30), radius=6, fill=accent)
    draw.text((x1 + 18, y1 + 40), title, font=load_font(24, bold=True), fill="#F8FAFC")
    bullet_font = load_font(18)
    current_y = y1 + 88
    for bullet in bullets:
        draw.ellipse((x1 + 20, current_y + 6, x1 + 30, current_y + 16), fill=accent)
        wrap_text(draw, bullet, (x1 + 42, current_y), bullet_font, "#C8D4E3", x2 - x1 - 58)
        current_y += 54


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1600, 980), "#08111E")
    draw = ImageDraw.Draw(image)

    draw.text((48, 30), "Azure IaC Baseline Preview", font=load_font(40, bold=True), fill="#F8FAFC")
    draw.text(
        (48, 84),
        "Subscription-scope Bicep landing zone for the Cloud Security Lab.",
        font=load_font(22),
        fill="#A5B8D2",
    )
    draw.rounded_rectangle((1206, 28, 1548, 84), radius=24, fill="#11233E", outline="#1D3355", width=2)
    draw.text((1234, 47), "Project 04 · Azure IaC", font=load_font(18), fill="#B6CCEA")

    box(
        draw,
        (48, 132, 384, 428),
        "Resource Groups",
        [
            "Identity monitoring resource group",
            "Security operations resource group",
            "Demo workload resource group",
            "Consistent tags and naming baseline",
        ],
        "#2563EB",
    )
    box(
        draw,
        (420, 132, 756, 428),
        "Network Layer",
        [
            "One core virtual network",
            "Separate management and workload subnets",
            "Dedicated NSGs for each subnet",
            "Storage service endpoint in workload subnet",
        ],
        "#8B5CF6",
    )
    box(
        draw,
        (792, 132, 1128, 428),
        "Monitoring Layer",
        [
            "Central Log Analytics workspace",
            "NSG diagnostic settings to workspace",
            "Storage blob diagnostic settings to workspace",
            "Scheduled query alert modules",
        ],
        "#10B981",
    )
    box(
        draw,
        (1164, 132, 1548, 428),
        "Optional Extensions",
        [
            "Linux VM workload",
            "RBAC role assignments",
            "Email-backed action group",
            "Platform alert rules",
        ],
        "#F59E0B",
    )

    draw.rounded_rectangle((48, 472, 1548, 842), radius=28, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((72, 496), "Deployment Flow", font=load_font(28, bold=True), fill="#F8FAFC")

    lanes = [
        ("Subscription Scope", "#2563EB"),
        ("Resource Groups", "#8B5CF6"),
        ("Core Services", "#10B981"),
        ("Detection Layer", "#F59E0B"),
    ]
    x = 74
    for label, color in lanes:
        rect = (x, 580, x + 300, 680)
        draw.rounded_rectangle(rect, radius=20, fill="#111D31", outline=color, width=3)
        wrap_text(draw, label, (x + 22, 612), load_font(22, bold=True), "#E5EEF9", 256)
        x += 344

    for start_x in (374, 718, 1062):
        y = 630
        draw.line((start_x, y, start_x + 40, y), fill="#4B678A", width=4)
        draw.polygon([(start_x + 40, y), (start_x + 28, y - 8), (start_x + 28, y + 8)], fill="#4B678A")

    wrap_text(
        draw,
        "Outcome: a reproducible Azure baseline that creates the lab resource structure, telemetry plumbing, and first alerting controls before any manual security validation begins.",
        (72, 734),
        load_font(19),
        "#B8C7DA",
        1420,
    )

    draw.rounded_rectangle((48, 878, 1548, 934), radius=18, fill="#0F1B30")
    draw.text(
        (66, 896),
        "This project is the infrastructure backbone for the live Cloud Security Lab deployment.",
        font=load_font(18),
        fill="#B8C7DA",
    )

    image.save(OUTPUT_PATH)
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
