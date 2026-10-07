"""Sliding-overlap diagrams for the continuous convolution worked examples."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "04-convolution" / "examples"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#202124"
ACCENT = "#A33A32"
BLUE = "#2E5EAA"
GREEN = "#3D7A57"
LIGHT = "#D8D8D8"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "mathtext.fontset": "stix",
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "savefig.transparent": True,
    }
)


def clean(ax, xlim, ylim, xticks=None):
    ax.axhline(0, color=INK, lw=0.75)
    ax.axvline(0, color=INK, lw=0.75)
    ax.grid(color=LIGHT, lw=0.4, alpha=0.7)
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if xticks is not None:
        ax.set_xticks(xticks)
    ax.set_xlabel(r"$\tau$", loc="right")


def step(ax, left, right, height, color, label=None, ls="-"):
    ax.hlines(height, left, right, color=color, lw=1.65, ls=ls, label=label)
    ax.vlines([left, right], 0, height, color=color, lw=1.0, ls=ls)


def save(fig, name):
    fig.tight_layout(pad=0.75)
    fig.savefig(OUT / name, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def ramp_sliding():
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 2.55), sharey=True)
    for ax, t, title in zip(axes, (0.5, 1.5), ("Entering: $t=0.5$", "Leaving: $t=1.5$")):
        clean(ax, (-0.65, 1.85), (-0.15, 1.55), sorted({0, 1, t - 1, t}))
        step(ax, 0, 1, 1, ACCENT, r"$x(\tau)$")
        left, right = t - 1, t
        u = np.linspace(left, right, 200)
        ax.plot(u, 1 - t + u, color=BLUE, lw=1.6, ls="--", label=r"$h(t-\tau)$")
        lo, hi = max(0, left), min(1, right)
        uu = np.linspace(lo, hi, 160)
        ax.fill_between(uu, 0, 1 - t + uu, color=GREEN, alpha=0.28)
        ax.axvline(left, color=BLUE, lw=0.55, ls=":")
        ax.axvline(right, color=BLUE, lw=0.55, ls=":")
        ax.set_title(title)
        ax.text(lo + 0.03, 0.12, rf"$\int_{{{lo:g}}}^{{{hi:g}}}$", color=GREEN)
        ax.legend(frameon=False, loc="upper left", fontsize=7)
    axes[0].set_ylabel(r"$x(\tau),\,h(t-\tau)$")
    save(fig, "ramp-sliding.pdf")


def rectangle_sliding():
    fig, axes = plt.subplots(2, 3, figsize=(8.2, 4.25), sharey=True)
    cases = [
        ((-1, 1), (-1, 1), (-1, 0, 1), "Equal widths"),
        ((-3, 3), (-1, 1), (-3, 0, 3), "Unequal widths"),
    ]
    for row, (fixed, moving, times, rowtitle) in enumerate(cases):
        for ax, t in zip(axes[row], times):
            clean(ax, (-4.4, 4.4), (-0.15, 1.35), [-3, -1, 0, 1, 3])
            a, b = fixed
            c, d = t + moving[0], t + moving[1]
            step(ax, a, b, 1, ACCENT, r"$x(\tau)$")
            step(ax, c, d, 1, BLUE, r"$h(t-\tau)$", ls="--")
            lo, hi = max(a, c), min(b, d)
            if lo < hi:
                ax.fill_between([lo, hi], 0, 1, color=GREEN, alpha=0.28)
                ax.text((lo + hi) / 2, 0.2, rf"$L={hi-lo:g}$", ha="center", color=GREEN)
            ax.set_title(rf"{rowtitle}, $t={t:g}$")
            ax.text(c, 1.08, rf"$t{moving[0]:+g}$", color=BLUE, fontsize=7, ha="center")
            ax.text(d, 1.08, rf"$t{moving[1]:+g}$", color=BLUE, fontsize=7, ha="center")
    axes[0, 0].legend(frameon=False, fontsize=7, loc="upper left")
    axes[1, 0].set_ylabel(r"$x(\tau),\,h(t-\tau)$")
    save(fig, "rectangle-sliding.pdf")


def signed_sliding():
    fig, axes = plt.subplots(2, 2, figsize=(7.8, 5.15), sharey=True)
    for ax, t in zip(axes.flat, (-1.5, -0.5, 0.5, 1.5)):
        clean(ax, (-2.8, 2.8), (-4.8, 2.9), sorted({-1, 0, 1, t-1, t, t+1}))
        step(ax, -1, 0, 1, ACCENT, r"$x(\tau)$")
        step(ax, 0, 1, -2, ACCENT)
        # h(t-tau): height 2 on [t-1,t], height 1 on [t,t+1]
        step(ax, t - 1, t, 2, BLUE, r"$h(t-\tau)$", ls="--")
        step(ax, t, t + 1, 1, BLUE, ls="--")
        # mark signed products on each overlap interval
        pieces = [(-1, 0, 1, 2), (-1, 0, 1, 1), (0, 1, -2, 2), (0, 1, -2, 1)]
        for lo0, hi0, xv, hv in pieces:
            lo, hi = max(lo0, t - 1 if hv == 2 else t), min(hi0, t if hv == 2 else t + 1)
            if lo < hi:
                product = xv * hv
                color = GREEN if product >= 0 else ACCENT
                ax.fill_between([lo, hi], 0, product, color=color, alpha=0.28)
                ax.hlines(product, lo, hi, color=color, lw=0.7)
                ax.text((lo+hi)/2, product + (0.16 if product > 0 else -0.18),
                        rf"${xv}\times{hv}={product}$",
                        ha="center", va="bottom" if product > 0 else "top",
                        color=color, fontsize=7)
        ax.axvline(t - 1, color=BLUE, lw=0.55, ls=":")
        ax.axvline(t, color=BLUE, lw=0.55, ls=":")
        ax.axvline(t + 1, color=BLUE, lw=0.55, ls=":")
        ax.set_title(rf"$t={t:g}$")
    axes[0, 0].legend(frameon=False, fontsize=7, loc="upper left")
    axes[1, 0].set_ylabel(r"$x(\tau),\,h(t-\tau)$")
    axes[1, 0].set_xlabel(r"$\tau$")
    axes[1, 1].set_xlabel(r"$\tau$")
    save(fig, "signed-sliding.pdf")


def lti_continuous_superposition():
    fig, axes = plt.subplots(3, 2, figsize=(7.5, 5.25))
    tt = np.linspace(-0.3, 4.3, 1801)
    p = lambda t: ((t >= 0) & (t < 2)).astype(float)
    q = lambda t: np.maximum(1 - np.abs(t - 1), 0)
    inputs = (p(tt), 2*p(tt)+p(tt-2), p(tt)+p(tt-1))
    outputs = (q(tt), 2*q(tt)+q(tt-2), q(tt)+q(tt-1))
    titles = (
        (r"$p(t)$", r"$q(t)$"),
        (r"$2p(t)+p(t-2)$", r"$2q(t)+q(t-2)$"),
        (r"$p(t)+p(t-1)$", r"$q(t)+q(t-1)$"),
    )
    for row in range(3):
        for col, values in enumerate((inputs[row], outputs[row])):
            ax = axes[row, col]
            clean(ax, (-0.3, 4.3), (-0.15, 2.4), [0, 1, 2, 3, 4])
            ax.set_xlabel(r"$t$", loc="right")
            ax.plot(tt, values, color=ACCENT if col == 0 else BLUE, lw=1.6)
            ax.set_title(titles[row][col])
    save(fig, "continuous-lti-superposition.pdf")


if __name__ == "__main__":
    ramp_sliding()
    rectangle_sliding()
    signed_sliding()
    lti_continuous_superposition()
