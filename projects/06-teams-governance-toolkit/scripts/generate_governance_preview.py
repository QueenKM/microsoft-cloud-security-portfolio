#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = BASE_DIR / "artifacts"
OUTPUT_PATH = ARTIFACTS_DIR / "02-governance-overview.png"


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


def wrapped_text(draw, text, xy, font, fill, max_width, line_gap=6):
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
    return y


def card(draw, box, title, bullets, accent):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=26, fill="#101827", outline="#1E293B", width=2)
    draw.rounded_rectangle((x1 + 22, y1 + 18, x1 + 108, y1 + 30), radius=6, fill=accent)
    title_font = load_font(24, bold=True)
    body_font = load_font(17)
    draw.text((x1 + 22, y1 + 42), title, font=title_font, fill="#F8FAFC")
    current_y = y1 + 88
    for bullet in bullets:
        draw.ellipse((x1 + 24, current_y + 6, x1 + 34, current_y + 16), fill=accent)
        current_y = wrapped_text(draw, bullet, (x1 + 46, current_y), body_font, "#C7D2E1", max_width=x2 - x1 - 70)
        current_y += 16


def decision_lane(draw, box):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=26, fill="#0F172A", outline="#1E293B", width=2)
    title_font = load_font(24, bold=True)
    body_font = load_font(18)
    draw.text((x1 + 24, y1 + 18), "External Collaboration Decision Path", font=title_font, fill="#F8FAFC")

    nodes = [
        ("Need external collaboration?", "#1D4ED8"),
        ("Full team access needed?", "#F59E0B"),
        ("Use guest access", "#8B5CF6"),
        ("Use shared channel", "#10B981"),
    ]
    node_boxes = []
    current_x = x1 + 24
    for text, color in nodes:
        box_width = 260
        node_box = (current_x, y1 + 82, current_x + box_width, y1 + 164)
        node_boxes.append((node_box, color, text))
        current_x += box_width + 26

    for node_box, color, text in node_boxes:
        draw.rounded_rectangle(node_box, radius=22, fill="#111D31", outline=color, width=3)
        wrapped_text(draw, text, (node_box[0] + 18, node_box[1] + 20), body_font, "#E3EDF7", max_width=node_box[2] - node_box[0] - 36)

    for idx in range(len(node_boxes) - 1):
        left = node_boxes[idx][0]
        right = node_boxes[idx + 1][0]
        y = (left[1] + left[3]) // 2
        draw.line((left[2] + 8, y, right[0] - 8, y), fill="#4B678A", width=4)
        draw.polygon([(right[0] - 8, y), (right[0] - 20, y - 8), (right[0] - 20, y + 8)], fill="#4B678A")

    wrapped_text(
        draw,
        "Principle: prefer shared channels when collaboration can stay inside one bounded workstream. Use guests when the external party genuinely needs full team participation.",
        (x1 + 24, y1 + 202),
        body_font,
        "#AFC2D8",
        max_width=x2 - x1 - 48,
    )


def main():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (1600, 980), "#08111E")
    draw = ImageDraw.Draw(image)

    title_font = load_font(40, bold=True)
    subtitle_font = load_font(22)
    small_font = load_font(18)

    draw.text((48, 30), "Microsoft Teams Governance Toolkit Preview", font=title_font, fill="#F8FAFC")
    draw.text((48, 84), "A policy and operating model view for controlled collaboration at Astera University", font=subtitle_font, fill="#A5B8D2")
    draw.rounded_rectangle((1208, 28, 1548, 84), radius=24, fill="#11233E", outline="#1D3355", width=2)
    draw.text((1232, 47), "Project 06 · Teams Governance Toolkit", font=small_font, fill="#B6CCEA")

    card(draw, (48, 132, 388, 462), "Provisioning Baseline", [
        "Controlled self-service with request metadata",
        "Minimum two owners per team",
        "Naming policy enforced through Microsoft 365 groups",
        "Standard templates for department, project, and vendor teams",
    ], "#2563EB")

    card(draw, (420, 132, 760, 462), "Access & Sharing", [
        "Guest access only with sponsor and business justification",
        "Shared channels preferred for bounded partner workstreams",
        "Sensitivity guides privacy and guest restrictions",
        "Quarterly guest review required for active external teams",
    ], "#8B5CF6")

    card(draw, (792, 132, 1132, 462), "Lifecycle", [
        "180-day review checkpoint",
        "Archive before delete by default",
        "Dormant teams flagged for owner validation",
        "Exception handling stays time-bound and documented",
    ], "#10B981")

    card(draw, (1164, 132, 1548, 462), "Owner Expectations", [
        "Keep two active owners assigned",
        "Remove stale guests and members",
        "Renew or retire the team on schedule",
        "Escalate policy conflicts instead of bypassing them",
    ], "#F59E0B")

    decision_lane(draw, (48, 500, 1548, 842))

    footer = "Governance story: enable collaboration without losing control of guest access, naming, ownership, and stale workspace cleanup."
    draw.rounded_rectangle((48, 872, 1548, 930), radius=18, fill="#0F1B30")
    draw.text((64, 892), footer, font=small_font, fill="#B8C7DA")

    image.save(OUTPUT_PATH)
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
