"""DTFT line spectra of periodic sequences; impulse weights are continuous-frequency weights."""

from generate import BLUE, RED, GRAY, OUT, save, style, stem

import matplotlib.pyplot as plt
import numpy as np


def line_weights(ax, positions, weights, title):
    style(ax, (-2.2, 2.2), (-0.8, 1.4))
    ax.axvspan(-1, 1, color="#eeeeee", zorder=-2)
    for position, weight in zip(positions, weights):
        if abs(weight) < 1e-12:
            ax.plot(position, 0, "o", color=GRAY, ms=3, zorder=3)
        else:
            ax.annotate(
                "", xy=(position, weight), xytext=(position, 0),
                arrowprops={"arrowstyle": "-|>", "color": RED, "lw": 1.5,
                            "shrinkA": 0, "shrinkB": 0},
            )
    ax.set(
        xlabel=r"$\omega/\pi$", ylabel="impulse weight / " + r"$\pi$",
        title=title, xticks=[-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2],
        yticks=[-0.5, 0, 0.5, 1],
    )


def four_point_spectrum():
    fig, ax = plt.subplots(1, 3, figsize=(10.0, 3.1), constrained_layout=True)
    n = np.arange(-4, 8)
    stem(ax[0], n, (n % 4 < 2).astype(float))
    ax[0].axvspan(-0.3, 3.7, color="#eeeeee", zorder=-2)
    ax[0].set(
        title=r"$x[n+4]=x[n]$", xlabel="$n$", ylabel="$x[n]$",
        xticks=[-4, -2, 0, 1, 2, 3, 4, 6], ylim=(-0.2, 1.4),
        yticks=[0, 1],
    )
    k = np.arange(-4, 5)
    coefficients = np.array([0.5, (1-1j)/4, 0, (1+1j)/4])
    weights_over_pi = 2 * coefficients[k % 4]
    line_weights(ax[1], k / 2, weights_over_pi.real, r"$\Re X(e^{j\omega})$")
    line_weights(ax[2], k / 2, weights_over_pi.imag, r"$\Im X(e^{j\omega})$")
    save(fig, OUT / "periodic-four-point-spectrum.pdf")


def periodic_impulse_train():
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 2.9), constrained_layout=True)
    n = np.arange(-8, 9)
    stem(ax[0], n, (n % 4 == 0).astype(float))
    ax[0].axvspan(-0.3, 3.7, color="#eeeeee", zorder=-2)
    ax[0].set(
        xlabel="$n$", ylabel="$p_4[n]$", title="Unit samples every 4 positions",
        xticks=[-8, -4, 0, 4, 8], yticks=[0, 1], ylim=(-0.15, 1.35),
    )
    style(ax[1], (-2.2, 2.2), (-0.2, 1.35 * np.pi / 2))
    ax[1].axvspan(-0.25, 1.75, color="#eeeeee", zorder=-2)
    for position in np.arange(-4, 5) / 2:
        ax[1].annotate(
            "", xy=(position, np.pi / 2), xytext=(position, 0),
            arrowprops={"arrowstyle": "-|>", "color": RED, "lw": 1.5,
                        "shrinkA": 0, "shrinkB": 0},
        )
    ax[1].set(
        title=r"Equal impulse weights $2\pi/N=\pi/2$",
        xlabel=r"$\omega/\pi$", ylabel="impulse weight",
        xticks=[-2, -1, -0.5, 0, 0.5, 1, 2],
        yticks=[0, np.pi / 2], yticklabels=["0", r"$\pi/2$"],
    )
    save(fig, OUT / "periodic-impulse-train.pdf")


if __name__ == "__main__":
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9,
        "mathtext.fontset": "stix", "axes.unicode_minus": False,
    })
    four_point_spectrum()
    periodic_impulse_train()
