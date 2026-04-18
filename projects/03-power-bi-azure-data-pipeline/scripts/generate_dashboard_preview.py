#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
OUTPUT_PATH = ARTIFACTS_DIR / "02-dashboard-preview.png"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
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


def read_fact_rows() -> list[dict[str, str]]:
    with (DATA_DIR / "fact_security_governance_daily.csv").open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_dimension(path: Path, key_name: str, value_name: str) -> dict[str, str]:
    with path.open(encoding="utf-8") as handle:
        return {row[key_name]: row[value_name] for row in csv.DictReader(handle)}


def kpi_value(rows: list[dict[str, str]], column: str) -> int:
    return sum(int(row[column]) for row in rows)


def avg_value(rows: list[dict[str, str]], column: str) -> float:
    values = [float(row[column]) for row in rows]
    return sum(values) / max(1, len(values))


def month_key(date_key: str) -> str:
    return f"{date_key[:4]}-{date_key[4:6]}"


def aggregate_by_month(rows: list[dict[str, str]], metric: str) -> list[tuple[str, float]]:
    bucket: defaultdict[str, float] = defaultdict(float)
    for row in rows:
        bucket[month_key(row["DateKey"])] += float(row[metric])
    return sorted(bucket.items())


def aggregate_by_workload(rows: list[dict[str, str]], workload_names: dict[str, str]) -> list[tuple[str, int]]:
    bucket: defaultdict[str, int] = defaultdict(int)
    for row in rows:
        incidents = int(row["HighSeverityIncidents"]) + int(row["MediumSeverityIncidents"])
        bucket[workload_names[row["WorkloadKey"]]] += incidents
    return sorted(bucket.items(), key=lambda item: item[1], reverse=True)


def aggregate_guest_by_department(rows: list[dict[str, str]], department_names: dict[str, str]) -> list[tuple[str, int]]:
    bucket: defaultdict[str, int] = defaultdict(int)
    for row in rows:
        bucket[department_names[row["DepartmentKey"]]] += int(row["GuestAccountsActive"])
    return sorted(bucket.items(), key=lambda item: item[1], reverse=True)


def draw_wrapped_text(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], font, fill, max_width: int, line_gap: int = 6) -> int:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
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


def draw_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, value: str, subtitle: str, accent: str) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=24, fill="#101827", outline="#1E293B", width=2)
    draw.rounded_rectangle((x1 + 20, y1 + 18, x1 + 100, y1 + 30), radius=6, fill=accent)
    title_font = load_font(22, bold=True)
    value_font = load_font(42, bold=True)
    body_font = load_font(18)
    draw.text((x1 + 22, y1 + 42), title, font=title_font, fill="#DCE7F3")
    draw.text((x1 + 22, y1 + 82), value, font=value_font, fill="#FFFFFF")
    draw.text((x1 + 22, y1 + 140), subtitle, font=body_font, fill="#9FB0C7")


def draw_line_chart(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, series_a: list[tuple[str, float]], series_b: list[tuple[str, float]]) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=28, fill="#0F172A", outline="#1E293B", width=2)
    title_font = load_font(24, bold=True)
    axis_font = load_font(16)
    draw.text((x1 + 24, y1 + 18), title, font=title_font, fill="#E5EEF9")

    chart_x1, chart_y1 = x1 + 50, y1 + 80
    chart_x2, chart_y2 = x2 - 30, y2 - 60
    draw.rectangle((chart_x1, chart_y1, chart_x2, chart_y2), outline="#223048", width=2)

    combined = [value for _, value in series_a] + [value for _, value in series_b]
    max_value = max(combined) if combined else 1

    for index in range(1, 4):
        y = chart_y2 - ((chart_y2 - chart_y1) * index / 4)
        draw.line((chart_x1, y, chart_x2, y), fill="#1E293B", width=1)

    def plot(series, color):
        points = []
        for idx, (label, value) in enumerate(series):
            x = chart_x1 + int((chart_x2 - chart_x1) * idx / max(1, len(series) - 1))
            y = chart_y2 - int((chart_y2 - chart_y1) * (value / max_value))
            points.append((x, y))
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)
            draw.text((x - 22, chart_y2 + 10), label[-2:], font=axis_font, fill="#92A6C2")
        if len(points) > 1:
            draw.line(points, fill=color, width=4)

    plot(series_a, "#3B82F6")
    plot(series_b, "#F59E0B")

    draw.rounded_rectangle((x2 - 205, y1 + 18, x2 - 118, y1 + 44), radius=10, fill="#10253F")
    draw.rounded_rectangle((x2 - 112, y1 + 18, x2 - 25, y1 + 44), radius=10, fill="#33240E")
    draw.text((x2 - 194, y1 + 22), "Failures", font=axis_font, fill="#9DC5FF")
    draw.text((x2 - 102, y1 + 22), "Incidents", font=axis_font, fill="#F8C676")


