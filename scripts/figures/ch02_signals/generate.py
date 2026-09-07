"""Generate the reproducible figures used by Chapter 2."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "figures" / "02-signals"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INK = "#202124"
GRAY = "#777777"
LIGHT_GRAY = "#D8D8D8"
ACCENT = "#A33A32"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "axes.titleweight": "regular",
        "mathtext.fontset": "stix",
        "xtick.color": INK,
        "ytick.color": INK,
        "lines.linewidth": 1.6,
        "savefig.transparent": True,
    }
)


def finish_axis(ax, *, xlabel="", ylabel=""):
    """Apply the shared restrained axis style."""
    ax.axhline(0, color=INK, linewidth=0.75)
    ax.axvline(0, color=INK, linewidth=0.75)
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.grid(axis="both", color=LIGHT_GRAY, linewidth=0.45, alpha=0.65)
    ax.set_xlabel(xlabel, loc="right")
    ax.set_ylabel(ylabel, rotation=0, loc="top")
    ax.margins(x=0.03)


def save(fig, filename):
    fig.tight_layout(pad=0.8)
    fig.savefig(OUTPUT_DIR / filename, bbox_inches="tight")
    plt.close(fig)


def base_signal(t):
    """An asymmetric piecewise-linear signal with compact support."""
    knots = np.array([-2.0, -1.0, 0.0, 0.8, 2.0])
    values = np.array([0.0, 1.0, 0.35, 1.45, 0.0])
    return np.interp(t, knots, values, left=0.0, right=0.0)


def plot_time_transformations():
    t = np.linspace(-4.2, 4.2, 1800)
    panels = (
        (base_signal(t), r"Original $x(t)$"),
        (base_signal(t - 1.5), r"Shift $x(t-1.5)$"),
        (base_signal(2 * t), r"Compression $x(2t)$"),
        (base_signal(-t), r"Reversal $x(-t)$"),
    )
    fig, axes = plt.subplots(2, 2, figsize=(6.5, 4.2), sharex=True, sharey=True)
    for ax, (values, title) in zip(axes.flat, panels):
        ax.plot(t, values, color=ACCENT)
        ax.set_title(title)
        ax.set_xlim(-4.2, 4.2)
        ax.set_ylim(-0.2, 1.75)
        ax.set_xticks(np.arange(-4, 5, 2))
        ax.set_yticks([0, 0.5, 1.0, 1.5])
        finish_axis(ax, xlabel=r"$t$", ylabel=r"$x$")
    save(fig, "time-transformations.pdf")


def plot_even_odd_decomposition():
    t = np.linspace(-2.2, 2.2, 800)
    original = 2 + t + t**2
    even = 2 + t**2
    odd = t
    panels = (
        (original, r"$x(t)=2+t+t^2$"),
        (even, r"Even part $x_{\mathrm{e}}(t)$"),
        (odd, r"Odd part $x_{\mathrm{o}}(t)$"),
    )
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.45))
    for ax, (values, title) in zip(axes, panels):
        ax.plot(t, values, color=ACCENT)
        ax.set_title(title)
        ax.set_xlim(-2.2, 2.2)
        ax.set_xticks([-2, -1, 0, 1, 2])
        finish_axis(ax, xlabel=r"$t$", ylabel=r"$x$")
    save(fig, "even-odd-decomposition.pdf")


def plot_continuous_step_impulse():
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.55))

    ax = axes[0]
    ax.plot([-3, 0], [0, 0], color=ACCENT)
    ax.plot([0, 3], [1, 1], color=ACCENT)
    ax.scatter([0], [0.5], s=24, color=ACCENT, zorder=3)
    ax.plot([0, 0], [0, 1], color=ACCENT, linewidth=0.8, linestyle=":")
    ax.set_title(r"Unit step $u(t)$")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.2, 1.35)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([0, 0.5, 1])
    finish_axis(ax, xlabel=r"$t$", ylabel=r"$u$")

    ax = axes[1]
    ax.annotate(
        "",
        xy=(0, 1.1),
        xytext=(0, 0),
        arrowprops={"arrowstyle": "-|>", "color": ACCENT, "linewidth": 1.8},
    )
    ax.text(0.14, 0.93, "unit area", color=ACCENT)
    ax.set_title(r"Unit impulse $\delta(t)$")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.2, 1.35)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([])
    finish_axis(ax, xlabel=r"$t$", ylabel=r"$\delta$")
    save(fig, "continuous-step-impulse.pdf")


def plot_discrete_step_impulse():
    n = np.arange(-5, 9)
    unit_step = (n >= 0).astype(float)
    unit_impulse = (n == 0).astype(float)
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.55), sharey=True)
    panels = (
        (unit_step, r"Unit step $u[n]$"),
        (unit_impulse, r"Unit impulse $\delta[n]$"),
    )
    for ax, (values, title) in zip(axes, panels):
        markerline, stemlines, _ = ax.stem(n, values, basefmt=" ")
        plt.setp(markerline, color=ACCENT, markersize=4.5)
        plt.setp(stemlines, color=ACCENT, linewidth=1.2)
        ax.set_title(title)
        ax.set_xlim(-5.5, 8.5)
        ax.set_ylim(-0.2, 1.35)
        ax.set_xticks(np.arange(-4, 9, 2))
        ax.set_yticks([0, 0.5, 1])
        finish_axis(ax, xlabel=r"$n$", ylabel=r"$x$")
    save(fig, "discrete-step-impulse.pdf")


def plot_sampling_functions():
    x_sa = np.linspace(-4 * np.pi, 4 * np.pi, 2000)
    sa = np.sinc(x_sa / np.pi)
    x_sinc = np.linspace(-4, 4, 2000)
    sinc = np.sinc(x_sinc)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7))

    ax = axes[0]
    ax.plot(x_sa, sa, color=ACCENT)
    zeros = np.arange(-4, 5) * np.pi
    ax.scatter(zeros[zeros != 0], np.zeros(8), s=12, color=INK, zorder=3)
    ax.set_title(r"$\mathrm{Sa}(t)=\sin(t)/t$")
    ax.set_xlim(-4 * np.pi, 4 * np.pi)
    ax.set_xticks(np.arange(-4, 5, 2) * np.pi)
    ax.set_xticklabels([r"$-4\pi$", r"$-2\pi$", "$0$", r"$2\pi$", r"$4\pi$"])
    ax.set_ylim(-0.35, 1.15)
    finish_axis(ax, xlabel=r"$t$", ylabel=r"$\mathrm{Sa}$")

    ax = axes[1]
    ax.plot(x_sinc, sinc, color=ACCENT)
    zeros = np.arange(-4, 5)
    ax.scatter(zeros[zeros != 0], np.zeros(8), s=12, color=INK, zorder=3)
    ax.set_title(r"$\mathrm{sinc}(t)=\sin(\pi t)/(\pi t)$")
    ax.set_xlim(-4, 4)
    ax.set_xticks(np.arange(-4, 5, 2))
    ax.set_ylim(-0.35, 1.15)
    finish_axis(ax, xlabel=r"$t$", ylabel=r"$\mathrm{sinc}$")
    save(fig, "sampling-functions.pdf")


def main():
    plot_time_transformations()
    plot_even_odd_decomposition()
    plot_continuous_step_impulse()
    plot_discrete_step_impulse()
    plot_sampling_functions()
    print(f"Generated 5 figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
