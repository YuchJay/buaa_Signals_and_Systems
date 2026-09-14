"""Generate figures for the pre-convolution-formula LTI example in Chapter 4."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "figures" / "04-convolution" / "examples"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INK = "#202124"
LIGHT_GRAY = "#D8D8D8"
ACCENT = "#A33A32"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "mathtext.fontset": "stix",
        "xtick.color": INK,
        "ytick.color": INK,
        "savefig.transparent": True,
    }
)


def plot_sequence(ax, indices, values, title, *, ylim):
    markerline, stemlines, _ = ax.stem(indices, values, basefmt=" ")
    plt.setp(markerline, color=ACCENT, markersize=4.5)
    plt.setp(stemlines, color=ACCENT, linewidth=1.35)
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.grid(color=LIGHT_GRAY, linewidth=0.45, alpha=0.65)
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.set_xlim(min(indices) - 0.7, max(indices) + 0.7)
    ax.set_ylim(*ylim)
    ax.set_xticks(indices)
    ax.set_xlabel(r"$n$", loc="right")
    ax.set_title(title)


def save(fig, filename):
    fig.tight_layout(pad=0.8)
    fig.savefig(OUTPUT_DIR / filename, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def given_figure():
    indices = np.arange(-1, 3)
    x = np.array([3, 2, 1, -1])
    h = np.array([1, 1, 2, -1])

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.5))
    plot_sequence(axes[0], indices, x, r"input $x[n]$", ylim=(-1.6, 3.7))
    plot_sequence(axes[1], indices, h, r"impulse response $h[n]$", ylim=(-1.6, 3.7))
    save(fig, "lti-superposition-given.pdf")


def answer_figure():
    indices = np.arange(-2, 5)
    y = np.array([3, 5, 9, 1, -1, -3, 1])

    fig, ax = plt.subplots(figsize=(6.2, 2.65))
    plot_sequence(ax, indices, y, r"output $y[n]$", ylim=(-4.0, 10.2))
    for n, value in zip(indices, y):
        offset = 0.45 if value >= 0 else -0.65
        x_position = n + 0.08 if n == 0 else n
        alignment = "left" if n == 0 else "center"
        ax.text(
            x_position,
            value + offset,
            rf"${value}$",
            ha=alignment,
            va="center",
            color=INK,
        )
    save(fig, "lti-superposition-answer.pdf")


def geometric_step_given_figure():
    indices = np.arange(-2, 9)
    x = np.where(indices >= 0, 0.5**indices, 0.0)
    h = np.where(indices >= 0, 1.0, 0.0)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.5))
    plot_sequence(axes[0], indices, x, r"$x[n]=(1/2)^n u[n]$", ylim=(-0.15, 1.25))
    plot_sequence(axes[1], indices, h, r"$h[n]=u[n]$", ylim=(-0.15, 1.25))
    axes[1].annotate(
        "continues",
        xy=(8.5, 1.0),
        xytext=(6.2, 1.13),
        arrowprops={"arrowstyle": "->", "color": INK},
        color=INK,
        fontsize=8,
    )
    save(fig, "geometric-step-given.pdf")


def geometric_step_answer_figure():
    indices = np.arange(-2, 9)
    y = np.where(indices >= 0, 2 * (1 - 0.5 ** (indices + 1)), 0.0)

    fig, ax = plt.subplots(figsize=(6.2, 2.65))
    plot_sequence(ax, indices, y, r"$y[n]=2(1-(1/2)^{n+1})u[n]$", ylim=(-0.2, 2.25))
    ax.axhline(2, color=INK, linewidth=0.8, linestyle="--")
    ax.text(7.5, 2.05, r"limit $2$", ha="right", va="bottom", color=INK)
    save(fig, "geometric-step-answer.pdf")


def main():
    given_figure()
    answer_figure()
    geometric_step_given_figure()
    geometric_step_answer_figure()
    print(f"Generated 4 figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
