#!/usr/bin/env python3
"""Generate the Dept of Education strategy deck."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# Brand palette
DARK = RGBColor(0x14, 0x53, 0x2d)
GREEN = RGBColor(0x16, 0x65, 0x34)
SKY = RGBColor(0x38, 0xbd, 0xf8)
LIGHT = RGBColor(0xbb, 0xf7, 0xd0)
MINT = RGBColor(0x86, 0xef, 0xac)
WHITE = RGBColor(0xff, 0xff, 0xff)
TEXT = RGBColor(0x1e, 0x29, 0x3b)
MUTED = RGBColor(0x64, 0x74, 0x8b)
CARD = RGBColor(0xf1, 0xf5, 0xf9)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def rect(s, x, y, w, h, color, line=None):
    sp = s.shapes.add_shape(1, x, y, w, h)
    sp.fill.solid()
    sp.fill.fore_color.rgb = color
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(1)
    sp.shadow.inherit = False
    return sp


def text(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=1.0):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    first = True
    for item in runs:
        txt, size, color, bold = item[0], item[1], item[2], item[3]
        bullet = item[4] if len(item) > 4 else False
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.line_spacing = space
        p.space_after = Pt(6)
        r = p.add_run()
        r.text = ("•  " + txt) if bullet else txt
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.bold = bold
        r.font.name = "Calibri"
    return tb


def header(s, kicker, title):
    rect(s, 0, 0, SW, Inches(1.25), DARK)
    rect(s, 0, Inches(1.25), SW, Pt(4), SKY)
    text(s, Inches(0.6), Inches(0.14), Inches(12), Inches(0.4),
         [(kicker, 13, MINT, True)])
    text(s, Inches(0.6), Inches(0.5), Inches(12.1), Inches(0.7),
         [(title, 26, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(0.6), Inches(6.95), Inches(12), Inches(0.4),
         [("Math Competition Readiness Hub  ·  Nationwide Awareness Initiative", 10, MUTED, False)])


def card(s, x, y, w, h, title, lines, accent=GREEN):
    rect(s, x, y, w, h, CARD)
    rect(s, x, y, w, Pt(5), accent)
    runs = [(title, 15, accent, True)]
    for ln in lines:
        runs.append((ln, 12, TEXT, False, True))
    text(s, x + Inches(0.18), y + Inches(0.18), w - Inches(0.36), h - Inches(0.3), runs, space=1.05)


# ---------- Slide 1: Title ----------
s = slide()
rect(s, 0, 0, SW, SH, DARK)
rect(s, 0, Inches(4.55), SW, Pt(5), SKY)
text(s, Inches(0.9), Inches(0.8), Inches(8), Inches(0.5),
     [("STRATEGY DISCUSSION  ·  U.S. DEPARTMENT OF EDUCATION", 15, MINT, True)])
text(s, Inches(0.9), Inches(1.9), Inches(11.5), Inches(2.2),
     [("Expanding Access to", 44, WHITE, True),
      ("Math Competitions", 54, WHITE, True)], space=1.0)
text(s, Inches(0.9), Inches(4.8), Inches(11), Inches(1.0),
     [("A nationwide initiative to raise awareness and participation among "
       "parents, students, and teachers — and strengthen the STEM pipeline from the ground up.", 18, LIGHT, False)], space=1.1)
text(s, Inches(0.9), Inches(6.5), Inches(11.5), Inches(0.6),
     [("Math Competition Readiness Hub   ·   vineetagrwal.github.io/math-dance-pathway", 14, SKY, True)])

# ---------- Slide 2: Executive Summary ----------
s = slide()
header(s, "EXECUTIVE SUMMARY", "The opportunity in one slide")
text(s, Inches(0.6), Inches(1.5), Inches(12.1), Inches(1.0),
     [("Math competitions are one of the most effective, lowest-cost on-ramps to STEM — yet most "
       "families and many schools don't know they exist or assume they're only for a gifted elite. "
       "The result is a vast pool of untapped talent, concentrated in under-resourced communities.", 15, TEXT, False)], space=1.15)
card(s, Inches(0.6), Inches(3.0), Inches(3.9), Inches(3.4), "The gap",
     ["Awareness, not ability, is the binding constraint",
      "Many Title I & rural schools host no contests",
      "Parents lack a clear 'start here' path"], GREEN)
card(s, Inches(4.7), Inches(3.0), Inches(3.9), Inches(3.4), "The solution",
     ["A free, open, static web hub — no cost, no login",
      "Turnkey kit so any teacher can host in ~40 min",
      "Shareable by design to spread school-to-school"], SKY)
card(s, Inches(8.8), Inches(3.0), Inches(3.9), Inches(3.4), "The ask",
     ["Help us reach schools at scale",
      "Co-sponsor a multi-state awareness pilot",
      "Point to existing federal STEM-equity goals"], RGBColor(0xd9,0x77,0x06))

# ---------- Slide 3: The Problem ----------
s = slide()
header(s, "THE PROBLEM", "A nationwide awareness & access gap")
card(s, Inches(0.6), Inches(1.6), Inches(5.9), Inches(2.3), "Awareness gap",
     ["Families don't know contests exist, or think they're elite-only",
      "No single trusted 'where do I start' resource",
      "Teachers unaware they can host with minimal effort"], GREEN)
card(s, Inches(6.8), Inches(1.6), Inches(5.9), Inches(2.3), "Access gap",
     ["Many schools host no contests — so students can't enter",
      "Private coaching costs lock out lower-income families",
      "Rural & Title I schools disproportionately absent"], RGBColor(0xd9,0x77,0x06))
text(s, Inches(0.6), Inches(4.2), Inches(12), Inches(0.5),
     [("Why it persists — a chicken-and-egg cycle:", 16, DARK, True)])
text(s, Inches(0.6), Inches(4.8), Inches(12.1), Inches(1.8),
     [("No champion at the school  →  the school never registers as a test site  →  "
       "students never compete  →  parents never ask  →  no champion emerges. "
       "The cycle breaks only when one informed adult — a parent or teacher — takes the first step. "
       "Our entire strategy is built around making that first step effortless.", 15, TEXT, False)], space=1.2)

# ---------- Slide 4: Why It Matters ----------
s = slide()
header(s, "WHY IT MATTERS", "Competitions strengthen the STEM pipeline & equity")
card(s, Inches(0.6), Inches(1.6), Inches(3.9), Inches(4.7), "Talent pipeline",
     ["Early problem-solving builds durable math confidence",
      "Clear ladder: MOEMS → AMC 8 → AMC 10 → AIME",
      "Feeds the nation's future scientists & engineers",
      "Top universities explicitly value these results"], GREEN)
card(s, Inches(4.7), Inches(1.6), Inches(3.9), Inches(4.7), "Equity",
     ["Free resources level an uneven playing field",
      "Reaches students without pricey tutoring",
      "A single hosting teacher opens doors for ~30 kids",
      "Aligns with federal STEM-access priorities"], SKY)
card(s, Inches(8.8), Inches(1.6), Inches(3.9), Inches(4.7), "School impact",
     ["Low cost (~$75 + $25/10 students for AMC 8)",
      "One ~40-minute session, minimal admin burden",
      "Boosts school STEM culture & recognition",
      "Engages parent & PTA volunteers"], RGBColor(0xd9,0x77,0x06))

# ---------- Slide 5: The Barriers ----------
s = slide()
header(s, "UNDERSTANDING THE AUDIENCE", "Three audiences, three barriers")
rows = [
    ("Audience", "What stops them", "What they need", True),
    ("Parents", "Don't know contests exist; assume elite-only", "A simple start-here path, deadlines, cost clarity", False),
    ("Students", "Intimidated; no peers competing; no practice", "Low-stakes entry + free practice archives", False),
    ("Teachers", "No time; unaware they can host", "A turnkey kit proving it's ~40 minutes", False),
]
y = Inches(1.7)
rh = Inches(1.15)
col = [Inches(0.6), Inches(3.0), Inches(7.3)]
cw = [Inches(2.4), Inches(4.3), Inches(5.4)]
for ri, (a, b, c, hdr) in enumerate(rows):
    yy = y + rh * ri if ri == 0 else y + Inches(0.75) + rh * (ri - 1)
    h = Inches(0.75) if ri == 0 else rh
    bg = DARK if hdr else (CARD if ri % 2 else WHITE)
    for ci, (cx, cwi) in enumerate(zip(col, cw)):
        rect(s, cx, yy, cwi, h, bg, line=RGBColor(0xe2,0xe8,0xf0))
        val = (a, b, c)[ci]
        text(s, cx + Inches(0.15), yy + Inches(0.08), cwi - Inches(0.3), h - Inches(0.16),
             [(val, 13 if not hdr else 13, WHITE if hdr else (DARK if ci == 0 and not hdr else TEXT), hdr or (ci == 0))],
             anchor=MSO_ANCHOR.MIDDLE)
text(s, Inches(0.6), Inches(6.3), Inches(12), Inches(0.6),
     [("Key insight: teachers are the highest-leverage audience — convincing one reaches ~30 families at once.", 15, GREEN, True)])

# ---------- Slide 6: The Equity Gap ----------
s = slide()
header(s, "THE EQUITY DIMENSION", "Who gets left out today")
text(s, Inches(0.6), Inches(1.55), Inches(12.1), Inches(1.3),
     [("Participation today skews toward well-resourced schools and families who already know the system. "
       "The students most likely to benefit from an early STEM signal — in Title I, rural, and immigrant-heavy "
       "communities — are the least likely to have a nearby test site or an informed adult to guide them.", 15, TEXT, False)], space=1.15)
card(s, Inches(0.6), Inches(3.2), Inches(5.9), Inches(3.1), "Barriers that compound",
     ["No host school within reach",
      "Registration must be led by a school employee",
      "Coaching & materials priced out of reach",
      "No local math circle or peer community"], RGBColor(0xd9,0x77,0x06))
card(s, Inches(6.8), Inches(3.2), Inches(5.9), Inches(3.1), "How this initiative closes it",
     ["100% free, no login, mobile-friendly",
      "Kit empowers ANY teacher to become the champion",
      "Links only to free, official practice archives",
      "Step-by-step guide to start a local math circle"], SKY)

# ---------- Slide 7: The Solution ----------
s = slide()
header(s, "THE SOLUTION", "A free Math Competition Readiness Hub")
text(s, Inches(0.6), Inches(1.5), Inches(12.1), Inches(0.9),
     [("A single, static web page — no cost, no accounts, no backend to maintain — that turns a confusing "
       "landscape into a clear, actionable pathway for every audience.", 15, TEXT, False)], space=1.15)
feats = [
    ("3-phase annual playbook", "Register → prepare → compete, on a clear yearly cycle"),
    ("School hosting guide", "Steps + a ready-to-send email template to recruit a manager"),
    ("Contest calendar", "AMC 8, MATHCOUNTS, MOEMS, Kangaroo — with free practice links"),
    ("6→12 university pathway", "From middle-school contests to top STEM universities"),
    ("Math-circle starter", "How parents launch a local peer community"),
    ("Share & spread tools", "One-tap sharing so it travels school-to-school"),
]
x0, y0 = Inches(0.6), Inches(2.7)
cw2, ch2 = Inches(3.9), Inches(1.75)
for i, (t, d) in enumerate(feats):
    cx = x0 + (cw2 + Inches(0.2)) * (i % 3)
    cy = y0 + (ch2 + Inches(0.2)) * (i // 3)
    card(s, cx, cy, cw2, ch2, t, [d], GREEN if i % 2 == 0 else SKY)

# ---------- Slide 8: Strategy ----------
s = slide()
header(s, "STRATEGY", "Teacher-first leverage")
text(s, Inches(0.6), Inches(1.5), Inches(12.1), Inches(0.9),
     [("Each audience spreads it to the next. We prioritize the highest-leverage node first, "
       "then let adoption cascade.", 15, TEXT, False)], space=1.15)
chain = [("1 Teacher", GREEN), ("~30 Families", SKY), ("Students compete", RGBColor(0xd9,0x77,0x06)), ("Word of mouth", DARK)]
x = Inches(0.6)
for i, (label, c) in enumerate(chain):
    rect(s, x, Inches(2.7), Inches(2.7), Inches(1.1), c)
    text(s, x, Inches(2.7), Inches(2.7), Inches(1.1), [(label, 16, WHITE, True)],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < 3:
        text(s, x + Inches(2.7), Inches(2.7), Inches(0.35), Inches(1.1), [("→", 24, MUTED, True)],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x += Inches(3.05)
card(s, Inches(0.6), Inches(4.3), Inches(5.9), Inches(2.0), "Why teacher-first",
     ["One convert unlocks a whole classroom",
      "Schools are trusted messengers to parents",
      "Hosting is cheap and low-effort once understood"], GREEN)
card(s, Inches(6.8), Inches(4.3), Inches(5.9), Inches(2.0), "Making it effortless",
     ["Downloadable one-page hosting kit",
      "Pre-written principal/PTA email template",
      "Printable flyer + QR code for staff rooms"], SKY)

# ---------- Slide 9: Distribution ----------
s = slide()
header(s, "GO-TO-MARKET", "Distribution channels")
chans = [
    ("Schools & teachers", "Email depts, PTAs, district STEM coordinators; turnkey hosting kit"),
    ("Parent communities", "Facebook, WhatsApp, Nextdoor, Reddit — one-tap link sharing"),
    ("Search & social", "Win searches like 'AMC 8 near me'; rich link previews"),
    ("Local & in-person", "Libraries, math circles, flyers with QR codes"),
    ("Dept of Ed channels", "State STEM offices, newsletters, educator networks"),
    ("Capture & remind", "Opt-in email list for deadline reminders"),
]
x0, y0 = Inches(0.6), Inches(1.7)
cw2, ch2 = Inches(3.9), Inches(2.45)
for i, (t, d) in enumerate(chans):
    cx = x0 + (cw2 + Inches(0.2)) * (i % 3)
    cy = y0 + (ch2 + Inches(0.2)) * (i // 3)
    card(s, cx, cy, cw2, ch2, t, [d], [GREEN, SKY, RGBColor(0xd9,0x77,0x06)][i % 3])

# ---------- Slide 10: The Ask ----------
s = slide()
header(s, "THE PARTNERSHIP ASK", "How the Dept of Education can help")
asks = [
    ("Reach", "Share the hub through state STEM offices, educator newsletters, and district networks"),
    ("Endorse", "Lend credibility so principals take the hosting ask seriously"),
    ("Pilot", "Co-sponsor a multi-state awareness pilot in Title I & rural districts"),
    ("Measure", "Help track host-school growth and participation as an equity metric"),
]
y = Inches(1.7)
for i, (t, d) in enumerate(asks):
    cy = y + (Inches(1.25) + Inches(0.12)) * i
    rect(s, Inches(0.6), cy, Inches(0.9), Inches(1.25), [GREEN, SKY, RGBColor(0xd9,0x77,0x06), DARK][i])
    text(s, Inches(0.6), cy, Inches(0.9), Inches(1.25), [(str(i+1), 28, WHITE, True)],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, Inches(1.5), cy, Inches(11.2), Inches(1.25), CARD)
    text(s, Inches(1.75), cy + Inches(0.14), Inches(10.8), Inches(1.0),
         [(t, 16, DARK, True), (d, 13, TEXT, False)], anchor=MSO_ANCHOR.MIDDLE, space=1.05)

# ---------- Slide 11: Pilot Proposal ----------
s = slide()
header(s, "PROPOSAL", "A concrete 12-month awareness pilot")
card(s, Inches(0.6), Inches(1.6), Inches(3.9), Inches(2.3), "Scope",
     ["3–5 states, focus on Title I & rural districts",
      "Target: 250+ new host schools",
      "Zero cost to schools to participate"], GREEN)
card(s, Inches(4.7), Inches(1.6), Inches(3.9), Inches(2.3), "Mechanics",
     ["Distribute hosting kit via state channels",
      "Webinar + office hours for new managers",
      "Track registrations vs. baseline"], SKY)
card(s, Inches(8.8), Inches(1.6), Inches(3.9), Inches(2.3), "Cost profile",
     ["Hub is free & static — no platform cost",
      "Spend = outreach + coordination only",
      "Highly leveraged per dollar"], RGBColor(0xd9,0x77,0x06))
text(s, Inches(0.6), Inches(4.2), Inches(12), Inches(0.5), [("Target outcomes", 16, DARK, True)])
card(s, Inches(0.6), Inches(4.75), Inches(5.9), Inches(1.7), "Participation",
     ["New host schools in underserved areas",
      "First-time student competitors"], GREEN)
card(s, Inches(6.8), Inches(4.75), Inches(5.9), Inches(1.7), "Sustainability",
     ["Returning host schools year 2",
      "Parent-led math circles started"], SKY)

# ---------- Slide 12: Success Metrics ----------
s = slide()
header(s, "MEASUREMENT", "How we'll know it's working")
metrics = [
    ("Host schools", "New test sites registered", GREEN),
    ("New competitors", "First-time student participants", SKY),
    ("Reach", "Shares & referral traffic", RGBColor(0xd9,0x77,0x06)),
    ("Equity mix", "% growth in Title I / rural", DARK),
    ("Teacher activation", "Hosting-kit downloads", GREEN),
    ("Retention", "Schools returning year 2", SKY),
]
x0, y0 = Inches(0.6), Inches(1.8)
bw, bh = Inches(3.9), Inches(2.15)
for i, (t, d, c) in enumerate(metrics):
    cx = x0 + (bw + Inches(0.2)) * (i % 3)
    cy = y0 + (bh + Inches(0.25)) * (i // 3)
    rect(s, cx, cy, bw, bh, c)
    text(s, cx + Inches(0.25), cy + Inches(0.25), bw - Inches(0.5), Inches(0.7),
         [(t, 19, WHITE, True)])
    text(s, cx + Inches(0.25), cy + Inches(1.0), bw - Inches(0.5), Inches(1.0),
         [(d, 13, WHITE, False)], space=1.05)
text(s, Inches(0.6), Inches(6.75), Inches(12), Inches(0.4),
     [("Privacy-friendly analytics (GoatCounter) — no student data collected.", 11, MUTED, False)])

# ---------- Slide 13: Roadmap ----------
s = slide()
header(s, "ROADMAP", "From launch to nationwide")
phases = [
    ("Now", "Foundation", ["Hub live & shareable", "SEO + social previews", "Open-source + documented"], GREEN),
    ("Q1–Q2", "Teacher enablement", ["Hosting kit + flyer", "Email reminders", "Webinars"], SKY),
    ("Q2–Q3", "Pilot", ["3–5 state rollout", "Track host growth", "Office hours"], RGBColor(0xd9,0x77,0x06)),
    ("Q4+", "Scale", ["Expand states", "Local site finder", "Community submissions"], DARK),
]
bw = Inches(3.0)
x = Inches(0.6)
for label, title, items, c in phases:
    rect(s, x, Inches(1.8), bw, Inches(0.8), c)
    text(s, x, Inches(1.8), bw, Inches(0.8), [(label, 18, WHITE, True)],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, x, Inches(2.65), bw, Inches(3.4), CARD)
    runs = [(title, 15, c, True)]
    for it in items:
        runs.append((it, 12, TEXT, False, True))
    text(s, x + Inches(0.18), Inches(2.85), bw - Inches(0.36), Inches(3.0), runs, space=1.1)
    x += bw + Inches(0.17)

# ---------- Slide 14: Call to Action ----------
s = slide()
rect(s, 0, 0, SW, SH, DARK)
rect(s, 0, Inches(2.2), SW, Pt(5), SKY)
text(s, Inches(0.9), Inches(0.8), Inches(11.5), Inches(1.2),
     [("Let's open the door to math — for every student", 34, WHITE, True)], space=1.0)
text(s, Inches(0.9), Inches(2.5), Inches(11.5), Inches(0.6),
     [("Proposed next steps", 20, MINT, True)])
steps = [
    "Identify 3–5 pilot states and district partners",
    "Route the hosting kit through state STEM & educator channels",
    "Set a shared baseline + success metrics for the pilot",
    "Schedule a working session to finalize scope and timeline",
]
text(s, Inches(0.9), Inches(3.3), Inches(11.5), Inches(2.6),
     [(st, 17, LIGHT, False, True) for st in steps], space=1.3)
text(s, Inches(0.9), Inches(6.3), Inches(11.5), Inches(0.8),
     [("Math Competition Readiness Hub", 15, WHITE, True),
      ("vineetagrwal.github.io/math-dance-pathway", 13, SKY, False)], space=1.1)

out = "Math-Competition-Strategy-DeptOfEducation.pptx"
prs.save(out)
print("Saved", out, "with", len(prs.slides._sldIdLst), "slides")
