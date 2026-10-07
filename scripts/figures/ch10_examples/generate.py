"""Generate figures for the Z-transform chapter examples."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "10-z-transform" / "examples"
BLUE, RED, GRAY = "#25669b", "#b23a2b", "#666666"


def save(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight",
                metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def stem(ax, n, y, color=BLUE):
    markerline, stemlines, _ = ax.stem(n, y, linefmt=color, markerfmt="o",
                                       basefmt=" ")
    plt.setp(stemlines, linewidth=1.2)
    plt.setp(markerline, markersize=3.5)


def style(ax, xlim, ylim, xlabel, ylabel):
    ax.axhline(0, color="#333333", lw=0.7, zorder=0)
    ax.axvline(0, color="#333333", lw=0.7, zorder=0)
    ax.grid(color="#dddddd", lw=0.45)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def recursive_impulse_response():
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    n = np.arange(0, 7)
    h = 0.5 ** n
    stem(ax, n, h)
    labels = {0: "1", 1: "0.5", 2: "0.25", 3: "0.125"}
    for k, txt in labels.items():
        ax.text(k, h[k] + 0.04, txt, ha="center", fontsize=8, color=BLUE)
    style(ax, (-0.8, 6.7), (-0.06, 1.14), r"$n$", r"$h[n]$")
    save(fig, OUT / "recursive-answer.pdf")


def first_order_difference():
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    n = np.arange(0, 5)
    ax.vlines(n, 0, 1, color=BLUE, lw=1.2)
    ax.plot(n, np.ones_like(n, dtype=float), "o", color=BLUE, ms=3.5)
    ax.vlines(-1, 0, -2, color=RED, lw=1.2)
    ax.plot([-1], [-2], "o", color=RED, ms=3.5)
    ax.annotate(r"$-2\delta[n+1]$", xy=(-1, -1.9), xytext=(-0.45, -2.6),
                color=RED, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    ax.annotate(r"$x[n]=1,\ n=0,\ldots,4$", xy=(2.0, 1.0), xytext=(1.3, 1.42),
                color=BLUE, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    style(ax, (-2.2, 5.0), (-3.1, 1.85), r"$n$", r"$x[n]$")
    save(fig, OUT / "first-order-difference-given.pdf")


def first_order_difference_answer():
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    n = np.arange(0, 6)
    y = (n + 2) / 2 ** (n + 1)
    stem(ax, n, y)
    labels = {0: "1", 1: "0.75", 2: "0.5", 3: "0.3125"}
    for k, txt in labels.items():
        ax.text(k, y[k] + 0.04, txt, ha="center", fontsize=8, color=BLUE)
    style(ax, (-0.8, 5.7), (-0.07, 1.35), r"$n$", r"$y[n]$")
    save(fig, OUT / "first-order-difference-answer.pdf")


if __name__ == "__main__":
    recursive_impulse_response()
    first_order_difference()
    first_order_difference_answer()
