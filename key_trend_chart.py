import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

df = pd.read_csv("meridian_financials_2022_2025.csv")

# Annual aggregates
df["year"] = df["quarter"].str[:4].astype(int)
annual = df.groupby("year").agg(
    revenue=("revenue_usd_m", "sum"),
    op_margin=("operating_margin_pct", "mean"),
    fcf_margin=("fcf_margin_pct", "mean"),
).reset_index()
annual["revenue_growth"] = annual["revenue"].pct_change() * 100

years = annual["year"].tolist()
growth = annual["revenue_growth"].tolist()       # NaN for 2022, values for 2023-2025
op_margins = annual["op_margin"].tolist()
fcf_margins = annual["fcf_margin"].tolist()

# Only plot years where we have growth (2023-2025)
plot_years  = years[1:]
plot_growth = growth[1:]
plot_op     = op_margins[1:]
plot_fcf    = fcf_margins[1:]

# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#F8F9FA")
ax1.set_facecolor("#FFFFFF")

BAR_COLOR  = "#AED6F1"
OP_COLOR   = "#1A5276"
FCF_COLOR  = "#1E8449"
ANNO_COLOR = "#2C3E50"

# ── Bars: revenue growth ──────────────────────────────────────────────────────
x = np.arange(len(plot_years))
bars = ax1.bar(x, plot_growth, width=0.5, color=BAR_COLOR, zorder=2,
               label="Revenue growth YoY (%)")

# Value labels on bars
for bar, val in zip(bars, plot_growth):
    ax1.text(bar.get_x() + bar.get_width() / 2,
             val + 0.4, f"{val:.0f}%",
             ha="center", va="bottom", fontsize=12, fontweight="bold",
             color=ANNO_COLOR)

ax1.set_ylim(0, 35)
ax1.set_ylabel("Revenue growth YoY (%)", fontsize=11, color=ANNO_COLOR)
ax1.set_yticks(range(0, 36, 5))
ax1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax1.set_xticks(x)
ax1.set_xticklabels([str(y) for y in plot_years], fontsize=13, fontweight="bold")
ax1.tick_params(axis="y", labelcolor=ANNO_COLOR)
ax1.grid(axis="y", alpha=0.25, zorder=0)
ax1.spines[["top", "right"]].set_visible(False)

# ── Right axis: margins ───────────────────────────────────────────────────────
ax2 = ax1.twinx()
ax2.set_facecolor("#FFFFFF")
ax2.plot(x, plot_op,  color=OP_COLOR,  lw=2.5, marker="o", ms=8,
         label="Operating margin (%)", zorder=3)
ax2.plot(x, plot_fcf, color=FCF_COLOR, lw=2.5, marker="s", ms=8,
         linestyle="--", label="FCF margin (%)", zorder=3)

# Value labels on lines
for xi, (om, fm) in enumerate(zip(plot_op, plot_fcf)):
    ax2.text(xi + 0.06, om + 0.5, f"{om:.1f}%", fontsize=9,
             color=OP_COLOR, fontweight="bold")
    ax2.text(xi + 0.06, fm - 1.3, f"{fm:.1f}%", fontsize=9,
             color=FCF_COLOR, fontweight="bold")

ax2.set_ylim(0, 25)
ax2.set_ylabel("Margin (%)", fontsize=11, color=ANNO_COLOR)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.tick_params(axis="y", labelcolor=ANNO_COLOR)
ax2.spines[["top", "left"]].set_visible(False)

# ── Arrow annotation: the divergence ─────────────────────────────────────────
ax1.annotate("", xy=(2, 10.5), xytext=(0, 28.5),
             arrowprops=dict(arrowstyle="-|>", color="#C0392B", lw=2.0))
ax1.text(2.12, 19, "Growth\ndecelerating", fontsize=9.5, color="#C0392B",
         fontweight="bold", ha="left")

ax2.annotate("", xy=(2, 12.0), xytext=(0, 7.1),
             arrowprops=dict(arrowstyle="-|>", color=OP_COLOR, lw=2.0))
ax2.text(2.12, 10.2, "Margins\nexpanding", fontsize=9.5, color=OP_COLOR,
         fontweight="bold", ha="left")

# ── Titles and legend ─────────────────────────────────────────────────────────
fig.suptitle(
    "Meridian Technologies — The Core Strategic Tension",
    fontsize=14, fontweight="bold", color=ANNO_COLOR, y=1.01
)
ax1.set_title(
    "Revenue growth has decelerated every year.  Margins have expanded every year.\n"
    "The business is becoming more profitable — and slower.",
    fontsize=9.5, color="#555555", pad=8
)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
           loc="upper right", fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig("key_trend_chart.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Saved key_trend_chart.png")
