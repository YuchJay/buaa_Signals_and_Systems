"""Draw the four-period DTFS example and its periodic complex coefficients."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "07-dtft" / "dtfs-four-point.pdf"
BLUE, RED = "#25669b", "#b23a2b"


def panel(ax, index, values, title, ylabel, color):
    ax.axvspan(-0.35, 3.35, color="#eeeeee", zorder=-2)
    ax.axhline(0, color="#333333", lw=0.7, zorder=0)
    markers, lines, _ = ax.stem(index, values, basefmt=" ")
    plt.setp(markers, color=color, markersize=4)
    plt.setp(lines, color=color, linewidth=1.2)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color="#dddddd", lw=0.45)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel(ylabel)
    ax.set_xlim(-4.6, 7.6)
    ax.set_xticks([-4, -2, 0, 2, 4, 6])


def main():
    index = np.arange(-4, 8)
    samples = np.array([1, 1, 0, 0])
    coefficients = np.array([0.5, (1-1j)/4, 0, (1+1j)/4])
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 2.8),
                             constrained_layout=True)
    panel(axes[0], index, samples[index % 4],
          r"$x[n+4]=x[n]$", r"$x[n]$", BLUE)
    panel(axes[1], index, coefficients[index % 4].real,
          r"$\Re\,a_{k+4}=\Re\,a_k$", r"$\Re\,a_k$", BLUE)
    panel(axes[2], index, coefficients[index % 4].imag,
          r"$\Im\,a_{k+4}=\Im\,a_k$", r"$\Im\,a_k$", RED)
    axes[0].set(xlabel=r"$n$", ylim=(-0.12, 1.25), yticks=[0, 1])
    axes[1].set(xlabel=r"$k$", ylim=(-0.07, 0.62),
                yticks=[0, 0.25, 0.5],
                yticklabels=["0", r"$1/4$", r"$1/2$"])
    axes[2].set(xlabel=r"$k$", ylim=(-0.34, 0.34),
                yticks=[-0.25, 0, 0.25],
                yticklabels=[r"$-1/4$", "0", r"$1/4$"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight",
                metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)
    print(OUT)


if __name__ == "__main__":
    main()
