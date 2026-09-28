"""Generate the modulation and synchronous-demodulation spectrum figure."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parents[3] / "figures" / "06-ctft"
OUT.mkdir(parents=True, exist_ok=True)


def baseband(omega: np.ndarray, center: float = 0.0, width: float = 2.0) -> np.ndarray:
    value = np.maximum(1.0 - np.abs(omega - center) / width, 0.0)
    return value


def main() -> None:
    wc, wm = 6.0, 2.0
    omega = np.linspace(-15.0, 15.0, 5000)
    y = 0.5 * baseband(omega, wc, wm) + 0.5 * baseband(omega, -wc, wm)
    w = (
        0.5 * baseband(omega, 0.0, wm)
        + 0.25 * baseband(omega, 2 * wc, wm)
        + 0.25 * baseband(omega, -2 * wc, wm)
    )

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "mathtext.fontset": "stix",
            "axes.unicode_minus": False,
        }
    )
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 4.8), sharex=True, constrained_layout=True)
    for ax, spectrum, title in zip(
        axes,
        (y, w),
        ("After cosine modulation", "After synchronous demodulation"),
    ):
        ax.plot(omega, spectrum, color="#b23a2b", lw=1.6)
        ax.axhline(0, color="black", lw=0.7)
        ax.axvline(0, color="black", lw=0.7)
        ax.grid(True, color="#dddddd", lw=0.6)
        ax.set_ylim(-0.03, 0.62)
        ax.set_title(title, loc="left", fontsize=10)
        for mark in (-2, 0, 2, -6, 6, -12, 12):
            ax.axvline(mark, color="#777777", lw=0.45, ls=":")
    axes[0].set_ylabel(r"$Y(\mathrm{j}\omega)$")
    axes[1].set_ylabel(r"$W(\mathrm{j}\omega)$")
    axes[1].axvspan(-3, 3, color="#87b4d8", alpha=0.15)
    axes[1].text(0, 0.57, r"LPF: gain $2$, $|\omega|<3$", ha="center", fontsize=8)
    axes[-1].set_xlabel(r"$\omega$")
    axes[-1].set_xticks([-12, -6, -2, 0, 2, 6, 12])
    fig.savefig(OUT / "modulation-demodulation.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated {OUT / 'modulation-demodulation.pdf'}")

    omega = np.linspace(-14.0, 14.0, 5000)
    fdm = (
        0.5 * baseband(omega, 4.0, 1.0)
        + 0.5 * baseband(omega, -4.0, 1.0)
        + 0.5 * baseband(omega, 8.0, 1.0)
        + 0.5 * baseband(omega, -8.0, 1.0)
    )
    demod_first = (
        0.5 * baseband(omega, 0.0, 1.0)
        + 0.25 * baseband(omega, 8.0, 1.0)
        + 0.25 * baseband(omega, -8.0, 1.0)
        + 0.25 * baseband(omega, 4.0, 1.0)
        + 0.25 * baseband(omega, -4.0, 1.0)
        + 0.25 * baseband(omega, 12.0, 1.0)
        + 0.25 * baseband(omega, -12.0, 1.0)
    )
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 4.8), sharex=True, constrained_layout=True)
    for ax, spectrum, title in zip(
        axes,
        (fdm, demod_first),
        ("Two-channel frequency-division multiplexing", "After multiplying by the first carrier"),
    ):
        ax.plot(omega, spectrum, color="#2369bd", lw=1.5)
        ax.axhline(0, color="black", lw=0.7)
        ax.axvline(0, color="black", lw=0.7)
        ax.grid(True, color="#dddddd", lw=0.6)
        ax.set_ylim(-0.03, 0.62)
        ax.set_title(title, loc="left", fontsize=10)
    axes[0].set_ylabel(r"$Y(\mathrm{j}\omega)$")
    axes[1].set_ylabel(r"$W_1(\mathrm{j}\omega)$")
    axes[1].axvspan(-2, 2, color="#87b4d8", alpha=0.15)
    axes[1].text(0, 0.57, r"LPF: gain $2$, $|\omega|<2\omega_m$", ha="center", fontsize=8)
    axes[-1].set_xlabel(r"$\omega/\omega_m$")
    axes[-1].set_xticks([-12, -8, -4, 0, 4, 8, 12])
    fig.savefig(OUT / "fdm-spectra.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated {OUT / 'fdm-spectra.pdf'}")


if __name__ == "__main__":
    main()
