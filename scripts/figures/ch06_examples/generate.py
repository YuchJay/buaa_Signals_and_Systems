"""Generate figures for the Chapter 6 worked examples."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parents[3] / "figures" / "06-ctft" / "examples"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#b23a2b"
GUIDE = "#555555"


def configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "mathtext.fontset": "stix",
            "axes.unicode_minus": False,
        }
    )


def draw_spectral_data() -> None:
    fig, axes = plt.subplots(2, 1, figsize=(6.8, 4.5), constrained_layout=True)

    omega = np.array([-4.0, -2.0, -2.0, 2.0, 2.0, 4.0])
    magnitude = np.array([0.0, 0.0, 1.0, 1.0, 0.0, 0.0])
    axes[0].plot(omega, magnitude, color=ACCENT, lw=1.6)
    axes[0].set_ylabel(r"$|X(\mathrm{j}\omega)|$")
    axes[0].set_ylim(-0.12, 1.25)
    axes[0].set_yticks([0, 1])

    omega_band = np.linspace(-2.0, 2.0, 400)
    axes[1].plot(omega_band, -omega_band, color=ACCENT, lw=1.6)
    axes[1].plot([-4, -2, 2, 4], [np.nan] * 4, alpha=0)
    axes[1].set_ylabel(r"$\angle X(\mathrm{j}\omega)$")
    axes[1].set_yticks([-2, 0, 2])
    axes[1].set_xlabel(r"$\omega$")

    for ax in axes:
        ax.axhline(0, color="black", lw=0.7)
        ax.axvline(0, color="black", lw=0.7)
        ax.set_xlim(-4, 4)
        ax.set_xticks([-4, -2, 0, 2, 4])
        ax.grid(True, color="#dddddd", lw=0.6)
    axes[1].text(
        0.69,
        0.87,
        r"undefined for $|\omega|\geq 2$",
        transform=axes[1].transAxes,
        color=GUIDE,
        fontsize=8,
    )

    fig.savefig(OUT / "phase-recovery-given.pdf", bbox_inches="tight")
    plt.close(fig)


def draw_recovered_signal() -> None:
    t = np.linspace(-5.0, 7.0, 3000)
    shifted = t - 1.0
    x = 2.0 / np.pi * np.sinc(2.0 * shifted / np.pi)

    fig, ax = plt.subplots(figsize=(6.8, 3.2), constrained_layout=True)
    ax.plot(t, x, color=ACCENT, lw=1.6)
    ax.scatter([1.0], [2.0 / np.pi], color=ACCENT, s=20, zorder=3)
    ax.axhline(0, color="black", lw=0.7)
    ax.axvline(0, color="black", lw=0.7)
    ax.axvline(1, color=GUIDE, lw=0.8, ls="--")
    ax.text(1.12, 2.0 / np.pi, r"$x(1)=2/\pi$", va="center")
    ax.set_xlim(-5, 7)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$x(t)$")
    ax.grid(True, color="#dddddd", lw=0.6)
    fig.savefig(OUT / "phase-recovery-answer.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    configure()
    draw_spectral_data()
    draw_recovered_signal()
    for name in ("phase-recovery-given.pdf", "phase-recovery-answer.pdf"):
        print(f"Generated {OUT / name}")


if __name__ == "__main__":
    main()
