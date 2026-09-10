"""Independent verification of Agently_Unit_Economics_Model_v1.xlsx.

LibreOffice cannot load ANY xlsx in this build environment (a three-cell test
file fails identically), so scripts/recalc.py cannot run here. This script is
the substitute:

  Part 1 — reference integrity. Every cell reference inside every formula is
           resolved and checked to point at a cell that actually holds a value
           or another formula. Catches the likeliest failure mode: a typo'd
           row number producing a silent zero.

  Part 2 — independent arithmetic. The headline numbers are recomputed in
           plain Python from the same inputs. If Excel shows something other
           than these when David opens the file, there is a bug in a formula.
"""

import re
import openpyxl

PATH = "Agently_Unit_Economics_Model_v1.xlsx"
wb = openpyxl.load_workbook(PATH)

# ---------------------------------------------------------------- Part 1
ref_re = re.compile(r"(?:'([^']+)'!)?\$?([A-Z]{1,2})\$?(\d+)")
problems = []
checked = 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            v = cell.value
            if not (isinstance(v, str) and v.startswith("=")):
                continue
            body = re.sub(r'"[^"]*"', '""', v)  # strip string literals
            for sheet_name, col, rownum in ref_re.findall(body):
                target_ws = wb[sheet_name] if sheet_name else ws
                tgt = target_ws[f"{col}{rownum}"]
                checked += 1
                if tgt.value is None:
                    problems.append(
                        f"{ws.title}!{cell.coordinate} -> "
                        f"{sheet_name or ws.title}!{col}{rownum} is EMPTY  ({v[:70]})")

print("=" * 72)
print("PART 1 — FORMULA REFERENCE INTEGRITY")
print("=" * 72)
print(f"references resolved: {checked}")
if problems:
    print(f"BROKEN REFERENCES: {len(problems)}")
    for p in problems[:40]:
        print("  !", p)
else:
    print("BROKEN REFERENCES: 0  — every reference points at a populated cell")

# ---------------------------------------------------------------- Part 2
# Inputs, read straight back out of sheet 1 so this cannot drift from the file
s1 = wb["1_Inputs"]
vals = {}
for r in range(1, s1.max_row + 1):
    lab = s1[f"A{r}"].value
    val = s1[f"B{r}"].value
    if isinstance(lab, str) and not isinstance(val, str) and val is not None:
        vals[lab.strip()] = val

g = lambda k: vals[k]
in_price = g("Input price per 1M tokens (USD)")
out_price = g("Output price per 1M tokens (USD)")
fx = g("USD → EUR conversion rate")
in_tok = g("Average INPUT tokens per call")
out_tok = g("Average OUTPUT tokens per call")
infra = g("Non-LLM infra cost per call (Vercel, Supabase)")
cpc = g("Credits charged per call (creator-set)")
fee = g("Platform fee — share WE keep")
creator = g("Creator share — share THEY get")
spct = g("Stripe percentage fee (EU cards)")
sfix = g("Stripe fixed fee per charge")

cost_in = (in_tok / 1_000_000) * in_price * fx
cost_out = (out_tok / 1_000_000) * out_price * fx
cost_call = cost_in + cost_out + infra
cost_credit = cost_call / cpc

print()
print("=" * 72)
print("PART 2 — EXPECTED VALUES  (what Excel must show on opening)")
print("=" * 72)
print(f"  Cost per call                       €{cost_call:,.4f}")
print(f"  Cost per credit                     €{cost_credit:,.4f}")
print(f"  Min viable credit price (cost/13.5%) €{cost_credit/(fee-spct):,.4f}")
print()

print("  TIER MARGINS")
print(f"  {'tier':<14}{'price':>8}{'credits':>9}{'€/credit':>11}"
      f"{'break-even':>12}{'net @35%':>11}{'net @100%':>11}")
for name, pk, ck in [("Basic", "Basic tier — monthly price", "Basic tier — monthly credits granted"),
                     ("Pro", "Pro tier — monthly price", "Pro tier — monthly credits granted"),
                     ("Professional", "Professional tier — monthly price",
                      "Professional tier — monthly credits granted")]:
    price = g(pk)
    creds = g(ck)
    keep = price * (1 - creator) - (price * spct + sfix)
    full_cogs = creds * cost_credit
    be = keep / full_cogs if full_cogs else 0
    net35 = keep - creds * 0.35 * cost_credit
    net100 = keep - full_cogs
    print(f"  {name:<14}€{price:>6.2f}{creds:>9,}  €{price/creds:>8.4f}"
          f"{be:>11.1%}  €{net35:>8.2f}  €{net100:>8.2f}")

print()
print("  FIX 1 — creators paid on NET, per €100 of revenue, Professional credit rate")
prof_p = g("Professional tier — monthly price")
prof_c = g("Professional tier — monthly credits granted")
cred_per_100 = 100 / (prof_p / prof_c)
for u in (0.10, 0.35, 0.80, 1.00):
    cogs = cred_per_100 * u * cost_credit
    today = 100 * fee - cogs - 100 * spct
    fix1 = (100 - cogs - 100 * spct) * fee
    print(f"    utilisation {u:>5.0%}   today: €{today:>8.2f}    fix 1: €{fix1:>7.2f}")

print()
print("  FIX 1 — per Professional member per month")
for u in (0.10, 0.35, 0.80):
    cogs = prof_c * u * cost_credit
    today = prof_p * (1 - creator) - (prof_p * spct + sfix) - cogs
    fix1 = (prof_p - cogs - (prof_p * spct + sfix)) * (1 - creator)
    print(f"    utilisation {u:>5.0%}   today: €{today:>8.2f}    fix 1: €{fix1:>7.2f}")

print()
print("=" * 72)
print("NOTE: this file was NOT machine-recalculated — LibreOffice cannot load")
print("any xlsx in this build environment. Excel/Numbers will compute the")
print("formulas on open. Check the four cells on sheet 7 against the numbers")
print("above; a mismatch means a formula bug, not a rounding difference.")
print("=" * 72)
