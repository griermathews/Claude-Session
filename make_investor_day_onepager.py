from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL

doc = Document()

# ── Page setup: tight margins, single page ────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Inches(0.55)
section.bottom_margin = Inches(0.55)
section.left_margin   = Inches(0.65)
section.right_margin  = Inches(0.65)

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY    = RGBColor(0x1A, 0x52, 0x76)
TEAL    = RGBColor(0x11, 0x72, 0x7F)
RED     = RGBColor(0xC0, 0x39, 0x2B)
GOLD    = RGBColor(0xD4, 0xAC, 0x0D)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
LGREY   = RGBColor(0xF2, 0xF3, 0xF4)
GREY    = RGBColor(0x55, 0x55, 0x55)
BLACK   = RGBColor(0x17, 0x17, 0x17)

def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)

def set_cell_border(cell, sides=("top","bottom","left","right"),
                    color="AAAAAA", sz="4"):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side in sides:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"),   "single")
        el.set(qn("w:sz"),    sz)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        tcBorders.append(el)
    tcPr.append(tcBorders)

def no_space(p):
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)

def cell_para(cell, text, size=9, color=BLACK, bold=False, italic=False,
              align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=0):
    p = cell.paragraphs[0] if cell.paragraphs else cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold; r.italic = italic
    r.font.color.rgb = color
    return p

