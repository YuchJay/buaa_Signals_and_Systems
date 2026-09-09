"""Generate diagnostic figures for the worked examples in Chapter 3."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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


def memoryless_figure():
    fig, ax = plt.subplots(figsize=(6.4, 1.95))
    ax.add_patch(FancyArrowPatch((-0.5, 0), (3.2, 0), arrowstyle="->", mutation_scale=12, color=INK))
    for n in [0, 1, 2, 3]:
        ax.vlines(n, -0.10, 0.10, color=INK, linewidth=1)
        ax.text(n, -0.20, rf"${n}$", ha="center", va="top")
    ax.plot(1, 0, "o", color=INK, markersize=6)
    ax.plot(2, 0, "o", color=ACCENT, markersize=6)
    ax.annotate(
        "",
        xy=(2, 0.08),
        xytext=(1, 0.08),
        arrowprops={"arrowstyle": "->", "color": ACCENT, "connectionstyle": "arc3,rad=-0.35"},
    )
    ax.text(1, 0.48, r"output time $n_0=1$", ha="center", color=INK)
    ax.text(2, 0.48, r"input read at $2n_0=2$", ha="center", color=ACCENT)
    ax.text(1.5, 0.72, r"$y[1]=x[2]$", ha="center", color=ACCENT, fontsize=11)
    ax.set_xlim(-0.6, 3.3)
    ax.set_ylim(-0.42, 0.85)
    ax.axis("off")
    save(fig, "memoryless-time-scaling-answer.pdf")


def invertibility_figure():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.25))

    ax = axes[0]
    box(ax, (0.02, 0.38), 0.22, 0.24, r"$x(t)$")
    box(ax, (0.39, 0.38), 0.22, 0.24, r"$\int_{-\infty}^{t}$")
    box(ax, (0.76, 0.38), 0.22, 0.24, r"$y(t)$")
    arrow(ax, (0.24, 0.50), (0.39, 0.50))
    arrow(ax, (0.61, 0.50), (0.76, 0.50))
    ax.add_patch(
        FancyArrowPatch(
            (0.87, 0.33),
            (0.13, 0.33),
            arrowstyle="->",
            mutation_scale=12,
            color=ACCENT,
            connectionstyle="arc3,rad=-0.35",
        )
    )
    ax.text(0.50, 0.08, r"inverse: $x(t)=\mathrm{d}y(t)/\mathrm{d}t$", ha="center", color=ACCENT)
    ax.set_title("integrator", color=MUTED)
    finish_diagram(ax)

    ax = axes[1]
    box(ax, (0.02, 0.60), 0.25, 0.20, r"$x(t)$")
    box(ax, (0.02, 0.20), 0.25, 0.20, r"$x(t)+C$")
    box(ax, (0.42, 0.38), 0.20, 0.24, r"$\mathrm{d}/\mathrm{d}t$")
    box(ax, (0.76, 0.38), 0.22, 0.24, r"$y(t)$", edge=ACCENT)
    arrow(ax, (0.27, 0.70), (0.42, 0.54))
    arrow(ax, (0.27, 0.30), (0.42, 0.46))
    arrow(ax, (0.62, 0.50), (0.76, 0.50), color=ACCENT)
    ax.text(0.50, 0.08, "constant information is lost", ha="center", color=ACCENT)
    ax.set_title("differentiator", color=MUTED)
    finish_diagram(ax)

    fig.tight_layout(pad=0.8)
    save(fig, "invertibility-calculus-answer.pdf")


def stability_figure():
    indices = np.arange(-1, 9)
    accumulator = np.where(indices >= 0, indices + 1, 0)
    difference = np.where(indices == 0, 1, 0)

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.45))
    for ax, values, title in [
        (axes[0], accumulator, r"accumulator: $(n+1)u[n]$"),
        (axes[1], difference, r"difference: $\delta[n]$"),
    ]:
        markerline, stemlines, _ = ax.stem(indices, values, basefmt=" ")
        plt.setp(markerline, color=ACCENT, markersize=4)
        plt.setp(stemlines, color=ACCENT, linewidth=1.3)
        ax.axhline(0, color=INK, linewidth=0.8)
        ax.set_xlim(-1.5, 8.7)
        ax.set_xticks([-1, 0, 2, 4, 6, 8])
        ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
        ax.set_xlabel(r"$n$", loc="right")
        ax.set_title(title)
    axes[0].set_ylim(-0.5, 9.8)
    axes[0].set_yticks([0, 2, 4, 6, 8])
    axes[1].set_ylim(-0.1, 1.25)
    axes[1].set_yticks([0, 1])
    fig.tight_layout(pad=0.7)
    save(fig, "stability-sum-difference-answer.pdf")


def main():
    linearity_figure()
    time_invariance_figure()
    causality_figure()
    memoryless_figure()
    invertibility_figure()
    stability_figure()
    print(f"Generated 6 figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
