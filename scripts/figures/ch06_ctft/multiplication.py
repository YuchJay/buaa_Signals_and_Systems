"""Plot the sinc-square example of the CTFT multiplication property."""

from basic_pairs import BLUE, RED, OUT, axes_grid, save

import matplotlib.pyplot as plt
import numpy as np


def sinc_square():
    fig, ax = axes_grid(1, 3, (9.2, 2.8))
    t = np.linspace(-6, 6, 2401)
    ax[0].plot(t, 4 * np.sinc(2 * t / np.pi) ** 2, color=BLUE)
    ax[0].plot(0, 4, "o", color=RED, ms=4)
    ax[0].set(
        title=r"$y(t)=[\sin(2t)/t]^2$",
        xlabel=r"$t$", ylabel=r"$y(t)$",
        xticks=[-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
        xticklabels=[r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"],
        yticks=[0, 2, 4], ylim=(-0.25, 4.6),
    )
    ax[1].plot(
        [-5, -2, -2, 2, 2, 5],
        [0, 0, np.pi, np.pi, 0, 0],
        color=BLUE,
    )
    ax[1].set(
        title=r"$X_1=X_2$", xlabel=r"$\omega$",
        ylabel=r"$X_k(\mathrm{j}\omega)$",
        xticks=[-4, -2, 0, 2, 4],
        yticks=[0, np.pi], yticklabels=["0", r"$\pi$"],
        ylim=(-0.25, 1.25 * np.pi),
    )
    ax[2].plot(
        [-5, -4, 0, 4, 5], [0, 0, 2 * np.pi, 0, 0], color=BLUE,
    )
    ax[2].plot(0, 2 * np.pi, "o", color=RED, ms=4)
    ax[2].set(
        title=r"$Y=(X_1\ast X_2)/(2\pi)$",
        xlabel=r"$\omega$", ylabel=r"$Y(\mathrm{j}\omega)$",
        xticks=[-4, -2, 0, 2, 4],
        yticks=[0, np.pi, 2 * np.pi],
        yticklabels=["0", r"$\pi$", r"$2\pi$"],
        ylim=(-0.4, 2.5 * np.pi),
    )
    save(fig, "sinc-square-frequency-convolution")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "mathtext.fontset": "stix",
        "axes.unicode_minus": False,
        "axes.titlesize": 10,
    })
    sinc_square()