def draw_bar_chart(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, items: list[tuple[str, int]], bar_color: str) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=28, fill="#0F172A", outline="#1E293B", width=2)
    title_font = load_font(24, bold=True)
    label_font = load_font(18)
    value_font = load_font(16, bold=True)
    draw.text((x1 + 24, y1 + 18), title, font=title_font, fill="#E5EEF9")

    chart_x1, chart_x2 = x1 + 26, x2 - 24
    start_y = y1 + 78
    row_height = 58
    max_value = max((value for _, value in items), default=1)
    for idx, (label, value) in enumerate(items[:4]):
        top = start_y + idx * row_height
        draw.text((chart_x1, top), label, font=label_font, fill="#C9D7E8")
        bar_left = chart_x1 + 190
        bar_right = bar_left + int((chart_x2 - bar_left) * (value / max_value))
        draw.rounded_rectangle((bar_left, top + 4, chart_x2, top + 32), radius=12, fill="#162235")
        draw.rounded_rectangle((bar_left, top + 4, bar_right, top + 32), radius=12, fill=bar_color)
        draw.text((chart_x2 - 44, top + 8), str(value), font=value_font, fill="#F8FAFC")


def main() -> None:
    rows = read_fact_rows()
    department_names = read_dimension(DATA_DIR / "dim_department.csv", "DepartmentKey", "DepartmentName")
    workload_names = read_dimension(DATA_DIR / "dim_workload.csv", "WorkloadKey", "WorkloadName")

    failures = kpi_value(rows, "SignInFailures")
    incidents = kpi_value(rows, "HighSeverityIncidents") + kpi_value(rows, "MediumSeverityIncidents")
    compliance = avg_value(rows, "ComplianceScore")
    guests = kpi_value(rows, "GuestAccountsActive")

    line_failures = aggregate_by_month(rows, "SignInFailures")
    line_incidents = [(label, int(value)) for label, value in aggregate_by_month(rows, "HighSeverityIncidents")]
    bar_workloads = aggregate_by_workload(rows, workload_names)
    bar_guests = aggregate_guest_by_department(rows, department_names)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1600, 940), "#09111F")
    draw = ImageDraw.Draw(image)

    title_font = load_font(40, bold=True)
    subtitle_font = load_font(22)
    small_font = load_font(18)

    draw.text((48, 32), "Astera University Security & Governance Dashboard Preview", font=title_font, fill="#F8FAFC")
    draw.text((48, 86), "Sample Power BI executive page built from the generated portfolio dataset", font=subtitle_font, fill="#A6B8D3")
    draw.rounded_rectangle((1210, 30, 1548, 86), radius=24, fill="#11233E", outline="#1D3355", width=2)
    draw.text((1236, 49), "Project 03 · Power BI + Azure Data Pipeline", font=small_font, fill="#B6CCEA")

    card_y1, card_y2 = 132, 330
    card_width = 356
    gap = 18
    boxes = []
    for idx in range(4):
        x1 = 48 + idx * (card_width + gap)
        boxes.append((x1, card_y1, x1 + card_width, card_y2))

    draw_card(draw, boxes[0], "Total Sign-In Failures", f"{failures:,}", "Identity noise across all departments", "#2563EB")
    draw_card(draw, boxes[1], "Total Incidents", f"{incidents:,}", "High + medium severity operational load", "#F59E0B")
    draw_card(draw, boxes[2], "Average Compliance Score", f"{compliance:.1f}", "Posture trend modeled at daily grain", "#10B981")
    draw_card(draw, boxes[3], "Active Guest Accounts", f"{guests:,}", "Collaboration exposure across teams", "#8B5CF6")

    draw_line_chart(draw, (48, 362, 1020, 888), "Monthly Trend: Failures vs High Severity Incidents", line_failures, line_incidents)
    draw_bar_chart(draw, (1048, 362, 1548, 618), "Incidents by Workload", bar_workloads, "#F97316")
    draw_bar_chart(draw, (1048, 632, 1548, 888), "Guest Exposure by Department", bar_guests, "#7C3AED")

    insight_box = (48, 900, 1548, 928)
    draw.rounded_rectangle(insight_box, radius=14, fill="#0E1A2E")
    draw.text((64, 904), "Storyline: Are we getting safer, or just busier? This preview pairs incident pressure, compliance maturity, and guest growth on one page.", font=small_font, fill="#B8C7DA")

    image.save(OUTPUT_PATH)
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
