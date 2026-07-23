#!/usr/bin/env python3
"""Generate ATS-friendly, professionally styled PDF resume from ganesh_resume_2026.md"""

import re
from pathlib import Path

from fpdf import FPDF

MD_FILE = Path(__file__).parent / "ganesh_resume_2026.md"
PDF_FILE = Path(__file__).parent / "ganesh_resume_2026.pdf"

# Typography & colors
FONT = "Calibri"
FONT_FALLBACK = "Helvetica"
NAME_SIZE = 22
TITLE_SIZE = 11
CONTACT_SIZE = 9.5
SECTION_SIZE = 11
JOB_TITLE_SIZE = 10.5
JOB_META_SIZE = 9.5
BODY_SIZE = 10
SKILL_SIZE = 9.75
PROJECT_TITLE_SIZE = 10

LINE_BODY = 5.5
LINE_SKILL = 5.2
LINE_TIGHT = 4.8

COLOR_NAME = (20, 55, 95)       # deep navy
COLOR_TITLE = (70, 70, 70)      # soft gray
COLOR_CONTACT = (90, 90, 90)
COLOR_SECTION = (30, 30, 30)
COLOR_BODY = (35, 35, 35)
COLOR_META = (100, 100, 100)
COLOR_RULE = (190, 190, 190)


def clean(text: str) -> str:
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2012", "-")
    text = text.replace("\u2192", "->").replace("\u2019", "'").replace("\u2018", "'")
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = text.replace("`", "")
    return text.strip()


def register_fonts(pdf: FPDF) -> str:
    """Register Calibri from Windows if available; otherwise use Helvetica."""
    win_fonts = Path(r"C:\Windows\Fonts")
    candidates = {
        "": win_fonts / "calibri.ttf",
        "B": win_fonts / "calibrib.ttf",
        "I": win_fonts / "calibrii.ttf",
        "BI": win_fonts / "calibriz.ttf",
    }
    if all(path.exists() for path in candidates.values()):
        for style, path in candidates.items():
            pdf.add_font(FONT, style, str(path))
        return FONT
    return FONT_FALLBACK


class ResumePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.font = register_fonts(self)
        self.set_auto_page_break(auto=True, margin=16)
        self.set_margins(18, 14, 18)

    def _rule(self, gap_after: float = 3.5):
        self.ln(1.2)
        y = self.get_y()
        self.set_draw_color(*COLOR_RULE)
        self.set_line_width(0.25)
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(gap_after)

    def header_block(self, name: str, title: str, contact: str, links: str = ""):
        self.set_font(self.font, "B", NAME_SIZE)
        self.set_text_color(*COLOR_NAME)
        self.cell(0, 10, clean(name), new_x="LMARGIN", new_y="NEXT")

        self.ln(1)
        self.set_font(self.font, "", TITLE_SIZE)
        self.set_text_color(*COLOR_TITLE)
        self.cell(0, 6, clean(title), new_x="LMARGIN", new_y="NEXT")

        self.ln(0.5)
        self.set_font(self.font, "", CONTACT_SIZE)
        self.set_text_color(*COLOR_CONTACT)
        self.cell(0, 5.5, clean(contact), new_x="LMARGIN", new_y="NEXT")
        if links:
            self.set_font(self.font, "", 8.5)
            self.multi_cell(0, 4.5, clean(links))
        self._rule(gap_after=4)

    def section_heading(self, title: str):
        self.ln(3)
        self.set_x(self.l_margin)
        self.set_font(self.font, "B", SECTION_SIZE)
        self.set_text_color(*COLOR_SECTION)
        self.cell(0, 6, clean(title).upper(), new_x="LMARGIN", new_y="NEXT")
        self._rule(gap_after=3)

    def body(self, text: str, size: float = BODY_SIZE, line: float = LINE_BODY):
        self.set_x(self.l_margin)
        self.set_font(self.font, "", size)
        self.set_text_color(*COLOR_BODY)
        self.multi_cell(0, line, clean(text))

    def skill_line(self, text: str):
        self.set_x(self.l_margin)
        self.set_font(self.font, "", SKILL_SIZE)
        self.set_text_color(*COLOR_BODY)
        self.multi_cell(0, LINE_SKILL, clean(text))
        self.ln(0.8)

    def job_block(self, title: str, meta: str, bullets: list[str], compact: bool = False):
        gap = 1.5 if compact else 2.5
        self.ln(gap)
        self.set_x(self.l_margin)
        self.set_font(self.font, "B", JOB_TITLE_SIZE if not compact else 10)
        self.set_text_color(*COLOR_SECTION)
        self.multi_cell(0, LINE_TIGHT + 0.3, clean(title))

        if meta:
            self.ln(0.3)
            self.set_x(self.l_margin)
            self.set_font(self.font, "I", JOB_META_SIZE)
            self.set_text_color(*COLOR_META)
            self.multi_cell(0, LINE_TIGHT, clean(meta))

        if bullets:
            self.ln(0.8 if compact else 1.2)
            for bullet in bullets:
                self.bullet(bullet, compact=compact)

    def bullet(self, text: str, compact: bool = False):
        self.set_x(self.l_margin + 2)
        self.set_font(self.font, "", BODY_SIZE if not compact else 9.75)
        self.set_text_color(*COLOR_BODY)
        width = self.w - self.l_margin - self.r_margin - 2
        self.multi_cell(width, LINE_BODY if not compact else 5.0, "-  " + clean(text))
        self.ln(0.6 if compact else 0.9)

    def project_block(self, title: str, lines: list[str]):
        self.ln(1.5)
        self.set_x(self.l_margin)
        self.set_font(self.font, "B", PROJECT_TITLE_SIZE)
        self.set_text_color(*COLOR_SECTION)
        self.multi_cell(0, LINE_TIGHT + 0.2, clean(title))
        self.ln(0.5)
        for line in lines:
            self.body(line, size=SKILL_SIZE, line=LINE_SKILL)
            self.ln(0.3)


