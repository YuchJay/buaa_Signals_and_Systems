"""Generate explanatory figures for Chapter 4 convolution formulas."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "figures" / "04-convolution"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INK = "#202124"
LIGHT_GRAY = "#D8D8D8"
ACCENT = "#A33A32"
SECONDARY = "#356A8A"

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


def style_axis(ax, *, xlim, ylim, xticks):
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.grid(color=LIGHT_GRAY, linewidth=0.45, alpha=0.65)
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_xlabel(r"$k$", loc="right")


def plot_stem(ax, indices, values, title):
    markerline, stemlines, _ = ax.stem(indices, values, basefmt=" ")
    plt.setp(markerline, color=ACCENT, markersize=4.5)
    plt.setp(stemlines, color=ACCENT, linewidth=1.35)
    style_axis(ax, xlim=(-2.7, 3.7), ylim=(-1.5, 2.7), xticks=np.arange(-2, 4))
    ax.set_title(title)


def save(fig, filename):
    fig.tight_layout(pad=0.8)
    fig.savefig(OUTPUT_DIR / filename, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def convolution_operations():
    fig, axes = plt.subplots(1, 3, figsize=(8.8, 2.45), sharey=True)
    plot_stem(axes[0], np.array([-1, 0, 1]), np.array([1, 2, -1]), r"$h[k]$")
    plot_stem(axes[1], np.array([-1, 0, 1]), np.array([-1, 2, 1]), r"$h[-k]$")
    plot_stem(axes[2], np.array([1, 2, 3]), np.array([-1, 2, 1]), r"$h[2-k]$")
    axes[1].annotate(
        "flip",
        xy=(0.02, 0.91),
        xytext=(-0.27, 0.91),
        xycoords="axes fraction",
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": SECONDARY},
        color=SECONDARY,
        ha="center",
    )
    axes[2].annotate(
        "shift",
        xy=(0.02, 0.91),
        xytext=(-0.27, 0.91),
        xycoords="axes fraction",
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": SECONDARY},
        color=SECONDARY,
        ha="center",
    )
    save(fig, "discrete-convolution-operations.pdf")


def rectangular_convolution():
    indices = np.arange(0, 9)
    values = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1])
    fig, ax = plt.subplots(figsize=(6.6, 2.65))
    markerline, stemlines, _ = ax.stem(indices, values, basefmt=" ")
    plt.setp(markerline, color=ACCENT, markersize=4.5)
    plt.setp(stemlines, color=ACCENT, linewidth=1.35)
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.grid(color=LIGHT_GRAY, linewidth=0.45, alpha=0.65)
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.set_xlim(-0.7, 8.7)
    ax.set_ylim(-0.4, 5.8)
    ax.set_xticks(indices)
    ax.set_yticks(np.arange(0, 6))
    ax.set_xlabel(r"$n$", loc="right")
    ax.set_title(r"$y[n]=x[n]\ast h[n]$")
    save(fig, "rectangular-sequence-convolution.pdf")


def continuous_impulse_approximation():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.55), sharey=True)
    for ax, delta in zip(axes, (1.0, 0.5)):
        ax.fill_between(
            [0, delta],
            [1 / delta, 1 / delta],
            color=ACCENT,
            alpha=0.23,
            step="post",
        )
        ax.plot([0, 0, delta, delta], [0, 1 / delta, 1 / delta, 0], color=ACCENT)
        ax.axhline(0, color=INK, linewidth=0.8)
        ax.axvline(0, color=INK, linewidth=0.8)
        ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
        ax.set_xlim(-0.25, 1.35)
        ax.set_ylim(-0.15, 2.35)
        ax.set_xticks([0, delta], [r"$0$", r"$\Delta$"])
        ax.set_yticks([0, 1 / delta], [r"$0$", r"$1/\Delta$"])
        ax.set_title(rf"$\Delta={delta:g}$, area $=1$")
        ax.set_xlabel(r"$t$", loc="right")
    save(fig, "continuous-impulse-approximation.pdf")


def sinc_impulse_sequence():
    t = np.linspace(-4.5, 4.5, 2401)
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.65), sharex=True)
    for ax, omega in zip(axes, (4, 12)):
        values = (omega / np.pi) * np.sinc(omega * t / np.pi)
        ax.plot(t, values, color=ACCENT, linewidth=1.15)
        ax.axhline(0, color=INK, linewidth=0.8)
        ax.axvline(0, color=INK, linewidth=0.8)
        ax.axvline(np.pi / omega, color=SECONDARY, linewidth=0.7, linestyle="--")
        ax.axvline(-np.pi / omega, color=SECONDARY, linewidth=0.7, linestyle="--")
        ax.grid(color=LIGHT_GRAY, linewidth=0.45, alpha=0.65)
        ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
        ax.set_xlim(-4.5, 4.5)
        ax.set_ylim(-1.2, 4.15)
        ax.set_xticks([-np.pi, 0, np.pi], [r"$-\pi$", r"$0$", r"$\pi$"])
        ax.set_title(rf"$\Omega={omega}$")
        ax.set_xlabel(r"$t$", loc="right")
    axes[0].set_ylabel(r"$\sin(\Omega t)/(\pi t)$")
    save(fig, "sinc-impulse-sequence.pdf")


def main():
    convolution_operations()
    rectangular_convolution()
    continuous_impulse_approximation()
    sinc_impulse_sequence()
    print(f"Generated 4 figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