def add_cell_line(cell, text, size=9, color=BLACK, bold=False, italic=False,
                  align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.add_paragraph()
    p.alignment = align
    no_space(p)
    r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    r.font.color.rgb = color
    return p

def remove_table_borders(table):
    tbl  = table._tbl
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)
    tblBorders = OxmlElement("w:tblBorders")
    for side in ("top","left","bottom","right","insideH","insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "none")
        tblBorders.append(el)
    tblPr.append(tblBorders)

def set_col_width(table, col_idx, width_inches):
    for row in table.rows:
        row.cells[col_idx].width = Inches(width_inches)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER BAR
# ══════════════════════════════════════════════════════════════════════════════
hdr = doc.add_table(rows=1, cols=2)
remove_table_borders(hdr)
hdr.alignment = WD_TABLE_ALIGNMENT.CENTER

cl = hdr.rows[0].cells[0]
cr = hdr.rows[0].cells[1]
set_cell_bg(cl, "1A5276")
set_cell_bg(cr, "1A5276")
cl.width = Inches(4.6)
cr.width = Inches(2.9)

cell_para(cl, "MERIDIAN TECHNOLOGIES  (NASDAQ: MRDN)",
          size=8, color=WHITE, bold=True, space_before=5, space_after=1)
add_cell_line(cl, "Investor Day  —  March 11, 2026", size=8, color=RGBColor(0xAE,0xD6,0xF1))

cell_para(cr, "CONFIDENTIAL  |  Forward-looking statements apply",
          size=7, color=RGBColor(0xAE,0xD6,0xF1), italic=True,
          align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=5, space_after=1)
add_cell_line(cr, "Catherine Park, President & CEO",
              size=8, color=WHITE, align=WD_ALIGN_PARAGRAPH.RIGHT)

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ══════════════════════════════════════════════════════════════════════════════
# HEADLINE
# ══════════════════════════════════════════════════════════════════════════════
hl = doc.add_table(rows=1, cols=1)
remove_table_borders(hl)
hl.alignment = WD_TABLE_ALIGNMENT.CENTER
c = hl.rows[0].cells[0]
set_cell_bg(c, "EAF4FB")
set_cell_border(c, sides=("left",), color="1A5276", sz="12")
c.width = Inches(7.5)

p = c.paragraphs[0]
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after  = Pt(6)
p.paragraph_format.left_indent  = Inches(0.12)
r = p.add_run(
    "Meridian is the agentic work platform that regulated enterprises trust — "
    "the only place where your agents have a full audit trail."
)
r.bold = True; r.font.size = Pt(12)
r.font.color.rgb = NAVY

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ══════════════════════════════════════════════════════════════════════════════
# THREE-COLUMN BODY
# ══════════════════════════════════════════════════════════════════════════════
body = doc.add_table(rows=1, cols=3)
remove_table_borders(body)
body.alignment = WD_TABLE_ALIGNMENT.CENTER

W = 2.43
for i in range(3):
    body.rows[0].cells[i].width = Inches(W)

c1, c2, c3 = body.rows[0].cells

# helper: section header inside a cell
def col_header(cell, text, bg="1A5276", fg=WHITE):
    set_cell_bg(cell, bg)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(3)
    p.paragraph_format.left_indent  = Inches(0.08)
    r = p.add_run(text.upper())
    r.bold = True; r.font.size = Pt(8)
    r.font.color.rgb = fg

def col_body(cell, lines):
    """lines: list of (text, bold, italic, size, color)"""
    first = True
    for (text, bold, italic, size, color) in lines:
        if first:
            p = cell.add_paragraph()
            first = False
        else:
            p = cell.add_paragraph()
        no_space(p)
        p.paragraph_format.left_indent  = Inches(0.08)
        p.paragraph_format.right_indent = Inches(0.06)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after  = Pt(1)
        r = p.add_run(text)
        r.bold = bold; r.italic = italic; r.font.size = Pt(size)
        r.font.color.rgb = color

# ── Column 1: Where we are ────────────────────────────────────────────────────
col_header(c1, "Where we are")
col_body(c1, [
    ("FY 2025 results", True, False, 8.5, NAVY),
    ("", False, False, 4, GREY),
    ("Revenue:  $400M  (+11% YoY)", False, False, 8.5, BLACK),
    ("ARR:  $413M  (+10% YoY)", False, False, 8.5, BLACK),
    ("Op. margin:  12.4%", False, False, 8.5, BLACK),
    ("FCF margin:  17.8%", False, False, 8.5, BLACK),
    ("Cash + investments:  $506M", False, False, 8.5, BLACK),
    ("Debt:  $0", False, False, 8.5, BLACK),
    ("", False, False, 3, GREY),
    ("Segment ARR mix", True, False, 8.5, NAVY),
    ("", False, False, 4, GREY),
    ("Enterprise  $167M  +21% YoY  NRR 125%", False, False, 8.5, BLACK),
    ("Mid-market  $194M  +6% YoY  NRR 102%", False, False, 8.5, BLACK),
    ("SMB  $52M  –23% YoY  NRR 84%", False, False, 8.5, BLACK),
    ("", False, False, 3, GREY),
    ("AI Copilot (first full year)", True, False, 8.5, NAVY),
    ("", False, False, 4, GREY),
    ("710 paying seats at year-end", False, False, 8.5, BLACK),
    ("44% attach on Q4 enterprise renewals", False, False, 8.5, BLACK),
    ("$3.5M ARR contribution", False, False, 8.5, BLACK),
    ("", False, False, 3, GREY),
    ("Growth has decelerated four years running.", False, True, 8, RED),
    ("Margins have expanded four years running.", False, True, 8, RED),
    ("We are choosing growth.", False, True, 8.5, RED),
])

# ── Column 2: Strategy ────────────────────────────────────────────────────────
col_header(c2, "The three-year strategy")
col_body(c2, [
    ("One positioning sentence", True, False, 8.5, NAVY),
    ("", False, False, 4, GREY),
    ("We are not a PM tool with AI.", False, True, 8.5, BLACK),
    ("We are the platform on which enterprise", False, True, 8.5, BLACK),
    ("agents run — with the audit trail that", False, True, 8.5, BLACK),
    ("Asana, Monday, and Atlassian cannot offer.", False, True, 8.5, BLACK),
    ("", False, False, 3, GREY),
    ("Pillar 1 — Enterprise agent governance", True, False, 8.5, NAVY),
    ("", False, False, 3, GREY),
    ("Ship enterprise governance suite Q1 2026:", False, False, 8.5, BLACK),
    ("agent audit logs, role-based permissions,", False, False, 8.5, BLACK),
    ("model selection, EU data residency.", False, False, 8.5, BLACK),
    ("This is the moat. No competitor has built it.", False, False, 8.5, BLACK),
    ("", False, False, 3, GREY),
    ("Pillar 2 — Agent platform & pricing", True, False, 8.5, NAVY),
    ("", False, False, 3, GREY),
    ("Agent builder GA Q2 2026 (Helio team).", False, False, 8.5, BLACK),
    ("Consumption pricing launched H2 2026:", False, False, 8.5, BLACK),
    ("per-seat for PM, per-action for agents.", False, False, 8.5, BLACK),
    ("Model-neutral: no single-lab dependency.", False, False, 8.5, BLACK),
    ("", False, False, 3, GREY),
    ("Pillar 3 — Enterprise expansion", True, False, 8.5, NAVY),
    ("", False, False, 3, GREY),
    ("Target: 250 enterprise logos by end 2027.", False, False, 8.5, BLACK),
    ("GxP-validated environment Q4 2026.", False, False, 8.5, BLACK),
    ("Tier 1 SI partnership signed H1 2026.", False, False, 8.5, BLACK),
    ("Second AI-native acquisition in H2 2026.", False, False, 8.5, BLACK),
    ("EMEA investment committed in 2026 plan.", False, False, 8.5, BLACK),
])

# ── Column 3: Targets & capital ───────────────────────────────────────────────
col_header(c3, "Targets & capital allocation")
col_body(c3, [
    ("2026 guidance (reaffirmed)", True, False, 8.5, NAVY),
    ("", False, False, 4, GREY),
    ("Revenue:  $440–455M  (+10–14%)", False, False, 8.5, BLACK),
    ("Op. margin:  14–15%", False, False, 8.5, BLACK),
    ("FCF:  ~$75M", False, False, 8.5, BLACK),
    ("", False, False, 3, GREY),
    ("2028 targets", True, False, 8.5, NAVY),
    ("", False, False, 4, GREY),
    ("Revenue:  $750–900M", False, False, 8.5, BLACK),
    ("ARR growth:  18–25% by 2027", False, False, 8.5, BLACK),
    ("Op. margin:  16–18%", False, False, 8.5, BLACK),
    ("Copilot / agent ARR:  $80–150M", False, False, 8.5, BLACK),
    ("Enterprise NRR:  sustained >120%", False, False, 8.5, BLACK),
    ("", False, False, 3, GREY),
    ("The range is intentional.", False, True, 8, GREY),
    ("Upside requires consumption pricing", False, True, 8, GREY),
    ("adoption ahead of plan.", False, True, 8, GREY),
    ("", False, False, 3, GREY),
    ("Capital allocation priority", True, False, 8.5, NAVY),
    ("", False, False, 4, GREY),
    ("$250M capacity for AI M&A in 2026", False, False, 8.5, BLACK),
    ("$200M revolver undrawn", False, False, 8.5, BLACK),
    ("Buyback resumes Q2 2026 ($140M auth.)", False, False, 8.5, BLACK),
    ("", False, False, 3, GREY),
    ("3 metrics we will report quarterly", True, False, 8.5, NAVY),
    ("", False, False, 4, GREY),
    ("1. Copilot attach rate on enterprise renewals", False, False, 8.5, BLACK),
    ("   (target: >50% by Q4 2026)", False, False, 8, GREY),
    ("2. Agent ARR as % of total ARR", False, False, 8.5, BLACK),
    ("   (target: >10% by Q4 2027)", False, False, 8, GREY),
    ("3. Enterprise NRR", False, False, 8.5, BLACK),
    ("   (floor: 120%)", False, False, 8, GREY),
])

doc.add_paragraph().paragraph_format.space_after = Pt(3)

# ══════════════════════════════════════════════════════════════════════════════
# COMPETITIVE POSITIONING ROW
# ══════════════════════════════════════════════════════════════════════════════
pos = doc.add_table(rows=2, cols=5)
remove_table_borders(pos)
pos.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = ["", "Asana", "Monday", "Smartsheet", "Atlassian"]
bg_map  = ["1A5276", "D5D8DC", "D5D8DC", "D5D8DC", "D5D8DC"]
fg_map  = ["FFFFFF", "171717", "171717", "171717", "171717"]

for i, (h, bg, fg) in enumerate(zip(headers, bg_map, fg_map)):
    c = pos.rows[0].cells[i]
    c.width = Inches(1.5)
    set_cell_bg(c, bg)
    p = c.paragraphs[0]
    no_space(p)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.left_indent  = Inches(0.06)
    r = p.add_run(h if h else "Meridian vs. peers")
    r.bold = True; r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(*[int(fg[i:i+2],16) for i in (0,2,4)]) if fg != WHITE else WHITE

rows_data = [
    ("Agentic posture",       "Agent OS (strong)",    "Work OS + AI (broad)",  "PM + AI (conservative)", "Rovo (most committed)"),
    ("Enterprise governance", "Weak",                  "Weak",                  "Moderate",               "Dev-only"),
    ("Regulated verticals",   "Limited",               "None",                  "Limited",                "Dev/IT only"),
    ("Consumption pricing",   "No",                    "No",                    "No",                     "Yes — Rovo"),
    ("Meridian's edge",       "Governance moat",       "Governance + verticals","Earlier agentic pivot",  "Non-dev verticals"),
]

# highlight row
for row_data in rows_data:
    row = pos.add_row()
    for i, val in enumerate(row_data):
        c = row.cells[i]
        c.width = Inches(1.5)
        bg = "EAF4FB" if i == 0 else "FFFFFF"
        set_cell_bg(c, bg)
        p = c.paragraphs[0]
        no_space(p)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after  = Pt(1)
        p.paragraph_format.left_indent  = Inches(0.06)
        r = p.add_run(val)
        r.font.size = Pt(7.8)
        r.bold = (i == 0)
        r.font.color.rgb = NAVY if i == 0 else BLACK

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
ftr = doc.add_table(rows=1, cols=1)
remove_table_borders(ftr)
ftr.alignment = WD_TABLE_ALIGNMENT.CENTER
fc = ftr.rows[0].cells[0]
set_cell_bg(fc, "1A5276")
fc.width = Inches(7.5)

fp = fc.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fp.paragraph_format.space_before = Pt(3)
fp.paragraph_format.space_after  = Pt(3)
fr = fp.add_run(
    "Investor Day webcast: investors.meridiantech.com  |  March 11, 2026, 9:00 AM ET  |  "
    "IR contact: Tara Linwood  ir@meridiantech.com"
)
fr.font.size = Pt(7.5)
fr.font.color.rgb = RGBColor(0xAE, 0xD6, 0xF1)

doc.save("investor_day_onepager.docx")
print("Saved investor_day_onepager.docx")
