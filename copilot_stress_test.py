import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

# ── Constants ────────────────────────────────────────────────────────────────
PRICE_PER_SEAT_MONTH = 40          # $40/seat/month (stated Q2 2025 call)
ENTERPRISE_LOGOS     = 140         # Q4 2025
AVG_SEATS_PER_LOGO   = 500         # proxy: enterprise ACV $295K / $40 / 12 ≈ 615; use 500 conservatively
MIDMARKET_LOGOS      = 3_200
AVG_MM_SEATS         = 80          # smaller deployments
Q4_2025_COPILOT_ARR  = 3.5        # $M, stated Q4 2025 call
Q4_2025_COPILOT_SEATS = 710

# Implied TAM ceiling checks
ENTERPRISE_SEAT_TAM  = ENTERPRISE_LOGOS * AVG_SEATS_PER_LOGO  # 70,000
MIDMARKET_SEAT_TAM   = MIDMARKET_LOGOS  * AVG_MM_SEATS         # 256,000

# ── Quarters ─────────────────────────────────────────────────────────────────
quarters = [
    "Q4'25", "Q1'26", "Q2'26", "Q3'26", "Q4'26",
    "Q1'27", "Q2'27", "Q3'27", "Q4'27"
]
n = len(quarters)
idx = np.arange(n)

# ── Base-platform ARR (ex-Copilot) ───────────────────────────────────────────
# Enterprise: 21% YoY → decelerates to 18% as base grows
# Mid-market: 6% YoY → decelerates to 4% (NRR compression)
# SMB: -23% YoY → stabilises at -15%
def grow_quarterly(start, annual_rates):
    vals = [start]
    for i, ar in enumerate(annual_rates):
        vals.append(vals[-1] * (1 + ar) ** 0.25)
    return vals[:n]

ent_annual   = [0.21, 0.21, 0.20, 0.19, 0.18, 0.18, 0.18, 0.18]
mm_annual    = [0.06, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04]
smb_annual   = [-0.23, -0.20, -0.18, -0.17, -0.15, -0.15, -0.15, -0.15]

ent_arr = grow_quarterly(167, ent_annual)   # $M
mm_arr  = grow_quarterly(194, mm_annual)
smb_arr = grow_quarterly(52,  smb_annual)

base_platform_arr = [e + m + s for e, m, s in zip(ent_arr, mm_arr, smb_arr)]

# ── Copilot ARR scenarios ─────────────────────────────────────────────────────
# Seats at end of each quarter; ARR = seats * $40 * 12 / 1e6

# Bear: stalls — Asana/Atlassian competition blunts adoption, no consumption pricing
#   attach rate on enterprise renewals slides back to ~25%
bear_seats = [710, 950, 1_200, 1_500, 1_800, 2_100, 2_400, 2_700, 3_000]

# Base: holds 44% enterprise attach, mid-market starts adopting after resource mgmt ships Q2'26
#   reaches ~18k seats by Q4'27 (~26% of enterprise TAM + small mid-market start)
base_seats = [710, 1_500, 2_800, 4_500, 6_500, 9_000, 12_000, 15_500, 18_500]

# Bull: consumption pricing Q3'26 drives higher velocity; agent-builder (Q2'26) accelerates
#   enterprise expansion + meaningful mid-market penetration
#   reaches ~35k seats by Q4'27 (~50% ent TAM + ~5% mid-market TAM)
bull_seats = [710, 2_200, 5_000, 9_500, 15_000, 20_000, 26_000, 31_000, 36_000]

def seats_to_arr(seats):
    return [s * PRICE_PER_SEAT_MONTH * 12 / 1e6 for s in seats]

bear_cop = seats_to_arr(bear_seats)
base_cop = seats_to_arr(base_seats)
bull_cop = seats_to_arr(bull_seats)

# ── Total company ARR ────────────────────────────────────────────────────────
total_bear = [p + c for p, c in zip(base_platform_arr, bear_cop)]
total_base = [p + c for p, c in zip(base_platform_arr, base_cop)]
total_bull = [p + c for p, c in zip(base_platform_arr, bull_cop)]

# ── YoY ARR growth (Q4 to Q4) ───────────────────────────────────────────────
# Q4 2025 baseline total ARR = $412.8M (stated)
Q4_2025_TOTAL = 412.8

def yoy_growth(total_arr_series):
    # index 0 = Q4'25, index 4 = Q4'26, index 8 = Q4'27
    g26 = (total_arr_series[4] - Q4_2025_TOTAL) / Q4_2025_TOTAL * 100
    g27 = (total_arr_series[8] - total_arr_series[4]) / total_arr_series[4] * 100
    return round(g26, 1), round(g27, 1)

bear_g26, bear_g27 = yoy_growth(total_bear)
base_g26, base_g27 = yoy_growth(total_base)
bull_g26, bull_g27 = yoy_growth(total_bull)

