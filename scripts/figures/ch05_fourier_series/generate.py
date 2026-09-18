"""Generate a reproducible Fourier-series approximation figure."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parents[3] / "figures" / "05-fourier-series"
OUT.mkdir(parents=True, exist_ok=True)


def rectangular_wave(t: np.ndarray, T: float, T1: float) -> np.ndarray:
    phase = ((t + T / 2) % T) - T / 2
    return (np.abs(phase) < T1).astype(float)


def partial_sum(t: np.ndarray, T: float, T1: float, n_terms: int) -> np.ndarray:
    omega0 = 2 * np.pi / T
    y = np.full_like(t, 2 * T1 / T, dtype=float)
    for n in range(1, n_terms + 1):
        bn = 2 * np.sin(n * omega0 * T1) / (n * np.pi)
        y += bn * np.cos(n * omega0 * t)
    return y


def main() -> None:
    T, T1 = 2.0, 0.6
    t = np.linspace(-2.0, 2.0, 4000)
    signal = rectangular_wave(t, T, T1)

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "stix",
        "axes.unicode_minus": False,
    })
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 4.8), sharex=True, constrained_layout=True)
    for ax, n_terms in zip(axes, (5, 25)):
        ax.plot(t, signal, color="#555555", lw=1.2, ls="--", label="original")
        ax.plot(t, partial_sum(t, T, T1, n_terms), color="#b23a2b", lw=1.4, label=f"N={n_terms}")
        ax.set_ylim(-0.35, 1.35)
        ax.set_ylabel("x(t)")
        ax.grid(True, color="#dddddd", lw=0.6)
        ax.axhline(0, color="black", lw=0.7)
        ax.legend(loc="upper right", frameon=False, ncol=2)
    axes[0].set_title("Fourier-series approximation of a periodic rectangular wave")
    axes[-1].set_xlabel("t")
    axes[-1].set_xticks([-2, -1, -0.6, 0, 0.6, 1, 2])
    fig.savefig(OUT / "rectangular-fourier-series.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated {OUT / 'rectangular-fourier-series.pdf'}")


if __name__ == "__main__":
    main()
