from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

section = doc.sections[0]
section.top_margin    = Inches(0.85)
section.bottom_margin = Inches(0.85)
section.left_margin   = Inches(1.0)
section.right_margin  = Inches(1.0)

NAVY  = RGBColor(0x1A, 0x52, 0x76)
RED   = RGBColor(0xC0, 0x39, 0x2B)
GREEN = RGBColor(0x1E, 0x84, 0x49)
GREY  = RGBColor(0x55, 0x55, 0x55)
BLACK = RGBColor(0x00, 0x00, 0x00)

def set_color(run, rgb):
    run.font.color.rgb = rgb

def divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "BBBBBB")
    pBdr.append(bottom)
    pPr.append(pBdr)

def para(text, size=10.5, color=GREY, bold=False, italic=False,
         space_before=3, space_after=3, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold; r.italic = italic
    set_color(r, color)
    return p

def label(text, color=NAVY):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(9)
    set_color(r, color)
    return p

def response_line(prefix, text, prefix_color=GREEN):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.left_indent  = Inches(0.25)
    rb = p.add_run(prefix + "  ")
    rb.bold = True; rb.font.size = Pt(10.5)
    set_color(rb, prefix_color)
    rt = p.add_run(text)
    rt.font.size = Pt(10.5)
    set_color(rt, RGBColor(0x1A, 0x1A, 0x1A))
    return p

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
para("MERIDIAN TECHNOLOGIES", size=9, color=GREY, bold=False,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=1)
para("Board Strategic Review — Anticipated Counter-Questions",
     size=9, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=1)
para("Prepared for CEO Catherine Park  |  Confidential",
     size=9, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
divider()

para(
    "The ask — advance Copilot consumption pricing to a Q1 2026 strategic priority — "
    "will draw resistance from three directions. The script below gives you the likely "
    "exact objection, the frame behind it, and a disciplined response.",
    size=10, color=GREY, italic=True, space_before=8, space_after=8
)
divider()

# ═══════════════════════════════════════════════════════════════════════════════
# Q1
# ═══════════════════════════════════════════════════════════════════════════════
para("QUESTION 1", size=10, color=NAVY, bold=True, space_before=10, space_after=2)
para(
    '"The per-seat model is working. You hit 44% attach, you beat your own seat target, '
    'and enterprise NRR is 125%. Why complicate a working model mid-flight?"',
    size=11.5, color=RED, bold=True, italic=True, space_before=2, space_after=6
)

label("WHY THIS QUESTION GETS ASKED")
para(
    "This is a legitimate defense of the status quo from a director who reads the Q4 "
    "numbers as a green light. The subtext is: you're new, the metrics are improving, "
    "don't break something that's working.",
    size=10, color=GREY, space_before=2, space_after=6
)

label("YOUR RESPONSE", color=GREEN)
response_line(
    "Acknowledge:",
    "You're right that the early signals are better than we feared. 44% attach and "
    "710 seats ahead of target is a real proof point, and I don't want to understate it."
)
response_line(
    "Reframe:",
    "The question isn't whether per-seat is working now — it's whether per-seat can "
    "get us to the growth rate we need. The math says it can't. Our enterprise seat "
    "TAM is roughly 70,000 seats. At $40 per seat that's a $34M ARR ceiling — even "
    "at 100% penetration. We need $29M of Copilot ARR just to hit 15% growth in 2026. "
    "Per-seat pricing structurally cannot close that gap."
)
response_line(
    "Evidence:",
    "Every AI-native SaaS company that has tried to monetise agentic usage on per-seat "
    "pricing has eventually moved to consumption. Salesforce Agentforce, Microsoft "
    "Copilot 365, ServiceNow Now Assist — all consumption or hybrid. The question is "
    "not if we move, it is whether we move before or after our competitors force our hand."
)
response_line(
    "Close:",
    "I am not asking to flip the switch today. I am asking for a board-ready proposal "
    "by March that gives us the option. We keep per-seat for customers where it works "
    "and add a consumption track for agentic usage. Optionality has value. A six-month "
    "delay has a cost."
)

divider()

# ═══════════════════════════════════════════════════════════════════════════════
# Q2
# ═══════════════════════════════════════════════════════════════════════════════
para("QUESTION 2", size=10, color=NAVY, bold=True, space_before=10, space_after=2)
para(
    '"Six of your twelve roadmap items slipped last year. Your own CPO says engineering '
    'net adds will be 25, not 80. You\'re already behind — why are you adding a pricing '
    'model overhaul to an overstretched team?"',
    size=11.5, color=RED, bold=True, italic=True, space_before=2, space_after=6
)

label("WHY THIS QUESTION GETS ASKED")
para(
    "This is the execution-risk pushback. The director has read the product roadmap "
    "memo carefully. The subtext: you're asking us to trust a team that has a "
    "documented slip problem with something even harder.",
    size=10, color=GREY, space_before=2, space_after=6
)

label("YOUR RESPONSE", color=GREEN)
response_line(
    "Acknowledge:",
    "The slip rate is real, and I own it. Six of twelve items missing by at least a "
    "quarter is not acceptable as a steady state. I have been direct about that with "
    "the CPO."
)
response_line(
    "Reframe:",
    "A pricing model change is not an engineering project — it is a go-to-market and "
    "finance design project. The work I am asking CFO, CRO, and CPO to do by March "
    "is a proposal: what does the model look like, what does implementation require, "
    "and what is the revenue forecast under different scenarios. That is six weeks of "
    "executive alignment work, not six months of engineering."
)
response_line(
    "Evidence:",
    "The roadmap memo explicitly flags that the consumption pricing decision should be "
    "jointly owned by CFO and CRO — it is not a product decision. I am following "
    "that recommendation. The engineering lift, if we decide to proceed, comes later "
    "and gets scoped in the March proposal."
)
response_line(
    "Close:",
    "I hear the concern. If the March proposal comes back and says the implementation "
    "risk is too high given current capacity, we will say so and the board will "
    "decide. What I don't want is to arrive at Investor Day on March 11th without "
    "having done that analysis. The cost of the analysis is low. The cost of not "
    "having it is high."
)

divider()

# ═══════════════════════════════════════════════════════════════════════════════
# Q3
# ═══════════════════════════════════════════════════════════════════════════════
para("QUESTION 3", size=10, color=NAVY, bold=True, space_before=10, space_after=2)
para(
    (
        '"You\'ve described a structural deceleration, a competitive threat from four '
        'directions, and a talent retention risk. Your one ask is to reprice an '
        'add-on product. Is that really the scale of response this situation warrants?"'
    ),
    size=11.5, color=RED, bold=True, italic=True, space_before=2, space_after=6
)

label("WHY THIS QUESTION GETS ASKED")
para(
    "This is the hardest question. It comes from the most engaged director — someone "
    "who understood everything you just said and is worried you are underreacting. "
    "The subtext: should we be talking about a transformative acquisition, a "
    "take-private, or a fundamental strategic pivot?",
    size=10, color=GREY, space_before=2, space_after=6
)

label("YOUR RESPONSE", color=GREEN)
response_line(
    "Acknowledge:",
    "That question is exactly right, and I want to sit with it for a moment rather "
    "than deflect. The situation does warrant a response at scale. I agree."
)
response_line(
    "Reframe:",
    "The reason I am bringing one specific ask today — rather than a full strategic "
    "plan — is that I promised you a rigorous plan, not a fast one. The board "
    "authorised me to deliver that plan by Q1 2026 and I will. What I am doing "
    "today is identifying the single decision that has the highest time-sensitivity: "
    "consumption pricing is a Q3 roadmap item that needs executive alignment starting "
    "now if it is going to be ready for Investor Day. Everything else — M&A targets, "
    "the mid-market defence, the EMEA investment decision — is in the plan."
)
response_line(
    "Evidence:",
    "I have two acquisition targets in early diligence. I have a working view on "
    "mid-market. I have a position on EMEA. I am not bringing those today because "
    "they are not ready for a board decision and I will not waste your time with "
    "incomplete analysis. Consumption pricing is the one item that is ready — and "
    "where a six-week delay has a direct cost."
)
response_line(
    "Close:",
    "If your question is really: Catherine, do you understand the gravity of what "
    "you are facing? — yes. I do. The March plan will reflect that. Today I am "
    "asking for the one thing I need from this room right now, so I can walk out "
    "of here and execute."
)

divider()

# ── Footer ────────────────────────────────────────────────────────────────────
para(
    "Preparation note: for each question, the structure is Acknowledge → Reframe → Evidence → Close. "
    "Do not skip Acknowledge — board members who feel dismissed become adversarial. "
    "Do not linger in Acknowledge — it reads as defensive. Ten seconds, then move.",
    size=8.5, color=GREY, italic=True, space_before=8, space_after=4
)

doc.save("board_counter_questions_script.docx")
print("Saved board_counter_questions_script.docx")
