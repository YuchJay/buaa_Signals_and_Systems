"""Draw sample pairings for the course's discrete convolution calculations."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "figures" / "04-convolution" / "examples"
INK = "#202124"
ACCENT = "#A33A32"
SECONDARY = "#356A8A"
GRAY = "#777777"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.edgecolor": INK,
        "mathtext.fontset": "stix",
        "savefig.transparent": True,
    }
)


def save(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / filename, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def paired_rows(output_indices, columns, x_values, h_values, filename, *, symbolic=False):
    """Each box pairs x[k] with h[n-k] at one unchanged horizontal index."""
    fig, axes = plt.subplots(
        len(output_indices), 1, figsize=(8.4, 1.05 * len(output_indices) + 0.35)
    )
    for ax, n in zip(np.atleast_1d(axes), output_indices):
        ax.set_xlim(min(columns) - 2.25, max(columns) + 0.6)
        ax.set_ylim(-0.05, 1.2)
        ax.axis("off")
        left = min(columns) - 1.05
        ax.text(min(columns) - 2.1, 1.04, rf"$n={n}$", color=INK, fontsize=14, va="center")
        ax.text(left, 0.65, r"$x[k]$", ha="right", va="center", color=ACCENT, fontsize=13)
        ax.text(left, 0.22, r"$h[n-k]$", ha="right", va="center", color=SECONDARY, fontsize=13)
        ax.text(left, 1.04, r"$k$", ha="right", va="center", color=GRAY, fontsize=11)
        for k in columns:
            x = x_values.get(k)
            if symbolic:
                h = 1 if k <= n else None
            else:
                h = h_values.get(n - k)
            if x is not None and h is not None:
                ax.add_patch(
                    FancyBboxPatch(
                        (k - 0.31, 0.02),
                        0.62,
                        0.82,
                        boxstyle="round,pad=0.04,rounding_size=0.1",
                        facecolor="#F5EEE6",
                        edgecolor=GRAY,
                        linewidth=0.75,
                    )
                )
            ax.text(k, 1.04, str(k), ha="center", va="center", color=GRAY, fontsize=11)
            ax.text(
                k, 0.65, f"${x}$" if x is not None else "–",
                ha="center", va="center", color=ACCENT if x is not None else GRAY,
                fontsize=14,
            )
            ax.text(
                k, 0.22, f"${h}$" if h is not None else "–",
                ha="center", va="center", color=SECONDARY if h is not None else GRAY,
                fontsize=14,
            )
        ax.plot([min(columns) - 0.5, max(columns) + 0.5], [0.9, 0.9], color="#DDDDDD", lw=0.6)
    fig.subplots_adjust(hspace=0.25, left=0.02, right=0.995, bottom=0.02, top=0.99)
    save(fig, filename)


def finite_sliding_figures():
    x = {-1: 3, 0: 2, 1: 1, 2: -1}
    h = {-1: 1, 0: 1, 1: 2, 2: -1}
    columns = list(range(-4, 6))
    paired_rows([-2, -1, 0, 1], columns, x, h, "lti-sliding-entering.pdf")
    paired_rows([2, 3, 4], columns, x, h, "lti-sliding-leaving.pdf")


def sequence_axis(ax, indices, values, title, *, ylim, color=ACCENT):
    markers, stems, _ = ax.stem(indices, values, basefmt=" ")
    plt.setp(markers, color=color, markersize=5)
    plt.setp(stems, color=color, linewidth=1.4)
    ax.axhline(0, color=INK, lw=0.75)
    ax.axvline(0, color=INK, lw=0.6)
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.grid(axis="y", color="#DDDDDD", lw=0.5)
    ax.set_xlim(min(indices) - 0.7, max(indices) + 0.7)
    ax.set_ylim(*ylim)
    ax.set_xticks(indices)
    ax.set_yticks(np.arange(np.ceil(ylim[0]), np.floor(ylim[1]) + 1))
    ax.set_xlabel(r"$n$", loc="right")
    ax.set_title(title)
    for n, value in zip(indices, values):
        # Put the n=0 annotation beside its stem to avoid the vertical axis.
        x_offset = 0.13 if n == 0 else 0
        alignment = "left" if n == 0 else "center"
        y_offset = 0.2 if value >= 0 else -0.25
        ax.text(n + x_offset, value + y_offset, f"${value}$", color=INK, ha=alignment)


def interior_zero_figures():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.65))
    sequence_axis(
        axes[0], np.arange(-1, 3), [1, 2, 1, 1], r"$x[n]$", ylim=(-0.4, 2.6)
    )
    sequence_axis(
        axes[1], np.arange(0, 6), [1, -1, 0, 0, -1, 1], r"$h[n]$",
        ylim=(-1.6, 1.6), color=SECONDARY,
    )
    fig.tight_layout(pad=0.85)
    save(fig, "interior-zeros-given.pdf")

    fig, ax = plt.subplots(figsize=(6.9, 2.8))
    sequence_axis(
        ax, np.arange(-1, 8), [1, 1, -1, 0, -2, -1, 1, 0, 1], r"$y[n]$",
        ylim=(-2.7, 1.7),
    )
    fig.tight_layout(pad=0.85)
    save(fig, "interior-zeros-answer.pdf")


def geometric_sliding_figure():
    x = {0: 1, 1: "a", 2: "a^2", 3: "a^3", 4: "a^4"}
    paired_rows(
        [0, 1, 2, 3], list(range(-2, 5)), x, {},
        "geometric-step-sliding.pdf", symbolic=True,
    )


def main():
    finite_sliding_figures()
    interior_zero_figures()
    geometric_sliding_figure()
    print(f"Generated 5 figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