# ── What Copilot ARR is needed to hit 15% growth in 2026? ───────────────────
target_15pct_arr_2026 = Q4_2025_TOTAL * 1.15   # $474.7M
platform_q4_2026      = base_platform_arr[4]    # base platform only
copilot_needed_15pct  = target_15pct_arr_2026 - platform_q4_2026
seats_needed_15pct    = copilot_needed_15pct * 1e6 / (PRICE_PER_SEAT_MONTH * 12)
pct_ent_tam_needed    = seats_needed_15pct / ENTERPRISE_SEAT_TAM * 100

# ── Plot ─────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 14))
fig.patch.set_facecolor("#F8F9FA")
gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

colors = {"bear": "#C0392B", "base": "#2980B9", "bull": "#27AE60"}
lw = 2.2

# ── Panel 1: Copilot ARR by scenario ─────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor("#FFFFFF")
ax1.plot(idx, bear_cop, color=colors["bear"], lw=lw, marker="o", ms=5, label="Bear")
ax1.plot(idx, base_cop, color=colors["base"], lw=lw, marker="o", ms=5, label="Base")
ax1.plot(idx, bull_cop, color=colors["bull"], lw=lw, marker="o", ms=5, label="Bull")
ax1.axhline(copilot_needed_15pct, color="black", lw=1.2, ls="--")
ax1.text(n - 1, copilot_needed_15pct + 1.5,
         f"  Needed for 15% ARR growth in 2026:\n  ${copilot_needed_15pct:.0f}M Copilot ARR",
         fontsize=7.5, color="black")
ax1.set_title("AI Copilot ARR ($M)", fontweight="bold", fontsize=11)
ax1.set_xticks(idx); ax1.set_xticklabels(quarters, fontsize=8)
ax1.set_ylabel("$M ARR"); ax1.legend(fontsize=8); ax1.grid(axis="y", alpha=0.3)

# ── Panel 2: Paying seat count ───────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor("#FFFFFF")
ax2.plot(idx, bear_seats, color=colors["bear"], lw=lw, marker="o", ms=5, label="Bear")
ax2.plot(idx, base_seats, color=colors["base"], lw=lw, marker="o", ms=5, label="Base")
ax2.plot(idx, bull_seats, color=colors["bull"], lw=lw, marker="o", ms=5, label="Bull")
ax2.axhline(seats_needed_15pct, color="black", lw=1.2, ls="--")
ax2.text(0.3, seats_needed_15pct + 200,
         f"  Seats needed for 15% growth: {seats_needed_15pct:,.0f} ({pct_ent_tam_needed:.0f}% of ent. TAM)",
         fontsize=7.5, color="black")
ax2.axhline(ENTERPRISE_SEAT_TAM, color="#7F8C8D", lw=1, ls=":", alpha=0.7)
ax2.text(0.1, ENTERPRISE_SEAT_TAM + 300, "  Enterprise seat TAM ceiling (70k)", fontsize=7, color="#7F8C8D")
ax2.set_title("Copilot Paying Seats", fontweight="bold", fontsize=11)
ax2.set_xticks(idx); ax2.set_xticklabels(quarters, fontsize=8)
ax2.set_ylabel("Seats"); ax2.legend(fontsize=8); ax2.grid(axis="y", alpha=0.3)

# ── Panel 3: Total company ARR ───────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor("#FFFFFF")
ax3.plot(idx, total_bear, color=colors["bear"], lw=lw, marker="o", ms=5, label="Bear")
ax3.plot(idx, total_base, color=colors["base"], lw=lw, marker="o", ms=5, label="Base")
ax3.plot(idx, total_bull, color=colors["bull"], lw=lw, marker="o", ms=5, label="Bull")
ax3.axhline(target_15pct_arr_2026, color="black", lw=1.2, ls="--")
ax3.text(n - 1, target_15pct_arr_2026 + 2,
         f"  15% growth target: ${target_15pct_arr_2026:.0f}M",
         fontsize=7.5, color="black", ha="right")
ax3.set_title("Total Company ARR ($M)", fontweight="bold", fontsize=11)
ax3.set_xticks(idx); ax3.set_xticklabels(quarters, fontsize=8)
ax3.set_ylabel("$M ARR"); ax3.legend(fontsize=8); ax3.grid(axis="y", alpha=0.3)

# ── Panel 4: Copilot as % of total ARR ───────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor("#FFFFFF")
bear_pct = [c / t * 100 for c, t in zip(bear_cop, total_bear)]
base_pct = [c / t * 100 for c, t in zip(base_cop, total_base)]
bull_pct = [c / t * 100 for c, t in zip(bull_cop, total_bull)]
ax4.plot(idx, bear_pct, color=colors["bear"], lw=lw, marker="o", ms=5, label="Bear")
ax4.plot(idx, base_pct, color=colors["base"], lw=lw, marker="o", ms=5, label="Base")
ax4.plot(idx, bull_pct, color=colors["bull"], lw=lw, marker="o", ms=5, label="Bull")
ax4.set_title("Copilot as % of Total ARR", fontweight="bold", fontsize=11)
ax4.set_xticks(idx); ax4.set_xticklabels(quarters, fontsize=8)
ax4.set_ylabel("% of ARR"); ax4.legend(fontsize=8); ax4.grid(axis="y", alpha=0.3)

