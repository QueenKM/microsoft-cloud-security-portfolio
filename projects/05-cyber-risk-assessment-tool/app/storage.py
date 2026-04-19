from __future__ import annotations

import csv
from datetime import datetime, timezone
import html
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from typing import Iterable

from models import RiskItem
from scoring import classify_risk, risk_row, summarize_risks


EXPORT_FIELDNAMES = [
    "identifier",
    "title",
    "category",
    "asset",
    "scenario",
    "owner",
    "status",
    "impact",
    "likelihood",
    "control_effectiveness",
    "inherent_score",
    "residual_score",
    "risk_level",
    "existing_controls",
    "notes",
]


def _risk_rows(risks: Iterable[RiskItem]) -> list[dict[str, str | int]]:
    return [risk_row(risk) for risk in risks]


def load_risks(path: Path) -> list[RiskItem]:
    if not path.exists():
        return []

    payload = json.loads(path.read_text(encoding="utf-8"))
    return [RiskItem.from_dict(item) for item in payload]


def save_risks(path: Path, risks: Iterable[RiskItem]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = [risk.to_dict() for risk in risks]
    path.write_text(json.dumps(serialized, indent=2), encoding="utf-8")


def load_scenario(path: Path) -> list[RiskItem]:
    return load_risks(path)


def export_csv(path: Path, risks: Iterable[RiskItem]) -> None:
    rows = _risk_rows(risks)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPORT_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def export_pdf(path: Path, risks: Iterable[RiskItem]) -> None:
    import os

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtGui import QPageSize, QPdfWriter, QTextDocument
    from PySide6.QtWidgets import QApplication

    rows = _risk_rows(risks)
    summary = summarize_risks(RiskItem.from_dict(row) for row in rows)
    app = QApplication.instance()
    owns_app = False
    if app is None:
        app = QApplication([])
        owns_app = True

    path.parent.mkdir(parents=True, exist_ok=True)
    writer = QPdfWriter(str(path))
    writer.setPageSize(QPageSize(QPageSize.A4))
    writer.setResolution(96)

    document = QTextDocument()
    document.setHtml(_build_pdf_html(rows, summary))
    document.print_(writer)

    if owns_app:
        app.quit()


def export_xlsx(path: Path, risks: Iterable[RiskItem]) -> None:
    rows = _risk_rows(risks)
    summary = summarize_risks(RiskItem.from_dict(row) for row in rows)
    path.parent.mkdir(parents=True, exist_ok=True)

    summary_rows: list[list[str | int | float]] = [
        ["Metric", "Value"],
        ["Export generated (UTC)", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")],
        ["Total risks", int(summary["total"])],
        ["Critical risks", int(summary["critical"])],
        ["High risks", int(summary["high"])],
        ["Average residual score", float(summary["average_residual_score"])],
    ]

    register_rows: list[list[str | int]] = [
        [_pretty_header(name) for name in EXPORT_FIELDNAMES]
    ]
    for row in rows:
        register_rows.append([row[name] for name in EXPORT_FIELDNAMES])

    with ZipFile(path, "w", compression=ZIP_DEFLATED) as workbook:
        workbook.writestr("[Content_Types].xml", _content_types_xml())
        workbook.writestr("_rels/.rels", _rels_xml())
        workbook.writestr("docProps/app.xml", _doc_props_app_xml())
        workbook.writestr("docProps/core.xml", _doc_props_core_xml())
        workbook.writestr("xl/workbook.xml", _workbook_xml())
        workbook.writestr("xl/_rels/workbook.xml.rels", _workbook_rels_xml())
        workbook.writestr("xl/styles.xml", _styles_xml())
        workbook.writestr(
            "xl/worksheets/sheet1.xml",
            _worksheet_xml(
                "Summary",
                summary_rows,
                header_row=1,
                title=None,
                widths=[38, 22],
                freeze_top=False,
                auto_filter=False,
            ),
        )
        workbook.writestr(
            "xl/worksheets/sheet2.xml",
            _worksheet_xml(
                "Risk Register",
                register_rows,
                header_row=1,
                title=None,
                widths=[18, 24, 18, 22, 32, 18, 14, 10, 10, 20, 12, 12, 14, 28, 36],
                freeze_top=True,
                auto_filter=True,
            ),
        )


def _pretty_header(name: str) -> str:
    return name.replace("_", " ").title()


def _build_pdf_html(rows: list[dict[str, str | int]], summary: dict[str, float | int]) -> str:
    table_rows = []
    for row in rows:
        table_rows.append(
            "<tr>"
            f"<td>{html.escape(str(row['title']))}</td>"
            f"<td>{html.escape(str(row['category']))}</td>"
            f"<td>{html.escape(str(row['owner']))}</td>"
            f"<td>{row['residual_score']}</td>"
            f"<td>{html.escape(str(row['risk_level']))}</td>"
            f"<td>{html.escape(str(row['status']))}</td>"
            "</tr>"
        )
    table_html = "".join(table_rows) or (
        "<tr><td colspan='6'>No risks available in the current register.</td></tr>"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          body {{
            font-family: Arial, Helvetica, sans-serif;
            color: #0f172a;
            margin: 24px;
          }}
          h1 {{
            color: #0f172a;
            font-size: 24px;
            margin-bottom: 8px;
          }}
          h2 {{
            font-size: 16px;
            margin-top: 24px;
            margin-bottom: 8px;
            color: #1d4ed8;
          }}
          .subtitle {{
            color: #475569;
            margin-bottom: 18px;
          }}
          .summary-grid {{
            width: 100%;
            border-spacing: 12px;
            margin-bottom: 16px;
          }}
          .summary-card {{
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 12px;
            background: #f8fafc;
          }}
          .summary-label {{
            font-size: 11px;
            text-transform: uppercase;
            color: #64748b;
          }}
          .summary-value {{
            font-size: 22px;
            font-weight: bold;
            color: #0f172a;
          }}
          table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 8px;
          }}
          th {{
            background: #1d4ed8;
            color: #ffffff;
            font-size: 12px;
            text-align: left;
            padding: 8px;
          }}
          td {{
            border: 1px solid #cbd5e1;
            padding: 8px;
            font-size: 11px;
          }}
        </style>
      </head>
      <body>
        <h1>Cyber Risk Register Export</h1>
        <div class="subtitle">
          Generated from the Cyber Risk Assessment Tool on
          {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
        <table class="summary-grid">
          <tr>
            <td class="summary-card">
              <div class="summary-label">Total risks</div>
              <div class="summary-value">{summary["total"]}</div>
            </td>
            <td class="summary-card">
              <div class="summary-label">Critical risks</div>
              <div class="summary-value">{summary["critical"]}</div>
            </td>
            <td class="summary-card">
              <div class="summary-label">High risks</div>
              <div class="summary-value">{summary["high"]}</div>
            </td>
            <td class="summary-card">
              <div class="summary-label">Average residual</div>
              <div class="summary-value">{summary["average_residual_score"]}</div>
            </td>
          </tr>
        </table>
        <h2>Risk Register</h2>
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Owner</th>
              <th>Residual</th>
              <th>Level</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {table_html}
          </tbody>
        </table>
      </body>
    </html>
    """


def _cell_reference(row_index: int, column_index: int) -> str:
    return f"{_column_name(column_index)}{row_index}"


def _column_name(index: int) -> str:
    result = ""
    current = index
    while current > 0:
        current, remainder = divmod(current - 1, 26)
        result = chr(65 + remainder) + result
    return result


def _escape_xml(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _cell_xml(row_index: int, column_index: int, value: str | int | float, style: int = 0) -> str:
    reference = _cell_reference(row_index, column_index)
    style_attr = f' s="{style}"' if style else ""
    if isinstance(value, bool):
        return f'<c r="{reference}" t="b"{style_attr}><v>{1 if value else 0}</v></c>'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{reference}" t="n"{style_attr}><v>{value}</v></c>'
    return (
        f'<c r="{reference}" t="inlineStr"{style_attr}>'
        f"<is><t>{_escape_xml(str(value))}</t></is></c>"
    )


def _worksheet_xml(
    sheet_name: str,
    rows: list[list[str | int | float]],
    header_row: int,
    title: str | None,
    widths: list[int],
    freeze_top: bool,
    auto_filter: bool,
) -> str:
    rendered_rows: list[str] = []
    current_row_index = 1

    if title:
        rendered_rows.append(
            f'<row r="{current_row_index}">{_cell_xml(current_row_index, 1, title, style=2)}</row>'
        )
        current_row_index += 1

    for row_offset, row in enumerate(rows, start=current_row_index):
        cells = []
        for column_index, value in enumerate(row, start=1):
            style = 1 if row_offset == header_row else 0
            cells.append(_cell_xml(row_offset, column_index, value, style=style))
        rendered_rows.append(f'<row r="{row_offset}">{"".join(cells)}</row>')

    row_count = current_row_index - 1 + len(rows)
    column_count = max((len(row) for row in rows), default=1)
    dimension = f"A1:{_column_name(column_count)}{max(1, row_count)}"
    cols = "".join(
        f'<col min="{index}" max="{index}" width="{width}" customWidth="1"/>'
        for index, width in enumerate(widths, start=1)
    )
    pane = ""
    selection = ""
    if freeze_top:
        pane = '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        selection = '<selection pane="bottomLeft" activeCell="A2" sqref="A2"/>'

    auto_filter_xml = ""
    if auto_filter and row_count >= 1:
        auto_filter_xml = f'<autoFilter ref="A1:{_column_name(column_count)}{row_count}"/>'

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="{dimension}"/>'
        '<sheetViews><sheetView workbookViewId="0">'
        f"{pane}{selection}"
        "</sheetView></sheetViews>"
        f"<cols>{cols}</cols>"
        f'<sheetData>{"".join(rendered_rows)}</sheetData>'
        f"{auto_filter_xml}"
        "</worksheet>"
    )


def _content_types_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""


def _rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


def _doc_props_app_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Cyber Risk Assessment Tool</Application>
</Properties>
"""


def _doc_props_core_xml() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Cyber Risk Register Export</dc:title>
  <dc:creator>Cyber Risk Assessment Tool</dc:creator>
  <cp:lastModifiedBy>Cyber Risk Assessment Tool</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{timestamp}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{timestamp}</dcterms:modified>
</cp:coreProperties>
"""


def _workbook_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Summary" sheetId="1" r:id="rId1"/>
    <sheet name="Risk Register" sheetId="2" r:id="rId2"/>
  </sheets>
</workbook>
"""


def _workbook_rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""


def _styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font>
      <sz val="11"/>
      <name val="Calibri"/>
    </font>
    <font>
      <b/>
      <sz val="11"/>
      <name val="Calibri"/>
    </font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill>
      <patternFill patternType="solid">
        <fgColor rgb="FF1D4ED8"/>
        <bgColor indexed="64"/>
      </patternFill>
    </fill>
  </fills>
  <borders count="1">
    <border><left/><right/><top/><bottom/><diagonal/></border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1">
      <alignment horizontal="center"/>
    </xf>
    <xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
  </cellXfs>
</styleSheet>
"""
