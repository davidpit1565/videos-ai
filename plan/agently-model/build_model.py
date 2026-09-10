"""Builds Agently_Unit_Economics_Model_v1.xlsx.

Structure mirrors the Béroche pricing architecture David supplied as the
reference for the level of detail expected: one sheet of live variables that
every other sheet references, a per-unit cost build-up (their BOM = our
cost-per-API-call), a tier matrix, and an executive overview.

Colour convention (financial-model standard):
  blue text   = hardcoded input / lever you can change
  black text  = formula
  green text  = link to another sheet
  yellow fill = assumption that must be replaced with a measured number
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FONT = "Arial"
BLUE = "0000FF"
BLACK = "000000"
GREEN = "008000"
YELLOW = "FFFF00"
HDR_FILL = PatternFill("solid", fgColor="1F3864")
SEC_FILL = PatternFill("solid", fgColor="D9E2F3")
YEL_FILL = PatternFill("solid", fgColor=YELLOW)
BAD_FILL = PatternFill("solid", fgColor="FFC7CE")
GOOD_FILL = PatternFill("solid", fgColor="C6EFCE")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

EUR = '€#,##0.00;(€#,##0.00);-'
EUR0 = '€#,##0;(€#,##0);-'
EUR4 = '€#,##0.0000;(€#,##0.0000);-'
PCT = '0.0%;(0.0%);-'
NUM = '#,##0;(#,##0);-'
NUM1 = '#,##0.0;(#,##0.0);-'

wb = openpyxl.Workbook()


def style(ws, cell, *, bold=False, color=BLACK, size=10, fmt=None, fill=None,
          wrap=False, align=None, border=False):
    c = ws[cell]
    c.font = Font(name=FONT, bold=bold, color=color, size=size)
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if wrap or align:
        c.alignment = Alignment(wrap_text=wrap, horizontal=align, vertical="top")
    if border:
        c.border = BOX
    return c


def title(ws, row, text, sub=None):
    ws[f"A{row}"] = text
    style(ws, f"A{row}", bold=True, size=14, color="1F3864")
    if sub:
        ws[f"A{row+1}"] = sub
        style(ws, f"A{row+1}", size=9, color="595959", wrap=True)


def section(ws, row, text, width=5):
    ws[f"A{row}"] = text
    for i in range(1, width + 1):
        style(ws, f"{get_column_letter(i)}{row}", bold=True, size=10,
              color="FFFFFF", fill=HDR_FILL)


def headers(ws, row, labels):
    for i, lab in enumerate(labels, start=1):
        ws.cell(row=row, column=i, value=lab)
        style(ws, f"{get_column_letter(i)}{row}", bold=True, size=9,
              fill=SEC_FILL, wrap=True, align="left", border=True)


# =====================================================================
# SHEET 1 — INPUTS
# =====================================================================
s1 = wb.active
s1.title = "1_Inputs"
s1.column_dimensions["A"].width = 44
s1.column_dimensions["B"].width = 14
s1.column_dimensions["C"].width = 12
s1.column_dimensions["D"].width = 13
s1.column_dimensions["E"].width = 62

title(s1, 1, "AGENTLY — Unit Economics & Pricing Model",
      "Every number below is either MEASURED (from the live code or database), SOURCED (published third-party "
      "figure, cited), or ASSUMPTION (a placeholder that must be replaced with a real measurement). "
      "Blue = you can change it. Yellow fill = assumption, replace as soon as real data exists. "
      "Every other sheet reads from this one — change a value here and the whole model updates.")
s1["A3"] = "Built 10 Sep 2026 · v1"
style(s1, "A3", size=9, color="595959")

R = {}  # label -> row number, so formulas reference exact cells

rows = [
    ("SEC", "A. WHAT A HOSTED CALL ACTUALLY COSTS US"),
    ("HDR", None),
    ("model_name", "LLM the invoke route calls", "claude-sonnet-5", "model", "MEASURED",
     "app/api/hosted-agents/[slug]/invoke/route.ts:258 — read from the live code, not assumed.", False),
    ("in_price", "Input price per 1M tokens (USD)", 2.00, "USD", "SOURCED",
     "Anthropic published API pricing for claude-sonnet-5. Verify at anthropic.com/pricing before investor use.", False),
    ("out_price", "Output price per 1M tokens (USD)", 10.00, "USD", "SOURCED",
     "Anthropic published API pricing for claude-sonnet-5. Verify at anthropic.com/pricing before investor use.", False),
    ("fx", "USD → EUR conversion rate", 0.92, "EUR per USD", "ASSUMPTION",
     "Placeholder. Replace with the rate your Stripe/bank actually settles at.", True),
    ("max_tok", "max_tokens cap per call", 2048, "tokens", "MEASURED",
     "app/api/hosted-agents/[slug]/invoke/route.ts:259 — hard ceiling on output per call.", False),
    ("in_tok", "Average INPUT tokens per call", 1500, "tokens", "ASSUMPTION",
     "Hidden agent system prompt + user input. NOT measured — log real token counts from the Anthropic "
     "response usage object and replace this. This is the single most important number in the model.", True),
    ("out_tok", "Average OUTPUT tokens per call", 600, "tokens", "ASSUMPTION",
     "Assumed well below the 2048 cap. NOT measured — same fix as above: log response.usage.output_tokens.", True),
    ("infra", "Non-LLM infra cost per call (Vercel, Supabase)", 0.0002, "EUR", "ASSUMPTION",
     "Serverless function + DB writes per invocation. Small but non-zero. Replace with real Vercel/Supabase billing "
     "divided by call count once there is volume.", True),

    ("SEC", "B. WHAT WE CHARGE — CURRENT LIVE PRICING"),
    ("HDR", None),
    ("basic_p", "Basic tier — monthly price", 9.00, "EUR", "MEASURED",
     "lib/membership.ts MEMBERSHIP_TIERS.basic.monthlyPriceCents = 900. Code comment calls it a placeholder.", False),
    ("basic_c", "Basic tier — monthly credits granted", 300, "credits", "MEASURED",
     "lib/membership.ts. Code comment: 'Round, clearly-arbitrary numbers... not measured against any real "
     "per-call cost.' This model exists to fix exactly that.", False),
    ("pro_p", "Pro tier — monthly price", 29.00, "EUR", "MEASURED", "lib/membership.ts monthlyPriceCents = 2900.", False),
    ("pro_c", "Pro tier — monthly credits granted", 1500, "credits", "MEASURED", "lib/membership.ts.", False),
    ("prof_p", "Professional tier — monthly price", 99.00, "EUR", "MEASURED", "lib/membership.ts monthlyPriceCents = 9900.", False),
    ("prof_c", "Professional tier — monthly credits granted", 8000, "credits", "MEASURED", "lib/membership.ts.", False),
    ("cpc", "Credits charged per call (creator-set)", 1, "credits", "ASSUMPTION",
     "Each creator sets credits_per_call on their agent, capped at 50 (lib/hosted-agents.ts MAX_CREDITS_PER_CALL). "
     "1 = the cheapest case, i.e. the worst case for us. Change to test other settings.", True),
    ("free_credits", "Free credits granted at signup (one-time)", 20, "credits", "MEASURED",
     "One-time non-renewing grant. Pure marketing cost — no revenue behind it.", False),

    ("SEC", "C. HOW REVENUE IS SPLIT"),
    ("HDR", None),
    ("fee_pct", "Platform fee — share WE keep", 0.15, "% of revenue", "MEASURED",
     "lib/membership.ts PLATFORM_FEE_PERCENT = 15. Report ch.6: 'start low (10-15%), raise once there's liquidity.'", False),
    ("creator_pct", "Creator share — share THEY get", 0.85, "% of revenue", "MEASURED",
     "= 1 − platform fee. lib/creator-payouts.ts pools 85% of membership revenue and splits it by usage share.", False),
    ("payout_base", "Creator payout is calculated on…", "GROSS revenue", "basis", "MEASURED",
     "lib/creator-payouts.ts: poolCents = totalRevenueCents × 85%. API cost is NOT deducted first. "
     "See sheet 4 — this is the structural problem.", False),

    ("SEC", "D. PAYMENT PROCESSING"),
    ("HDR", None),
    ("stripe_pct", "Stripe percentage fee (EU cards)", 0.015, "% of charge", "SOURCED",
     "Stripe published EU standard rate ~1.5%. Verify against your own Stripe dashboard.", False),
    ("stripe_fix", "Stripe fixed fee per charge", 0.25, "EUR", "MEASURED",
     "lib/membership.ts comment: measured at ~€0.25-0.30 by running a live €1 test purchase and reading the "
     "resulting Stripe balance transactions — platform ended at -€0.13 net on it.", False),

    ("SEC", "E. GROWTH ASSUMPTIONS (sheet 5 only — all unproven)"),
    ("HDR", None),
    ("start_paid", "Paying members at month 0", 2, "members", "MEASURED",
     "Live Supabase query 6.9.2026 — and both are David's own test accounts, not external customers.", False),
    ("new_signups", "New free signups per month", 40, "signups", "ASSUMPTION",
     "No basis in real data. There are 3 registered users total today. Placeholder to make the sheet compute.", True),
    ("conv", "Free → paid conversion rate", 0.04, "%", "ASSUMPTION",
     "Typical prosumer SaaS freemium conversion is low single digits. Not measured for this product.", True),
    ("churn", "Monthly churn of paying members", 0.07, "%", "ASSUMPTION",
     "Placeholder in the normal SMB/prosumer range. Not measured — there is no cohort history yet.", True),
    ("mix_basic", "Tier mix — Basic", 0.60, "% of paid", "ASSUMPTION", "Placeholder. No real mix data exists.", True),
    ("mix_pro", "Tier mix — Pro", 0.30, "% of paid", "ASSUMPTION", "Placeholder.", True),
    ("mix_prof", "Tier mix — Professional", 0.10, "% of paid", "ASSUMPTION", "Placeholder.", True),
    ("util", "Credit utilisation — % of granted credits actually used", 0.35, "%", "ASSUMPTION",
     "THE swing variable. At low utilisation the model works; above the break-even on sheet 3 every member "
     "loses money. Must be measured from agently_agent_invocations as soon as there is real usage.", True),
    ("fixed_cost", "Fixed monthly operating cost", 150.00, "EUR", "ASSUMPTION",
     "Vercel + Supabase + domain + email. Excludes any salary for David.", True),
]

r = 5
for item in rows:
    if item[0] == "SEC":
        r += 1
        section(s1, r, item[1])
        r += 1
        headers(s1, r, ["Variable", "Value", "Unit", "Status", "Source / why this number"])
        r += 1
        continue
    if item[0] == "HDR":
        continue
    key, label, val, unit, status, src, is_assum = item
    R[key] = r
    s1[f"A{r}"] = label
    s1[f"B{r}"] = val
    s1[f"C{r}"] = unit
    s1[f"D{r}"] = status
    s1[f"E{r}"] = src
    style(s1, f"A{r}", size=10, wrap=True, align="left", border=True)
    fmt = None
    if unit == "EUR":
        fmt = EUR4 if isinstance(val, float) and val < 0.01 else EUR
    elif unit.startswith("%"):
        fmt = PCT
    elif unit in ("tokens", "credits", "signups", "members"):
        fmt = NUM
    style(s1, f"B{r}", bold=True, color=BLUE, fmt=fmt,
          fill=YEL_FILL if is_assum else None, border=True, align="right")
    style(s1, f"C{r}", size=9, color="595959", border=True)
    style(s1, f"D{r}", size=9, bold=True, border=True,
          color="C00000" if status == "ASSUMPTION" else ("006100" if status == "MEASURED" else "7F6000"))
    style(s1, f"E{r}", size=8, color="404040", wrap=True, align="left", border=True)
    r += 1

# Derived cost block
r += 1
section(s1, r, "F. DERIVED — COST PER CALL (calculated, do not edit)")
r += 1
headers(s1, r, ["Derived value", "Value", "Unit", "Status", "Formula in words"])
r += 1
IN_ = f"$B${R['in_price']}"; OUT_ = f"$B${R['out_price']}"; FX = f"$B${R['fx']}"
R["cost_in"] = r
s1[f"A{r}"] = "Input cost per call"
s1[f"B{r}"] = f"=($B${R['in_tok']}/1000000)*{IN_}*{FX}"
s1[f"C{r}"] = "EUR"; s1[f"D{r}"] = "DERIVED"
s1[f"E{r}"] = "avg input tokens ÷ 1M × input price × FX"
r += 1
R["cost_out"] = r
s1[f"A{r}"] = "Output cost per call"
s1[f"B{r}"] = f"=($B${R['out_tok']}/1000000)*{OUT_}*{FX}"
s1[f"C{r}"] = "EUR"; s1[f"D{r}"] = "DERIVED"
s1[f"E{r}"] = "avg output tokens ÷ 1M × output price × FX"
r += 1
R["cost_call"] = r
s1[f"A{r}"] = "TOTAL cost per call (LLM + infra)"
s1[f"B{r}"] = f"=$B${R['cost_in']}+$B${R['cost_out']}+$B${R['infra']}"
s1[f"C{r}"] = "EUR"; s1[f"D{r}"] = "DERIVED"
s1[f"E{r}"] = "input cost + output cost + infra cost"
r += 1
R["cost_credit"] = r
s1[f"A{r}"] = "TOTAL cost per credit"
s1[f"B{r}"] = f"=$B${R['cost_call']}/$B${R['cpc']}"
s1[f"C{r}"] = "EUR"; s1[f"D{r}"] = "DERIVED"
s1[f"E{r}"] = "cost per call ÷ credits charged per call"
r += 1
R["free_cost"] = r
s1[f"A{r}"] = "Cost of the free signup grant (per signup)"
s1[f"B{r}"] = f"=$B${R['free_credits']}*$B${R['cost_credit']}"
s1[f"C{r}"] = "EUR"; s1[f"D{r}"] = "DERIVED"
s1[f"E{r}"] = "free credits × cost per credit — pure marketing cost, no revenue behind it"

for rr in range(R["cost_in"], R["free_cost"] + 1):
    style(s1, f"A{rr}", size=10, bold=True, border=True, wrap=True, align="left")
    style(s1, f"B{rr}", bold=True, fmt=EUR4, border=True, align="right")
    style(s1, f"C{rr}", size=9, color="595959", border=True)
    style(s1, f"D{rr}", size=9, bold=True, color="404040", border=True)
    style(s1, f"E{rr}", size=8, color="404040", wrap=True, align="left", border=True)

S1 = "'1_Inputs'"
C_CALL = f"{S1}!$B${R['cost_call']}"
C_CRED = f"{S1}!$B${R['cost_credit']}"
CREATOR = f"{S1}!$B${R['creator_pct']}"
FEEPCT = f"{S1}!$B${R['fee_pct']}"
SPCT = f"{S1}!$B${R['stripe_pct']}"
SFIX = f"{S1}!$B${R['stripe_fix']}"


# =====================================================================
# SHEET 2 — COST PER CALL (the "BOM" equivalent)
# =====================================================================
s2 = wb.create_sheet("2_Cost per Call")
for col, w in zip("ABCDEFG", [40, 14, 14, 14, 14, 14, 46]):
    s2.column_dimensions[col].width = w

title(s2, 1, "COST PER CALL — the bill of materials, in tokens",
      "Béroche's BOM sheet costs a bottle, a pump and a label. Ours costs input tokens, output tokens and "
      "serverless compute. Same idea: you cannot price a product until you know what one unit costs to produce. "
      "The model column shows what the same call would cost on a cheaper Claude model — that is a real lever.")

section(s2, 4, "PER-CALL COST BY MODEL CHOICE", 7)
headers(s2, 5, ["Model", "Input $/1M", "Output $/1M", "Input cost (€)", "Output cost (€)",
                "Total per call (€)", "Note"])

models = [
    ("claude-sonnet-5  ← what we run today", 2.00, 10.00,
     "Currently hardcoded in the invoke route. Source: Anthropic published pricing."),
    ("claude-haiku-4-5", 1.00, 5.00,
     "Half the price of Sonnet 5. Viable for simple prompt-based agents (category 1) — a real cost lever."),
    ("claude-opus-5", 5.00, 25.00,
     "2.5× Sonnet 5. Only justified for agents where output quality is the product."),
]
mrow0 = 6
for i, (name, ip, op, note) in enumerate(models):
    rr = mrow0 + i
    s2[f"A{rr}"] = name
    s2[f"B{rr}"] = ip
    s2[f"C{rr}"] = op
    s2[f"D{rr}"] = f"=({S1}!$B${R['in_tok']}/1000000)*B{rr}*{S1}!$B${R['fx']}"
    s2[f"E{rr}"] = f"=({S1}!$B${R['out_tok']}/1000000)*C{rr}*{S1}!$B${R['fx']}"
    s2[f"F{rr}"] = f"=D{rr}+E{rr}+{S1}!$B${R['infra']}"
    s2[f"G{rr}"] = note
    style(s2, f"A{rr}", bold=(i == 0), border=True, wrap=True, align="left")
    style(s2, f"B{rr}", color=BLUE, fmt='$#,##0.00', border=True, align="right")
    style(s2, f"C{rr}", color=BLUE, fmt='$#,##0.00', border=True, align="right")
    style(s2, f"D{rr}", fmt=EUR4, border=True, align="right")
    style(s2, f"E{rr}", fmt=EUR4, border=True, align="right")
    style(s2, f"F{rr}", bold=True, fmt=EUR4, border=True, align="right",
          fill=GOOD_FILL if i == 1 else None)
    style(s2, f"G{rr}", size=8, color="404040", wrap=True, align="left", border=True)

section(s2, 10, "SENSITIVITY — what if the token estimate is wrong?", 7)
s2["A11"] = ("The two token counts on sheet 1 are assumptions, not measurements. This grid shows the cost per call "
             "across a realistic range so you can see how much the answer moves. Read the row that matches your "
             "guess; the model uses the sheet-1 values.")
style(s2, "A11", size=9, color="595959", wrap=True)
s2.merge_cells("A11:G11")
s2.row_dimensions[11].height = 28

headers(s2, 13, ["Input tokens ↓  /  Output tokens →", "300", "600", "1,000", "1,500", "2,048 (cap)", ""])
in_variants = [500, 1000, 1500, 2500, 4000]
out_variants = [300, 600, 1000, 1500, 2048]
for i, itok in enumerate(in_variants):
    rr = 14 + i
    s2[f"A{rr}"] = f"{itok:,} input tokens"
    style(s2, f"A{rr}", bold=True, size=9, border=True, align="left")
    for j, otok in enumerate(out_variants):
        col = get_column_letter(2 + j)
        s2[f"{col}{rr}"] = (f"=({itok}/1000000)*{S1}!$B${R['in_price']}*{S1}!$B${R['fx']}"
                            f"+({otok}/1000000)*{S1}!$B${R['out_price']}*{S1}!$B${R['fx']}"
                            f"+{S1}!$B${R['infra']}")
        style(s2, f"{col}{rr}", fmt=EUR4, border=True, align="right",
              fill=YEL_FILL if (itok == 1500 and otok == 600) else None)

s2["A20"] = ("Yellow cell = the combination the model currently assumes. Across this whole grid the cost per call "
             "stays between roughly €0.002 and €0.030 — so even the optimistic corner does not rescue the tier "
             "economics on sheet 3.")
style(s2, "A20", size=9, color="404040", wrap=True)
s2.merge_cells("A20:G20")
s2.row_dimensions[20].height = 28


# =====================================================================
# SHEET 3 — TIER MARGINS
# =====================================================================
s3 = wb.create_sheet("3_Tier Margins")
for col, w in zip("ABCDEFG", [42, 15, 15, 15, 15, 15, 4]):
    s3.column_dimensions[col].width = w

title(s3, 1, "TIER MARGINS — does each membership actually make money?",
      "For each tier: what we charge, what we owe the creator (85% of GROSS revenue, per lib/creator-payouts.ts), "
      "what Stripe takes, and what the API calls cost us. Columns are credit utilisation — the share of the "
      "granted monthly credits a member actually uses. The break-even row is the punchline.")

utils = [0.10, 0.25, 0.50, 0.75, 1.00]
tiers = [("BASIC", "basic_p", "basic_c"), ("PRO", "pro_p", "pro_c"), ("PROFESSIONAL", "prof_p", "prof_c")]

row = 4
tier_net_rows = {}
for tname, pkey, ckey in tiers:
    price_ref = f"{S1}!$B${R[pkey]}"
    cred_ref = f"{S1}!$B${R[ckey]}"
    section(s3, row, f"{tname}  —  see sheet 1 for price and credit allotment", 6)
    row += 1
    headers(s3, row, ["Metric", "10% used", "25% used", "50% used", "75% used", "100% used"])
    hdr_row = row
    row += 1

    metrics = [
        ("Credits actually used", lambda u: f"={cred_ref}*{u}", NUM, False),
        ("Calls that represents", lambda u: f"={cred_ref}*{u}/{S1}!$B${R['cpc']}", NUM, False),
        ("Gross revenue (member pays)", lambda u: f"={price_ref}", EUR, False),
        ("less: creator payout (85% of gross)", lambda u: f"=-{price_ref}*{CREATOR}", EUR, False),
        ("less: Stripe processing fee", lambda u: f"=-({price_ref}*{SPCT}+{SFIX})", EUR, False),
        ("less: API + infra cost", lambda u: f"=-{cred_ref}*{u}*{C_CRED}", EUR, False),
    ]
    first_metric_row = row
    for label, fn, fmt, _ in metrics:
        s3[f"A{row}"] = label
        style(s3, f"A{row}", size=9, border=True, align="left",
              bold=label.startswith("Gross"))
        for j, u in enumerate(utils):
            col = get_column_letter(2 + j)
            s3[f"{col}{row}"] = fn(u)
            style(s3, f"{col}{row}", fmt=fmt, border=True, align="right", size=9)
        row += 1

    net_row = row
    tier_net_rows[tname] = net_row
    s3[f"A{row}"] = "= PLATFORM NET PER MEMBER / MONTH"
    style(s3, f"A{row}", bold=True, size=10, border=True, align="left")
    for j, u in enumerate(utils):
        col = get_column_letter(2 + j)
        s3[f"{col}{row}"] = f"=SUM({col}{first_metric_row+2}:{col}{first_metric_row+5})"
        style(s3, f"{col}{row}", bold=True, fmt=EUR, border=True, align="right")
    row += 1

    s3[f"A{row}"] = "Net margin % of revenue"
    style(s3, f"A{row}", size=9, border=True, align="left")
    for j, u in enumerate(utils):
        col = get_column_letter(2 + j)
        s3[f"{col}{row}"] = f"=IFERROR({col}{net_row}/{price_ref},0)"
        style(s3, f"{col}{row}", fmt=PCT, border=True, align="right", size=9)
    row += 1

    s3[f"A{row}"] = "BREAK-EVEN utilisation (above this, we lose money)"
    style(s3, f"A{row}", bold=True, size=9, border=True, align="left", fill=SEC_FILL)
    s3[f"B{row}"] = (f"=IFERROR(({price_ref}*(1-{CREATOR})-({price_ref}*{SPCT}+{SFIX}))"
                     f"/({cred_ref}*{C_CRED}),0)")
    style(s3, f"B{row}", bold=True, fmt=PCT, border=True, align="right", fill=YEL_FILL)
    s3[f"C{row}"] = ("← what we keep after creator + Stripe, divided by the cost of using every granted credit")
    style(s3, f"C{row}", size=8, color="404040", align="left")
    s3.merge_cells(f"C{row}:F{row}")
    row += 3

section(s3, row, "WHAT THIS SHEET SAYS", 6)
row += 1
s3[f"A{row}"] = (
    "The platform keeps only 15% of membership revenue, but pays 100% of the API cost out of that 15%. "
    "So the break-even is not a matter of scale or efficiency — it is arithmetic: API cost must stay under "
    "15% of revenue, minus Stripe. The higher the tier, the more credits are granted per euro, and therefore "
    "the WORSE the economics. That is the opposite of how tiers are supposed to work: normally the expensive "
    "tier is the profitable one.\n\n"
    "Note also what is NOT on this sheet: any cost for the free 20-credit signup grant, support time, or "
    "David's own time. Those only make it worse. Sheet 4 works out what would have to change."
)
style(s3, f"A{row}", size=9, color="404040", wrap=True, align="left")
s3.merge_cells(f"A{row}:F{row}")
s3.row_dimensions[row].height = 88


# =====================================================================
# SHEET 4 — CREDIT PRICING / THE FIX
# =====================================================================
s4 = wb.create_sheet("4_Credit Pricing")
for col, w in zip("ABCDEF", [46, 16, 16, 16, 52, 4]):
    s4.column_dimensions[col].width = w

title(s4, 1, "WHAT A CREDIT MUST COST — and the two ways to fix the split",
      "Sheet 3 shows the current pricing loses money. This sheet works out by how much, and prices the two "
      "structural fixes. Everything here is arithmetic off sheet 1 — no new assumptions are introduced.")

section(s4, 4, "A. WHAT WE SELL A CREDIT FOR TODAY, VS WHAT IT COSTS", 5)
headers(s4, 5, ["Tier", "Price per credit charged", "Cost per credit", "Sold at … × cost", "Verdict"])
row = 6
for tname, pkey, ckey in tiers:
    s4[f"A{row}"] = tname.title()
    s4[f"B{row}"] = f"={S1}!$B${R[pkey]}/{S1}!$B${R[ckey]}"
    s4[f"C{row}"] = f"={C_CRED}"
    s4[f"D{row}"] = f"=IFERROR(B{row}/C{row},0)"
    s4[f"E{row}"] = ('Must exceed cost ÷ 15% to survive — see section B. A multiple below that is a structural loss, '
                     'not a volume problem.')
    style(s4, f"A{row}", bold=True, border=True, align="left")
    style(s4, f"B{row}", fmt=EUR4, border=True, align="right")
    style(s4, f"C{row}", fmt=EUR4, border=True, align="right")
    style(s4, f"D{row}", bold=True, fmt='0.00"×"', border=True, align="right")
    style(s4, f"E{row}", size=8, color="404040", wrap=True, align="left", border=True)
    row += 1

row += 1
section(s4, row, "B. THE MINIMUM VIABLE CREDIT PRICE, UNDER THE CURRENT 85/15 SPLIT", 5)
row += 1
headers(s4, row, ["Calculation", "Value", "", "", "Explanation"])
row += 1
be_rows = {}
items_b = [
    ("Cost per credit", f"={C_CRED}", EUR4,
     "From sheet 1 — what one credit of usage costs us in API + infra."),
    ("Share of revenue we keep (platform fee)", f"={FEEPCT}", PCT,
     "The creator takes the other 85%, calculated on GROSS revenue before any cost is deducted."),
    ("less: Stripe's percentage fee", f"={SPCT}", PCT,
     "Comes out of our share too. The fixed €0.25 per charge is handled per-tier on sheet 3, since it does "
     "not scale with credits."),
    ("MINIMUM price per credit to break even", f"=IFERROR({C_CRED}/({FEEPCT}-{SPCT}),0)", EUR4,
     "cost ÷ (15% platform fee − 1.5% Stripe) = cost ÷ 13.5%. Below this price, what we keep cannot cover "
     "the API bill, at any volume. Scale does not help: the gap widens with every extra call."),
    ("Professional tier sells credits at", f"={S1}!$B${R['prof_p']}/{S1}!$B${R['prof_c']}", EUR4,
     "€99 ÷ 8,000 credits — the cheapest credit we sell, and therefore the worst case."),
    ("Shortfall — how far under the minimum", None, '0.00"× too cheap"',
     "How many times over the current Professional credit price would have to rise, with nothing else changed."),
]
for i, (lab, f, fmt, expl) in enumerate(items_b):
    s4[f"A{row}"] = lab
    be_rows[lab] = row
    if f is None:
        f = f"=IFERROR(B{be_rows['MINIMUM price per credit to break even']}/B{be_rows['Professional tier sells credits at']},0)"
    s4[f"B{row}"] = f
    s4[f"E{row}"] = expl
    bold = lab.startswith("MINIMUM") or lab.startswith("Shortfall")
    style(s4, f"A{row}", bold=bold, border=True, align="left", wrap=True)
    style(s4, f"B{row}", bold=bold, fmt=fmt, border=True, align="right",
          fill=YEL_FILL if bold else None)
    style(s4, f"E{row}", size=8, color="404040", wrap=True, align="left", border=True)
    row += 1

row += 1
section(s4, row, "C. THE TWO STRUCTURAL FIXES, PRICED", 5)
row += 1
headers(s4, row, ["Option", "Platform net per €100 of revenue", "Creator gets", "Feasible?", "What it means in practice"])
row += 1

# Assume €100 revenue, utilisation from sheet 1, credits per €100 at Professional rate
util_ref = f"{S1}!$B${R['util']}"
cred_per_100 = f"(100/({S1}!$B${R['prof_p']}/{S1}!$B${R['prof_c']}))"
cogs_100 = f"({cred_per_100}*{util_ref}*{C_CRED})"

opts = [
    ("Today — creators paid 85% of GROSS revenue",
     f"=100*{FEEPCT}-{cogs_100}-(100*{SPCT})",
     f"=100*{CREATOR}",
     "NO",
     "What the code does today (lib/creator-payouts.ts). We pay the API bill out of our 15%. "
     "Negative above the break-even utilisation on sheet 3."),
    ("Fix 1 — creators paid 85% of NET revenue (after API cost)",
     f"=(100-{cogs_100}-(100*{SPCT}))*{FEEPCT}",
     f"=(100-{cogs_100}-(100*{SPCT}))*{CREATOR}",
     "YES",
     "Deduct the API cost of serving the calls before splitting. Cannot go negative, at any utilisation. "
     "This is a one-line change in the payout formula and the single highest-leverage fix in this model."),
    ("Fix 2 — keep 85% of gross, but reprice credits to the sheet-4B minimum",
     f"=100*{FEEPCT}-(100/(IFERROR({C_CRED}/({FEEPCT}-{SPCT}),1)))*{util_ref}*{C_CRED}-(100*{SPCT})",
     f"=100*{CREATOR}",
     "YES, but",
     "Keeps the marketing-friendly 85/15 headline, but a Professional membership would buy roughly a fifth "
     "of the credits it does today. Harder to sell, and it prices out exactly the heavy users a marketplace needs."),
]
for lab, netf, credf, feas, expl in opts:
    s4[f"A{row}"] = lab
    s4[f"B{row}"] = netf
    s4[f"C{row}"] = credf
    s4[f"D{row}"] = feas
    s4[f"E{row}"] = expl
    style(s4, f"A{row}", bold=True, size=9, border=True, align="left", wrap=True)
    style(s4, f"B{row}", bold=True, fmt=EUR, border=True, align="right")
    style(s4, f"C{row}", fmt=EUR, border=True, align="right")
    style(s4, f"D{row}", bold=True, size=9, border=True, align="center",
          fill=BAD_FILL if feas == "NO" else GOOD_FILL)
    style(s4, f"E{row}", size=8, color="404040", wrap=True, align="left", border=True)
    s4.row_dimensions[row].height = 46
    row += 1

row += 2
s4[f"A{row}"] = (
    "Recommendation: Fix 1. Paying creators a share of net rather than gross is what every marketplace with real "
    "per-transaction costs does — the 85/15 App Store analogy breaks precisely because Apple has no per-download "
    "compute bill. It keeps the creator's incentive identical (they still earn more when their agent is used more), "
    "it cannot produce a negative month, and it survives a heavy user. Fix 2 is a fallback if the 85% headline "
    "turns out to matter for recruiting creators — but it should be tested, not assumed."
)
style(s4, f"A{row}", size=9, color="404040", wrap=True, align="left")
s4.merge_cells(f"A{row}:E{row}")
s4.row_dimensions[row].height = 62


# =====================================================================
# SHEET 5 — 36-MONTH PROJECTION
# =====================================================================
s5 = wb.create_sheet("5_Projection 36M")
cols5 = ["Month", "New free signups", "New paid", "Churned", "Active paid", "MRR",
         "Creator payouts", "API + infra COGS", "Stripe fees", "Gross profit",
         "Fixed costs", "Net profit", "Cumulative"]
for i, w in enumerate([8, 15, 11, 11, 12, 13, 15, 16, 12, 13, 12, 13, 13], start=1):
    s5.column_dimensions[get_column_letter(i)].width = w

title(s5, 1, "36-MONTH PROJECTION — scaffolding, not a forecast",
      "EVERY growth input behind this sheet is an assumption (yellow on sheet 1). Today the business has 3 "
      "registered users and €2.00 of lifetime revenue. This sheet exists to show the SHAPE the model produces "
      "and to be re-run against real numbers later — it is not evidence of anything and must not be presented "
      "to an investor as a forecast.")

headers(s5, 4, cols5)
first = 5
for m in range(36):
    rr = first + m
    s5[f"A{rr}"] = m + 1
    s5[f"B{rr}"] = f"={S1}!$B${R['new_signups']}"
    s5[f"C{rr}"] = f"=B{rr}*{S1}!$B${R['conv']}"
    if m == 0:
        s5[f"D{rr}"] = f"={S1}!$B${R['start_paid']}*{S1}!$B${R['churn']}"
        s5[f"E{rr}"] = f"={S1}!$B${R['start_paid']}+C{rr}-D{rr}"
    else:
        s5[f"D{rr}"] = f"=E{rr-1}*{S1}!$B${R['churn']}"
        s5[f"E{rr}"] = f"=E{rr-1}+C{rr}-D{rr}"
    # MRR from tier mix
    s5[f"F{rr}"] = (f"=E{rr}*({S1}!$B${R['mix_basic']}*{S1}!$B${R['basic_p']}"
                    f"+{S1}!$B${R['mix_pro']}*{S1}!$B${R['pro_p']}"
                    f"+{S1}!$B${R['mix_prof']}*{S1}!$B${R['prof_p']})")
    s5[f"G{rr}"] = f"=F{rr}*{CREATOR}"
    s5[f"H{rr}"] = (f"=E{rr}*({S1}!$B${R['mix_basic']}*{S1}!$B${R['basic_c']}"
                    f"+{S1}!$B${R['mix_pro']}*{S1}!$B${R['pro_c']}"
                    f"+{S1}!$B${R['mix_prof']}*{S1}!$B${R['prof_c']})*{S1}!$B${R['util']}*{C_CRED}"
                    f"+B{rr}*{S1}!$B${R['free_cost']}")
    s5[f"I{rr}"] = f"=F{rr}*{SPCT}+E{rr}*{SFIX}"
    s5[f"J{rr}"] = f"=F{rr}-G{rr}-H{rr}-I{rr}"
    s5[f"K{rr}"] = f"={S1}!$B${R['fixed_cost']}"
    s5[f"L{rr}"] = f"=J{rr}-K{rr}"
    s5[f"M{rr}"] = f"=L{rr}" if m == 0 else f"=M{rr-1}+L{rr}"

    style(s5, f"A{rr}", bold=True, size=9, border=True, align="center")
    for col, fmt in zip("BCDE", [NUM, NUM1, NUM1, NUM1]):
        style(s5, f"{col}{rr}", fmt=fmt, size=9, border=True, align="right")
    for col in "FGHIJKLM":
        style(s5, f"{col}{rr}", fmt=EUR0, size=9, border=True, align="right",
              bold=(col in "LM"))

last5 = first + 35
row = last5 + 2
s5[f"A{row}"] = ("Read the 'Net profit' and 'Cumulative' columns. If they are negative and getting more negative "
                 "as the member count grows, the pricing is upside-down — that is the sheet-3 finding showing up "
                 "over time. Fix the pricing on sheet 4 first; only then is a projection worth arguing about.")
style(s5, f"A{row}", size=9, color="404040", wrap=True, align="left")
s5.merge_cells(f"A{row}:M{row}")
s5.row_dimensions[row].height = 42


# =====================================================================
# SHEET 6 — SCENARIOS
# =====================================================================
s6 = wb.create_sheet("6_Scenarios")
for col, w in zip("ABCDE", [40, 18, 18, 18, 50]):
    s6.column_dimensions[col].width = w

title(s6, 1, "SCENARIOS — the three utilisation worlds",
      "Utilisation (what share of granted credits members actually burn) is the variable that decides whether "
      "this business works. These three columns hold everything else constant and move only that. "
      "Change the utilisation cell on sheet 1 to make the rest of the model follow any of these.")

section(s6, 4, "PLATFORM NET PER PROFESSIONAL MEMBER PER MONTH", 5)
headers(s6, 5, ["Scenario", "Utilisation", "Platform net / member", "Annualised per 100 members", "Reading"])
scen = [
    ("Light — members barely use their credits", 0.10,
     "Members forget they subscribed. Profitable, but this is churn waiting to happen: nobody renews a product "
     "they do not use."),
    ("Base — moderate engagement", 0.35,
     "The utilisation figure currently on sheet 1. This is the case that has to work."),
    ("Heavy — engaged members using the product", 0.80,
     "The outcome a marketplace actually wants. Under today's pricing it is the most expensive outcome for us — "
     "which is the clearest possible statement that the pricing is inverted."),
]
row = 6
for name, u, reading in scen:
    pr = f"{S1}!$B${R['prof_p']}"
    cr = f"{S1}!$B${R['prof_c']}"
    s6[f"A{row}"] = name
    s6[f"B{row}"] = u
    s6[f"C{row}"] = f"={pr}*(1-{CREATOR})-({pr}*{SPCT}+{SFIX})-{cr}*B{row}*{C_CRED}"
    s6[f"D{row}"] = f"=C{row}*100*12"
    s6[f"E{row}"] = reading
    style(s6, f"A{row}", bold=True, size=9, border=True, align="left", wrap=True)
    style(s6, f"B{row}", color=BLUE, fmt=PCT, border=True, align="right")
    style(s6, f"C{row}", bold=True, fmt=EUR, border=True, align="right")
    style(s6, f"D{row}", bold=True, fmt=EUR0, border=True, align="right")
    style(s6, f"E{row}", size=8, color="404040", wrap=True, align="left", border=True)
    s6.row_dimensions[row].height = 42
    row += 1

row += 1
section(s6, row, "THE SAME THREE SCENARIOS UNDER FIX 1 (creators paid on NET)", 5)
row += 1
headers(s6, row, ["Scenario", "Utilisation", "Platform net / member", "Annualised per 100 members", "Reading"])
row += 1
for name, u, _ in scen:
    pr = f"{S1}!$B${R['prof_p']}"
    cr = f"{S1}!$B${R['prof_c']}"
    s6[f"A{row}"] = name
    s6[f"B{row}"] = u
    s6[f"C{row}"] = f"=({pr}-{cr}*B{row}*{C_CRED}-({pr}*{SPCT}+{SFIX}))*(1-{CREATOR})"
    s6[f"D{row}"] = f"=C{row}*100*12"
    s6[f"E{row}"] = "Positive in every scenario. Smaller in absolute terms at high usage — but never negative."
    style(s6, f"A{row}", bold=True, size=9, border=True, align="left", wrap=True)
    style(s6, f"B{row}", color=BLUE, fmt=PCT, border=True, align="right")
    style(s6, f"C{row}", bold=True, fmt=EUR, border=True, align="right", fill=GOOD_FILL)
    style(s6, f"D{row}", bold=True, fmt=EUR0, border=True, align="right")
    style(s6, f"E{row}", size=8, color="404040", wrap=True, align="left", border=True)
    row += 1


# =====================================================================
# SHEET 7 — EXECUTIVE SUMMARY
# =====================================================================
s7 = wb.create_sheet("7_Executive Summary")
for col, w in zip("ABCD", [52, 20, 20, 56]):
    s7.column_dimensions[col].width = w

title(s7, 1, "EXECUTIVE SUMMARY — read this screen only",
      "Everything below is calculated from the live code and the assumptions on sheet 1. Nothing here is typed in "
      "by hand.")

section(s7, 4, "THE FOUR NUMBERS THAT MATTER", 4)
headers(s7, 5, ["Question", "Answer", "Unit", "What it means"])

summary = [
    ("What does one hosted-agent call cost us?", f"={C_CALL}", EUR4,
     "LLM tokens plus serverless compute. The whole model rests on this and on the two token assumptions "
     "behind it — measure them first."),
    ("What must one credit sell for, just to break even?", f"=IFERROR({C_CRED}/({FEEPCT}-{SPCT}),0)", EUR4,
     "Because we keep only 15% of revenue, Stripe takes 1.5%, and the whole API bill comes out of what is left."),
    ("What does the Professional tier actually sell a credit for?",
     f"={S1}!$B${R['prof_p']}/{S1}!$B${R['prof_c']}", EUR4,
     "€99 for 8,000 credits. Compare with the row above."),
    ("Above what usage does a Professional member lose us money?",
     f"=IFERROR(({S1}!$B${R['prof_p']}*(1-{CREATOR})-({S1}!$B${R['prof_p']}*{SPCT}+{SFIX}))"
     f"/({S1}!$B${R['prof_c']}*{C_CRED}),0)", PCT,
     "Share of their granted credits. Above this line, the better the product performs, the more we lose."),
]
row = 6
for q, f, fmt, mean in summary:
    s7[f"A{row}"] = q
    s7[f"B{row}"] = f
    s7[f"C{row}"] = "EUR" if fmt == EUR4 else "% of credits"
    s7[f"D{row}"] = mean
    style(s7, f"A{row}", bold=True, size=10, border=True, align="left", wrap=True)
    style(s7, f"B{row}", bold=True, size=12, fmt=fmt, border=True, align="right", fill=YEL_FILL)
    style(s7, f"C{row}", size=9, color="595959", border=True, align="center")
    style(s7, f"D{row}", size=8, color="404040", wrap=True, align="left", border=True)
    s7.row_dimensions[row].height = 40
    row += 1

row += 1
section(s7, row, "THE FINDING", 4)
row += 1
s7[f"A{row}"] = (
    "Agently currently pays creators 85% of GROSS membership revenue while absorbing 100% of the Anthropic API "
    "cost out of the remaining 15%. That makes gross margin a function of how much customers use the product — "
    "in the wrong direction. Past a low usage threshold, every additional call costs the platform money, and the "
    "most expensive tier crosses that threshold soonest, because it grants the most credits per euro.\n\n"
    "This is not a scale problem and it does not improve with volume: it is arithmetic. The fix is on sheet 4, "
    "and it is small — pay creators a share of revenue NET of the API cost of serving their agents, rather than "
    "gross. The creator's incentive is unchanged (more usage still means more money), and the platform can no "
    "longer be bankrupted by its own success."
)
style(s7, f"A{row}", size=10, color="404040", wrap=True, align="left")
s7.merge_cells(f"A{row}:D{row}")
s7.row_dimensions[row].height = 118

row += 2
section(s7, row, "WHAT THIS MODEL IS NOT", 4)
row += 1
s7[f"A{row}"] = (
    "It is not evidence of a market. As of the live database query on 6.9.2026 the platform has 2 approved agents, "
    "0 external creators, 3 registered users and €2.00 of lifetime revenue. Sheets 1–4 are decision-grade: they "
    "run on real code and real published prices, and they are enough to fix the pricing today. Sheets 5–6 are "
    "scaffolding built on invented growth assumptions and should not be shown to an investor as a forecast — "
    "they become real when there are real cohorts to put in them."
)
style(s7, f"A{row}", size=9, color="404040", wrap=True, align="left")
s7.merge_cells(f"A{row}:D{row}")
s7.row_dimensions[row].height = 72

row += 2
section(s7, row, "NEXT THREE ACTIONS", 4)
row += 1
for i, a in enumerate([
    "1.  Log the real input and output token counts from the Anthropic response on every hosted call. Two numbers, "
    "one commit — they replace the only two load-bearing assumptions in this model.",
    "2.  Decide between Fix 1 (pay creators on net) and Fix 2 (reprice credits) on sheet 4. Fix 1 is recommended.",
    "3.  Re-run this model with the measured token counts before any pricing goes public or any investor sees a number.",
], start=1):
    s7[f"A{row}"] = a
    style(s7, f"A{row}", size=9, color="404040", wrap=True, align="left")
    s7.merge_cells(f"A{row}:D{row}")
    s7.row_dimensions[row].height = 30
    row += 1


# =====================================================================
# SHEET 8 — SOURCES
# =====================================================================
s8 = wb.create_sheet("8_Sources")
for col, w in zip("ABC", [34, 18, 92]):
    s8.column_dimensions[col].width = w
title(s8, 1, "SOURCES & PROVENANCE",
      "House rule: never fabricate. Every input in this model is listed here with where it came from. "
      "Anything marked ASSUMPTION is a placeholder and is flagged as such wherever it appears.")
headers(s8, 4, ["Input", "Status", "Source"])
row = 5
for key, rr in R.items():
    if key in ("cost_in", "cost_out", "cost_call", "cost_credit", "free_cost"):
        continue
    s8[f"A{row}"] = s1[f"A{rr}"].value
    s8[f"B{row}"] = s1[f"D{rr}"].value
    s8[f"C{row}"] = s1[f"E{rr}"].value
    st = s1[f"D{rr}"].value
    style(s8, f"A{row}", size=9, border=True, align="left", wrap=True)
    style(s8, f"B{row}", size=9, bold=True, border=True, align="center",
          color="C00000" if st == "ASSUMPTION" else ("006100" if st == "MEASURED" else "7F6000"),
          fill=YEL_FILL if st == "ASSUMPTION" else None)
    style(s8, f"C{row}", size=8, color="404040", border=True, align="left", wrap=True)
    row += 1

row += 1
s8[f"A{row}"] = "EXTERNAL PRECEDENT — what other platforms actually do (researched 10.9.2026, sources below)"
style(s8, f"A{row}", bold=True, size=10, color="1F3864")
row += 1
for who, what, src in [
    ("Poe (Quora)",
     "The closest structural analogue to our hosted model — and it deliberately ABANDONED the usage-pool split. "
     "Creators now set a price per message themselves, up to $10,000 per 1,000 messages, precisely because a "
     "pool does not cover an expensive bot's inference cost. That is the same failure this model found, "
     "reached independently by a company that raised $75M from a16z to run it.",
     "TechCrunch 9.4.2024 techcrunch.com/2024/04/09/poe-introduces-a-price-per-message-revenue-model-for-ai-bot-creators/ "
     "· poe.com/blog/new-on-poe-creator-monetization-via-price-per-message · a16z round: TechCrunch 9.1.2024"),
    ("OpenAI GPT Store",
     "Our payout design was described as 'the same model the GPT Store pays creators under'. That claim does not "
     "hold up: revenue sharing was announced Jan 2024, never opened beyond an invite-only US pilot, the formula "
     "was never published, and GPTs have since been superseded by the Apps SDK — whose documented monetization "
     "route is external checkout on the developer's own site. CORRECT THIS CLAIM wherever it appears.",
     "VentureBeat 1.2024 · OpenAI dev community thread 839172 · developers.openai.com/apps-sdk/build/monetization"),
    ("Take rates, observed range",
     "Apple 30% (15% under $1M) · Google Play 15% on subs · Unity Asset Store 30% · Shopify 0% on first $1M · "
     "Patreon 10% · Substack 10% · YouTube 45% of ad revenue. Our 15% is defensible and creator-friendly, but it "
     "is NOT 'standard' — the modal digital-goods rate is 30%. Reframe the claim.",
     "Apple SBP via RevenueCat · assetstore.unity.com/publishing · TechCrunch 29.6.2021 (Shopify) · "
     "support.google.com/youtube/answer/72902"),
    ("Monthly payout cadence",
     "This half of our claim does hold — Patreon, Substack and YouTube all pay monthly. Note that every mature "
     "system also has a minimum payout threshold and a lag (Roblox 30,000 Robux, YouTube $100). Ours has neither "
     "yet; investors will ask.",
     "support.google.com/youtube/answer/72902 · create.roblox.com/docs/production/monetization/developer-exchange"),
    ("Disintermediation risk",
     "Peer-reviewed result: as a platform improves trust between its two sides, it increases the risk they "
     "transact off-platform to avoid the fee. Directly relevant to file agents, which have zero ongoing platform "
     "dependency once downloaded. The hosted product is the only half with a real anti-leakage mechanism.",
     "Hagiu & Wright, 'Marketplace Leakage', Management Science — doi 10.1287/mnsc.2023.4757"),
]:
    s8[f"A{row}"] = who
    s8[f"B{row}"] = "SOURCED"
    s8[f"C{row}"] = what + "  [" + src + "]"
    style(s8, f"A{row}", bold=True, size=9, border=True, align="left", wrap=True)
    style(s8, f"B{row}", size=9, bold=True, border=True, align="center", color="7F6000")
    style(s8, f"C{row}", size=8, color="404040", border=True, align="left", wrap=True)
    s8.row_dimensions[row].height = 62
    row += 1

row += 1
s8[f"A{row}"] = "NOT CONFIRMED — do not present as fact"
style(s8, f"A{row}", bold=True, size=10, color="C00000")
row += 1
for gap in [
    "Real input/output token counts per hosted call — never measured. The two most important numbers in the model.",
    "Real credit utilisation — never measured; there is no meaningful usage history.",
    "Stripe's exact effective rate on this account — the €0.25 fixed fee is measured, the 1.5% is the published rate.",
    "USD/EUR rate actually realised after bank spread.",
    "Every growth input on sheet 5 (signups, conversion, churn, tier mix) — invented placeholders.",
]:
    s8[f"A{row}"] = gap
    style(s8, f"A{row}", size=9, color="404040", wrap=True, align="left")
    s8.merge_cells(f"A{row}:C{row}")
    row += 1

for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A5"

out = "/home/user/videos-ai/plan/agently-model/Agently_Unit_Economics_Model_v1.xlsx"
wb.save(out)
print("saved", out)