# ── Panel 5: Summary table ────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[2, :])
ax5.axis("off")
ax5.set_facecolor("#FFFFFF")

table_data = [
    ["Scenario", "Copilot seats\nQ4'26", "Copilot ARR\nQ4'26 ($M)", "Total ARR\nQ4'26 ($M)",
     "YoY ARR\ngrowth 2026", "Copilot seats\nQ4'27", "Copilot ARR\nQ4'27 ($M)", "Total ARR\nQ4'27 ($M)",
     "YoY ARR\ngrowth 2027"],
    ["Bear\n(competition stalls adoption)",
     f"{bear_seats[4]:,}", f"${bear_cop[4]:.1f}M", f"${total_bear[4]:.0f}M",
     f"{bear_g26}%",
     f"{bear_seats[8]:,}", f"${bear_cop[8]:.1f}M", f"${total_bear[8]:.0f}M",
     f"{bear_g27}%"],
    ["Base\n(44% ent attach holds, MM starts)",
     f"{base_seats[4]:,}", f"${base_cop[4]:.1f}M", f"${total_base[4]:.0f}M",
     f"{base_g26}%",
     f"{base_seats[8]:,}", f"${base_cop[8]:.1f}M", f"${total_base[8]:.0f}M",
     f"{base_g27}%"],
    ["Bull\n(consumption pricing + agent builder)",
     f"{bull_seats[4]:,}", f"${bull_cop[4]:.1f}M", f"${total_bull[4]:.0f}M",
     f"{bull_g26}%",
     f"{bull_seats[8]:,}", f"${bull_cop[8]:.1f}M", f"${total_bull[8]:.0f}M",
     f"{bull_g27}%"],
    ["Needed for 15% growth in 2026",
     f"{seats_needed_15pct:,.0f}", f"${copilot_needed_15pct:.0f}M", f"${target_15pct_arr_2026:.0f}M",
     "15.0%", "—", "—", "—", "—"],
]

row_colors = [
    ["#D5D8DC"] * 9,
    ["#FADBD8"] * 9,
    ["#D6EAF8"] * 9,
    ["#D5F5E3"] * 9,
    ["#F9E79F"] * 9,
]

tbl = ax5.table(
    cellText=table_data,
    cellLoc="center",
    loc="center",
    cellColours=row_colors,
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)
tbl.scale(1, 2.6)
ax5.set_title("Scenario Summary — Copilot ARR vs. Company Growth Targets",
              fontweight="bold", fontsize=11, pad=12)

# ── Key insight annotations ───────────────────────────────────────────────────
fig.suptitle(
    "Meridian AI Copilot Stress Test  |  Q4 2025 – Q4 2027\n"
    "Base platform assumes: Enterprise +21%→18%, Mid-market +6%→4%, SMB –23%→–15%  |  Copilot: $40/seat/month",
    fontsize=9, color="#555555", y=0.98
)

plt.savefig("copilot_stress_test.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Saved copilot_stress_test.png")

# ── Print key numbers ─────────────────────────────────────────────────────────
print(f"\n── Key findings ──────────────────────────────────────────────────")
print(f"Q4 2025 starting point: {Q4_2025_COPILOT_SEATS} seats, ${Q4_2025_COPILOT_ARR}M ARR")
print(f"Enterprise seat TAM ceiling: {ENTERPRISE_SEAT_TAM:,} seats (${ENTERPRISE_SEAT_TAM * PRICE_PER_SEAT_MONTH * 12 / 1e6:.0f}M ARR)")
print(f"Mid-market seat TAM ceiling: {MIDMARKET_SEAT_TAM:,} seats (${MIDMARKET_SEAT_TAM * PRICE_PER_SEAT_MONTH * 12 / 1e6:.0f}M ARR)")
print(f"\nTo hit 15% ARR growth in 2026:")
print(f"  Target total ARR: ${target_15pct_arr_2026:.0f}M")
print(f"  Base platform (ex-Copilot) Q4'26: ${platform_q4_2026:.0f}M")
print(f"  Copilot ARR required:  ${copilot_needed_15pct:.0f}M")
print(f"  Seats required: {seats_needed_15pct:,.0f} ({pct_ent_tam_needed:.0f}% of enterprise TAM)")
print(f"\nScenario outcomes (YoY ARR growth):")
print(f"  Bear: 2026 = {bear_g26}%,  2027 = {bear_g27}%")
print(f"  Base: 2026 = {base_g26}%,  2027 = {base_g27}%")
print(f"  Bull: 2026 = {bull_g26}%,  2027 = {bull_g27}%")
