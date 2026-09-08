"""Generate figures for the worked examples appended to Chapter 2."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "figures" / "02-signals" / "examples"
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
        "lines.linewidth": 1.7,
        "savefig.transparent": True,
    }
)


def finish_axis(ax, *, xlabel, ylabel, xlim, ylim, xticks, yticks):
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.grid(color=LIGHT_GRAY, linewidth=0.45, alpha=0.65)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xlabel(xlabel, loc="right")
    ax.set_ylabel(ylabel, rotation=0, loc="top")


def save(fig, filename):
    fig.tight_layout(pad=0.8)
    fig.savefig(OUTPUT_DIR / filename, bbox_inches="tight")
    plt.close(fig)


def plot_triangle(ax, points, title, xticks):
    x, y = zip(*points)
    ax.plot(x, y, color=ACCENT)
    ax.scatter(x, y, s=14, color=ACCENT, zorder=3)
    ax.set_title(title)
    finish_axis(
        ax,
        xlabel=r"$t$",
        ylabel=r"$x$",
        xlim=(min(xticks) - 0.45, max(xticks) + 0.45),
        ylim=(-0.16, 1.25),
        xticks=xticks,
        yticks=[0, 1],
    )


def affine_triangle_figures():
    fig, ax = plt.subplots(figsize=(4.4, 2.35))
    plot_triangle(ax, [(0, 0), (3, 1), (6, 0)], r"$x(t)$", [0, 3, 6])
    save(fig, "affine-triangle-given.pdf")

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.35))
    plot_triangle(
        axes[0], [(-2, 0), (-1, 1), (0, 0)], r"$x(3t+6)$", [-2, -1, 0]
    )
    plot_triangle(
        axes[1], [(0, 0), (1, 1), (2, 0)], r"$x(-3t+6)$", [0, 1, 2]
    )
    save(fig, "affine-triangle-answer.pdf")


def plot_step(ax, *, title, xlim, xticks, segments, ylabel):
    for left, right, height in segments:
        ax.plot([left, right], [height, height], color=ACCENT)
        ax.plot([left, left], [0, height], color=ACCENT, linewidth=1.0)
        ax.plot([right, right], [0, height], color=ACCENT, linewidth=1.0)
    ax.set_title(title)
    finish_axis(
        ax,
        xlabel=r"$t$",
        ylabel=ylabel,
        xlim=xlim,
        ylim=(-0.25, 2.35),
        xticks=xticks,
        yticks=[0, 1, 2],
    )


def recover_original_figures():
    fig, ax = plt.subplots(figsize=(4.8, 2.35))
    plot_step(
        ax,
        title=r"$y(t)=x(3-2t)$",
        xlim=(-0.6, 5.0),
        xticks=[0, 1, 2, 3, 4],
        segments=[(2, 3, 1), (3, 4, 2)],
        ylabel=r"$y$",
    )
    save(fig, "recover-original-given.pdf")

    fig, ax = plt.subplots(figsize=(4.8, 2.35))
    plot_step(
        ax,
        title=r"$x(t)=y((3-t)/2)$",
        xlim=(-5.8, 0.8),
        xticks=[-5, -4, -3, -2, -1, 0],
        segments=[(-5, -3, 2), (-3, -1, 1)],
        ylabel=r"$x$",
    )
    save(fig, "recover-original-answer.pdf")


def plot_sequence(ax, indices, values, *, title, xlim, xticks):
    markerline, stemlines, _ = ax.stem(indices, values, basefmt=" ")
    plt.setp(markerline, color=ACCENT, markersize=5)
    plt.setp(stemlines, color=ACCENT, linewidth=1.4)
    ax.set_title(title)
    finish_axis(
        ax,
        xlabel=r"$n$",
        ylabel=r"$x$",
        xlim=xlim,
        ylim=(-0.75, 1.28),
        xticks=xticks,
        yticks=[-0.5, 0, 0.5, 1],
    )


def discrete_transform_figures():
    indices = np.arange(-2, 4)
    values = np.array([0.5, -0.5, 1, 1, 1, 1])

    fig, ax = plt.subplots(figsize=(5.4, 2.55))
    plot_sequence(
        ax,
        indices,
        values,
        title=r"$x[n]$",
        xlim=(-3.1, 4.1),
        xticks=np.arange(-3, 5),
    )
    save(fig, "discrete-transform-given.pdf")

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.55), sharey=True)
    shifted_indices = np.arange(1, 7)
    plot_sequence(
        axes[0],
        shifted_indices,
        values,
        title=r"$x[n-3]$",
        xlim=(-0.2, 7.0),
        xticks=np.arange(0, 8),
    )
    reversed_values = np.array([1, 1, 1, 1, -0.5, 0.5])
    plot_sequence(
        axes[1],
        shifted_indices,
        reversed_values,
        title=r"$x[4-n]$",
        xlim=(-0.2, 7.0),
        xticks=np.arange(0, 8),
    )
    save(fig, "discrete-transform-answer.pdf")


def main():
    affine_triangle_figures()
    recover_original_figures()
    discrete_transform_figures()
    print(f"Generated 6 figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
