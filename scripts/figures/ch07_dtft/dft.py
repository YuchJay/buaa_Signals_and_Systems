"""Figures for the finite point DFT section."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from generate import save, style, stem

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "07-dtft"
BLUE, RED, GRAY = "#25669b", "#b23a2b", "#666666"


def dft_sampling():
    n = np.arange(0, 8)
    x = np.array([1.0, 0.7, -0.3, 0.5, 0.2, 0.0, 0.15, -0.2])
    w = np.linspace(-np.pi, np.pi, 2401)
    X = np.sum(x[:, None] * np.exp(-1j * n[:, None] * w[None, :]), axis=0)
    wk = 2 * np.pi * np.arange(8) / 8
    Xk = np.sum(x[:, None] * np.exp(-1j * n[:, None] * wk[None, :]), axis=0)
    fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.5), constrained_layout=True)
    stem(ax[0], n, x)
    ax[0].set(xlabel="$n$", ylabel="$x[n]$", title="Finite sequence, $N=8$", ylim=(-.5, 1.2))
    ax[0].set_xticks(np.arange(0, 8))
    ax[1].plot(w / np.pi, np.real(X), color=BLUE, lw=1.5, label=r"$\Re X(e^{j\omega})$")
    ax[1].plot(w / np.pi, np.imag(X), color=GRAY, lw=1.0, label=r"$\Im X(e^{j\omega})$")
    wn = (((wk + np.pi) % (2*np.pi)) - np.pi) / np.pi
    ax[1].scatter(wn, np.real(Xk), color=RED, s=24, zorder=4,
                   label=r"$\Re X[k]$")
    ax[1].scatter(wn, np.imag(Xk), color="#25835b", marker="x", s=24,
                   zorder=4, label=r"$\Im X[k]$")
    style(ax[1], (-1, 1), (-2.6, 3.4))
    ax[1].set(xlabel=r"$\omega/\pi$", ylabel="value", title="DTFT curve and DFT samples")
    ax[1].set_xticks([-1, -.75, -.5, -.25, 0, .25, .5, .75, 1])
    ax[1].legend(fontsize=8, loc="upper right")
    ax[1].text(0.02, 0.04, r"red points: $\omega_k=2\pi k/N$", transform=ax[1].transAxes, fontsize=8, color=RED)
    save(fig, OUT / "dft-sampling.pdf")


def dft_matrix_flow():
    fig, ax = plt.subplots(figsize=(9.2, 2.8), constrained_layout=True)
    ax.axis("off")
    boxes = [(0.04, 0.25, 0.22, 0.5, "x\n[x[0], ..., x[N-1]]^T"),
             (0.39, 0.16, 0.22, 0.68, "W\nW[k,n] = exp(-j 2 pi kn/N)"),
             (0.74, 0.25, 0.22, 0.5, "X\n[X[0], ..., X[N-1]]^T")]
    for x0, y0, w, h, text in boxes:
        rect = plt.Rectangle((x0, y0), w, h, facecolor="#eef3f7", edgecolor=BLUE, lw=1.3)
        ax.add_patch(rect)
        ax.text(x0+w/2, y0+h/2, text, ha="center", va="center", fontsize=12, usetex=False)
    ax.annotate("", xy=(0.38, .5), xytext=(.27, .5), arrowprops={"arrowstyle": "->", "lw": 1.5, "color": GRAY})
    ax.annotate("", xy=(0.73, .5), xytext=(.62, .5), arrowprops={"arrowstyle": "->", "lw": 1.5, "color": GRAY})
    ax.text(.325, .57, "X = W x", ha="center", fontsize=10)
    ax.text(.675, .57, "x = (1/N) W^H X", ha="center", fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    save(fig, OUT / "dft-matrix-flow.pdf")


def fft_flow():
    """Explain one radix-2 butterfly and the 8-point DIT flow graph."""
    fig, ax = plt.subplots(1, 2, figsize=(12.2, 5.2),
                           gridspec_kw={"width_ratios": [1, 2.4]},
                           constrained_layout=True)

    # One butterfly.
    a = ax[0]
    a.axis("off")
    a.set_xlim(0, 1)
    a.set_ylim(0, 1)
    a.text(.08, .76, "A", fontsize=12, ha="center")
    a.text(.08, .24, "B", fontsize=12, ha="center")
    a.text(.51, .50, "W", fontsize=12, ha="center", color=RED)
    a.text(.92, .76, "A + WB", fontsize=11, ha="center")
    a.text(.92, .24, "A - WB", fontsize=11, ha="center")
    a.annotate("", xy=(.82, .76), xytext=(.15, .76),
               arrowprops={"arrowstyle": "->", "color": BLUE, "lw": 1.3})
    a.annotate("", xy=(.82, .24), xytext=(.15, .24),
               arrowprops={"arrowstyle": "->", "color": BLUE, "lw": 1.3})
    a.annotate("", xy=(.46, .76), xytext=(.15, .24),
               arrowprops={"arrowstyle": "->", "color": RED, "lw": 1.1})
    a.annotate("", xy=(.46, .24), xytext=(.15, .24),
               arrowprops={"arrowstyle": "->", "color": RED, "lw": 1.1})
    a.plot([.46, .56], [.76, .50], color=RED, lw=1.1)
    a.plot([.46, .56], [.24, .50], color=RED, lw=1.1)
    a.text(.50, .07, "one multiply + two add/subtract operations", fontsize=9,
           ha="center", color=GRAY)
    a.set_title("One radix-2 butterfly", fontsize=12)

    # Eight-point decimation-in-time graph.
    a = ax[1]
    a.set_xlim(-.15, 3.35)
    a.set_ylim(-.7, 7.7)
    a.axis("off")
    xcols = [0.0, 1.0, 2.0, 3.0]
    labels = [
        [r"$x[0]$", r"$x[4]$", r"$x[2]$", r"$x[6]$",
         r"$x[1]$", r"$x[5]$", r"$x[3]$", r"$x[7]$"],
        None, None,
        [r"$X[0]$", r"$X[1]$", r"$X[2]$", r"$X[3]$",
         r"$X[4]$", r"$X[5]$", r"$X[6]$", r"$X[7]$"],
    ]
    y = np.arange(7, -1, -1)
    for col, lab in zip(xcols, labels):
        if lab is None:
            continue
        for yi, text in zip(y, lab):
            a.text(col, yi, text, ha="center", va="center", fontsize=9)
    for col, title in zip(xcols, ["Input (bit-reversed)", "2-point DFT", "4-point DFT",
                                  "8-point DFT output"]):
        a.text(col, 7.55, title, ha="center", va="bottom", fontsize=9,
               color=GRAY)

    def edge(x1, r1, x2, r2, color=BLUE, lw=0.9):
        a.plot([x1, x2], [y[r1], y[r2]], color=color, lw=lw)

    # Stage 1: adjacent pairs.
    for base in range(0, 8, 2):
        edge(0.08, base, .92, base)
        edge(0.08, base + 1, .92, base)
        edge(0.08, base, .92, base + 1)
        edge(0.08, base + 1, .92, base + 1)
    # Stage 2: distance-two pairs.
    for base in range(0, 8, 4):
        for r in range(2):
            edge(1.08, base + r, 1.92, base + r)
            edge(1.08, base + r + 2, 1.92, base + r)
            edge(1.08, base + r, 1.92, base + r + 2)
            edge(1.08, base + r + 2, 1.92, base + r + 2)
            if r == 1:
                a.text(1.53, y[base + r + 2] + .18, r"$W_4^1$",
                       fontsize=8, color=RED, ha="center")
    # Stage 3: distance-four pairs.
    for r in range(4):
        edge(2.08, r, 2.92, r)
        edge(2.08, r + 4, 2.92, r)
        edge(2.08, r, 2.92, r + 4)
        edge(2.08, r + 4, 2.92, r + 4)
        if r:
            a.text(2.52, y[r + 4] + .18, rf"$W_8^{r}$",
                   fontsize=8, color=RED, ha="center")
    a.text(1.5, -.48,
           "Each stage merges smaller DFTs; red labels are nontrivial twiddle factors",
           fontsize=9, ha="center", color=GRAY)
    a.text(-.12, 3.5, "3-bit reversal:\n"
           "000,001,010,011,... -> 000,100,010,110,...",
           fontsize=8, ha="right", va="center", color=GRAY)
    a.set_title("8-point radix-2 FFT", fontsize=12)
    save(fig, OUT / "fft-flow.pdf")


def fft_convolution_flow():
    fig, ax = plt.subplots(figsize=(10.5, 2.8), constrained_layout=True)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    boxes = [
        (.03, .58, .17, .25, "x[n]\nzero-pad to N"),
        (.31, .58, .17, .25, "N-point FFT\nX[k]"),
        (.60, .58, .17, .25, "Pointwise product\nX[k]H[k]"),
        (.83, .58, .14, .25, "IFFT\ny[n]"),
        (.03, .13, .17, .25, "h[n]\nzero-pad to N"),
        (.31, .13, .17, .25, "N-point FFT\nH[k]"),
    ]
    for x0, y0, w, h, text in boxes:
        ax.add_patch(plt.Rectangle((x0, y0), w, h,
                                   facecolor="#eef3f7", edgecolor=BLUE,
                                   lw=1.2))
        ax.text(x0 + w / 2, y0 + h / 2, text, ha="center", va="center",
                fontsize=10)
    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops={"arrowstyle": "->", "color": GRAY, "lw": 1.3})
    arrow(.20, .705, .30, .705)
    arrow(.48, .705, .59, .705)
    arrow(.77, .705, .82, .705)
    arrow(.20, .255, .30, .255)
    arrow(.48, .255, .58, .52)
    ax.text(.50, .91, "Zero-pad first to prevent wrap-around", ha="center",
            fontsize=10, color=RED)
    save(fig, OUT / "fft-convolution-flow.pdf")


if __name__ == "__main__":
    dft_sampling()
    dft_matrix_flow()
    fft_flow()
    fft_convolution_flow()
