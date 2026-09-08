"""Generate diagnostic figures for the worked examples in Chapter 3."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "figures" / "03-systems-and-lti" / "examples"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INK = "#202124"
MUTED = "#6B7280"
LIGHT = "#E5E7EB"
ACCENT = "#A33A32"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "mathtext.fontset": "stix",
        "savefig.transparent": True,
    }
)


def save(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def box(ax, xy, width, height, text, *, edge=INK, face="white"):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.025,rounding_size=0.025",
        linewidth=1.2,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center")


def arrow(ax, start, end, label="", *, color=INK):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=12, color=color))
    if label:
        ax.text(
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2 + 0.045,
            label,
            ha="center",
            va="bottom",
            color=color,
        )


def finish_diagram(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def linearity_figure():
    fig, ax = plt.subplots(figsize=(7.0, 2.25))
    box(ax, (0.03, 0.38), 0.18, 0.24, r"$x(t)$")
    box(ax, (0.39, 0.38), 0.22, 0.24, r"$\mathcal{T}$")
    box(ax, (0.77, 0.38), 0.20, 0.24, r"$y(t)$")
    arrow(ax, (0.21, 0.50), (0.39, 0.50), r"$\times a$")
    arrow(ax, (0.61, 0.50), (0.77, 0.50), r"$\times a^2$", color=ACCENT)
    ax.text(0.5, 0.82, r"$\mathcal{T}\{a x\}=a^2\mathcal{T}\{x\}$", ha="center", color=ACCENT, fontsize=11)
    ax.text(0.5, 0.16, r"linearity would require $\times a$ at the output", ha="center", color=MUTED)
    finish_diagram(ax)
    save(fig, "linearity-product-integral-answer.pdf")


def stem(ax, n, *, color=ACCENT, label=None):
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.vlines(n, 0, 1, color=color, linewidth=1.5)
    ax.plot(n, 1, "o", color=color, markersize=4)
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.15, 1.3)
    ax.set_xticks(range(0, 6))
    ax.set_yticks([0, 1])
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.set_xlabel(r"$n$", loc="right")
    if label:
        ax.set_title(label, fontsize=9)


def time_invariance_figure():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.35), sharey=True)
    stem(axes[0], 2, label=r"shift input, then apply $\mathcal{T}$: $\delta[n-2]$")
    stem(axes[1], 4, label=r"apply $\mathcal{T}$, then shift output: $\delta[n-4]$")
    fig.tight_layout(pad=0.7)
    save(fig, "time-invariance-reversal-answer.pdf")


def causality_figure():
    fig, ax = plt.subplots(figsize=(6.7, 2.05))
    ax.axhline(0, color=INK, linewidth=1)
    ax.add_patch(FancyArrowPatch((-4.5, 0), (5.0, 0), arrowstyle="->", mutation_scale=12, color=INK))
    ax.plot([-4.2, 4], [0, 0], linewidth=6, color=LIGHT, solid_capstyle="butt", zorder=0)
    ax.plot([2, 4], [0, 0], linewidth=6, color=ACCENT, solid_capstyle="butt", zorder=1)
    for n in [2, 3, 4]:
        ax.vlines(n, -0.12, 0.12, color=INK, linewidth=1)
        ax.text(n, -0.23, rf"${n}$", ha="center", va="top")
    ax.text(2, 0.23, r"current $n_0=2$", ha="center", color=INK)
    ax.text(3, 0.50, r"future samples used by $y[2]$", ha="center", color=ACCENT)
    ax.annotate("", xy=(3, 0.11), xytext=(3, 0.40), arrowprops={"arrowstyle": "->", "color": ACCENT})
    ax.text(-1.0, -0.40, r"summation interval: $k\leq 2n_0=4$", ha="center", color=MUTED)
    ax.set_xlim(-4.6, 5.1)
    ax.set_ylim(-0.55, 0.72)
    ax.axis("off")
    save(fig, "causality-variable-limit-answer.pdf")


def main():
    linearity_figure()
    time_invariance_figure()
    causality_figure()
    print(f"Generated 3 figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
