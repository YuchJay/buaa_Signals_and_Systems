"""Generate figures for the Laplace-transform chapter examples."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "09-laplace-transform" / "examples"
BLUE, RED, GRAY = "#25669b", "#b23a2b", "#666666"


def save(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight",
                metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def style(ax, xlim, ylim, xlabel, ylabel):
    ax.axhline(0, color="#333333", lw=0.7, zorder=0)
    ax.grid(color="#dddddd", lw=0.45)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def impulse_response():
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    t = np.linspace(0, 3.2, 700)
    y = np.exp(-2 * t) - np.exp(-3 * t)
    ax.plot(t, y, color=BLUE, lw=1.5, label=r"$y(t)$")
    ax.plot(t, np.exp(-2 * t), color=GRAY, lw=1.0, ls="--",
            label=r"$\mathrm{e}^{-2t}$")
    ax.plot(t, -np.exp(-3 * t), color=RED, lw=1.0, ls=":",
            label=r"$-\mathrm{e}^{-3t}$")
    tmax = np.log(3 / 2)
    ax.plot([tmax], [np.exp(-2 * tmax) - np.exp(-3 * tmax)], "o",
            color=BLUE, ms=4)
    ax.annotate(r"$t=\ln\frac{3}{2}$", xy=(tmax, 0.148), xytext=(1.55, 0.34),
                color=BLUE, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    style(ax, (0, 3.2), (-1.08, 1.08), r"$t$", r"$y(t)$")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    save(fig, OUT / "first-order-answer.pdf")


def second_order_response():
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    t = np.linspace(0, 6.0, 900)
    y = 0.5 - np.exp(-t) + 0.5 * np.exp(-2 * t)
    ax.plot(t, y, color=BLUE, lw=1.5, label=r"$y(t)$")
    ax.axhline(0.5, color=GRAY, lw=0.9, ls="--")
    ax.text(4.7, 0.525, r"$\frac{1}{2}$", color=GRAY, fontsize=10)
    ax.plot([0], [0], "o", color=BLUE, ms=4)
    ax.annotate(r"$y'(0)=0$", xy=(0.06, 0.006), xytext=(1.15, 0.33),
                color=BLUE, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    style(ax, (0, 6.0), (-0.06, 0.62), r"$t$", r"$y(t)$")
    save(fig, OUT / "second-order-answer.pdf")


def repeated_pole_response():
    """Exponential input e^-t for y''+3y'+2y=x, with zero initial state."""
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    t = np.linspace(0, 7.0, 900)
    particular = t * np.exp(-t)
    homogeneous = -np.exp(-t) + np.exp(-2 * t)
    ax.plot(t, particular + homogeneous, color=BLUE, lw=1.8,
            label=r"$y(t)=t\mathrm{e}^{-t}-\mathrm{e}^{-t}+\mathrm{e}^{-2t}$")
    ax.plot(t, particular, color=GRAY, lw=1.1, ls="--",
            label=r"$y_{\mathrm{p}}(t)=t\mathrm{e}^{-t}$")
    ax.plot(t, homogeneous, color=RED, lw=1.1, ls=":",
            label=r"$y_{\mathrm{h}}(t)=-\mathrm{e}^{-t}+\mathrm{e}^{-2t}$")
    ax.plot([0], [0], "o", color=BLUE, ms=4)
    ax.annotate(r"$y(0^+)=y'(0^+)=0$", xy=(0.07, 0.002),
                xytext=(2.6, -0.17), color=BLUE, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    style(ax, (0, 7.0), (-0.30, 0.48), r"$t$", r"$y(t)$")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    save(fig, OUT.parent / "repeated-pole-response.pdf")


def impulse_input_rc():
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    t = np.linspace(0, 3.2, 700)
    ax.plot(t, np.exp(-2 * t) - np.exp(-3 * t), color=BLUE, lw=1.5,
            label=r"$b=1$")
    ax.plot(t, 4 * (np.exp(-2 * t) - np.exp(-3 * t)), color=RED, lw=1.5,
            ls="--", label=r"$b=4$")
    tmax = np.log(3 / 2)
    ax.plot([tmax, tmax], [0, np.exp(-2 * tmax) - np.exp(-3 * tmax)],
            color=GRAY, lw=0.8, ls=":")
    txt = r"$t=\ln\frac{3}{2}$"
    ax.text(1.62, 0.28, txt, color=GRAY, fontsize=9)
    style(ax, (0, 3.2), (-0.35, 3.05), r"$t$", r"$y(t)$")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    save(fig, OUT / "impulse-input-rc.pdf")


if __name__ == "__main__":
    impulse_response()
    second_order_response()
    repeated_pole_response()
    impulse_input_rc()