def parse_markdown(content: str) -> dict:
    lines = content.splitlines()
    data = {
        "name": "",
        "title": "",
        "contact": "",
        "links": "",
        "summary": "",
        "skills": [],
        "jobs": [],
        "projects": [],
        "education": [],
    }

    section = None
    current_job = None
    current_project = None
    buffer = []

    section_map = {
        "## SUMMARY": "summary",
        "## PROFESSIONAL SUMMARY": "summary",
        "## SKILLS": "skills",
        "## TECHNICAL SKILLS": "skills",
        "## EXPERIENCE": "experience",
        "## PROFESSIONAL EXPERIENCE": "experience",
        "## PROJECTS": "projects",
        "## SELECTED PROJECTS": "projects",
        "## EDUCATION": "education",
    }

    def flush_job():
        nonlocal current_job
        if current_job:
            data["jobs"].append(current_job)
            current_job = None

    def flush_project():
        nonlocal current_project
        if current_project:
            data["projects"].append(current_project)
            current_project = None

    for line in lines:
        stripped = line.strip()
        upper = stripped.upper()

        if stripped.startswith("# ") and not data["name"]:
            data["name"] = stripped[2:].strip()
            continue

        if section is None and data.get("contact") and stripped and not stripped.startswith("#") and not stripped.startswith("**") and not data.get("links"):
            data["links"] = clean(re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", stripped))
            continue

        if section is None and stripped.startswith("**") and "|" in stripped:
            parts = [p.strip() for p in stripped.split("|")]
            data["title"] = parts[0].strip("*")
            data["contact"] = "  |  ".join(parts[1:])
            continue

        if stripped.startswith("## "):
            key = upper.split("\n")[0]
            if key in section_map:
                if section == "summary" and buffer:
                    data["summary"] = " ".join(buffer)
                    buffer = []
                flush_job()
                flush_project()
                section = section_map[key]
            continue

        if stripped == "---":
            if section == "experience":
                flush_job()
            continue

        if section == "summary" and stripped:
            buffer.append(stripped)
            continue

        if section == "skills" and stripped:
            data["skills"].append(stripped)
            continue

        if section == "experience":
            if stripped.startswith("**") and " — " in stripped:
                flush_job()
                current_job = {"title": stripped, "meta": "", "bullets": []}
                continue
            if stripped.startswith("### "):
                flush_job()
                current_job = {"title": stripped[4:], "meta": "", "bullets": []}
                continue
            if current_job and stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
                current_job["meta"] = stripped.strip("*")
                continue
            if current_job and stripped.startswith("**") and stripped.endswith("**"):
                current_job["meta"] = stripped.strip("*")
                continue
            if current_job and stripped.startswith("- "):
                current_job["bullets"].append(stripped[2:])
                continue

        if section == "projects":
            if stripped.startswith("**") and stripped.endswith("**") and " — " not in stripped:
                flush_project()
                current_project = {"title": stripped.strip("*"), "lines": []}
                continue
            if stripped.startswith("### "):
                flush_project()
                current_project = {"title": stripped[4:], "lines": []}
                continue
            if current_project and stripped:
                current_project["lines"].append(stripped)
                continue

        if section == "education" and stripped:
            data["education"].append(stripped)

    if buffer and section == "summary":
        data["summary"] = " ".join(buffer)
    flush_job()
    flush_project()

    return data


def build_pdf(data: dict) -> FPDF:
    pdf = ResumePDF()
    pdf.add_page()

    pdf.header_block(data["name"], data["title"], data["contact"], data.get("links", ""))

    pdf.section_heading("Professional Summary")
    pdf.body(data["summary"])
    pdf.ln(1)

    pdf.section_heading("Technical Skills")
    for skill in data["skills"]:
        pdf.skill_line(skill)

    pdf.section_heading("Professional Experience")
    # Recent roles — full spacing; older roles — compact
    for i, job in enumerate(data["jobs"]):
        compact = i >= 3
        pdf.job_block(job["title"], job["meta"], job["bullets"], compact=compact)

    pdf.section_heading("Selected Projects")
    for project in data["projects"]:
        pdf.project_block(project["title"], project["lines"])

    pdf.section_heading("Education")
    pdf.ln(0.5)
    for line in data["education"]:
        pdf.body(line, size=BODY_SIZE, line=LINE_BODY)
        pdf.ln(0.5)

    return pdf


def main():
    content = MD_FILE.read_text(encoding="utf-8")
    data = parse_markdown(content)
    pdf = build_pdf(data)
    pdf.output(str(PDF_FILE))
    print(f"Generated: {PDF_FILE} ({PDF_FILE.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
