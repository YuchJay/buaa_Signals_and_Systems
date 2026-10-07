"""DTFT multiplication, periodic convolution, energy, and symmetry figures."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from generate import save, stem, frequency_axis, sinc_samples

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "07-dtft"
EX = OUT / "examples"
BLUE, RED, GRAY = "#25669b", "#b23a2b", "#666666"


def freq(ax, title, ylabel="$X$", limits=(-1, 1)):
    frequency_axis(ax, limits)
    ax.set(title=title, ylabel=ylabel)


def sample(ax, n, y, title, ylabel="$x[n]$"):
    stem(ax, n, y)
    ax.set(title=title, xlabel="$n$", ylabel=ylabel)


def triangle(w, a):
    return np.maximum(2*a-np.abs(w), 0)


def period_sum(w, a):
    return sum(triangle(w-2*k*np.pi, a) for k in range(-3, 4))/(2*np.pi)


def cosine_modulation():
    fig, ax = plt.subplots(2, 3, figsize=(10.5, 5.3), constrained_layout=True)
    w = np.linspace(-np.pi, np.pi, 2401)
    for row, carrier in enumerate((np.pi/2, np.pi)):
        for col, shift in enumerate((carrier, -carrier)):
            folded = (w-shift+np.pi) % (2*np.pi)-np.pi
            ax[row, col].plot(w/np.pi, .5*(np.abs(folded)<np.pi/4),
                              color=BLUE if col == 0 else RED,
                              drawstyle="steps-mid")
            freq(ax[row, col],
                 r"$\frac{1}{2} R_{\pi/4}(\omega-\omega_0)$" if col == 0
                 else r"$\frac{1}{2} R_{\pi/4}(\omega+\omega_0)$")
        plus = (w-carrier+np.pi) % (2*np.pi)-np.pi
        minus = (w+carrier+np.pi) % (2*np.pi)-np.pi
        y = .5*(np.abs(plus)<np.pi/4)+.5*(np.abs(minus)<np.pi/4)
        ax[row, 2].plot(w/np.pi, y, color=BLUE, drawstyle="steps-mid")
        freq(ax[row, 2], "Sum: carrier $\\pi/2$" if row == 0
             else "Sum: carrier $\\pi$")
        for a in ax[row]:
            a.set(ylim=(-.08, 1.18), yticks=[0, .5, 1],
                  yticklabels=["0", r"$1/2$", "1"])
            a.set_xticks([-1, -.75, -.25, .25, .75, 1],
                         labels=["-1", r"$-3/4$", r"$-1/4$",
                                 r"$1/4$", r"$3/4$", "1"])
    save(fig, OUT / "cosine-modulation.pdf")


def even_odd():
    fig, ax = plt.subplots(2, 3, figsize=(10.5, 5), constrained_layout=True)
    n = np.arange(-3, 4)
    x = 2*(n == -1)+1*(n == 0)+.5*(n == 1)
    xe = (x+x[::-1])/2
    xo = (x-x[::-1])/2
    for a, y, title in zip(ax[0], (x, xe, xo), ("$x[n]$", "$x_e[n]$", "$x_o[n]$")):
        sample(a, n, y, title)
        a.set_xticks(n)
        a.set_ylim(-1, 2.4)
    w = np.linspace(-np.pi, np.pi, 1601)
    re, im = 1+2.5*np.cos(w), 1.5*np.sin(w)
    ax[1, 0].plot(w/np.pi, re, color=BLUE, label=r"$\Re X$")
    ax[1, 0].plot(w/np.pi, im, color=RED, label=r"$\Im X$")
    ax[1, 0].legend(fontsize=9)
    ax[1, 1].plot(w/np.pi, re, color=BLUE)
    ax[1, 2].plot(w/np.pi, im, color=RED)
    for a, title in zip(ax[1], ("Complex spectrum", "Even real part", "Odd imaginary part")):
        freq(a, title)
    save(fig, OUT / "even-odd-spectrum.pdf")


def narrow():
    n = np.arange(-16, 17)
    fig, ax = plt.subplots(figsize=(7.5, 2.6), constrained_layout=True)
    sample(ax, n, sinc_samples(np.pi/4, n)**2, r"$s_{\pi/4}^2[n]$", "$z[n]$")
    ax.plot(0, 1/16, "o", color=RED)
    ax.set_ylim(-.004, .075)
    save(fig, EX / "square-narrow-given.pdf")

    fig, ax = plt.subplots(1, 2, figsize=(9, 2.9), constrained_layout=True)
    w = np.linspace(-np.pi, np.pi, 1801)
    ax[0].plot(w/np.pi, triangle(w, np.pi/4), color=BLUE)
    freq(ax[0], "Ordinary rectangle convolution", "$C_0$")
    ax[0].set(yticks=[0, np.pi/2], yticklabels=["0", r"$\pi/2$"])
    w = np.linspace(-3*np.pi, 3*np.pi, 4001)
    ax[1].plot(w/np.pi, period_sum(w, np.pi/4), color=BLUE)
    freq(ax[1], "Normalize and repeat", "$Z$", (-3, 3))
    ax[1].set(yticks=[0, .25], yticklabels=["0", r"$1/4$"])
    save(fig, EX / "square-narrow-answer.pdf")


def triangle_inverse():
    fig, ax = plt.subplots(1, 2, figsize=(9, 2.9), constrained_layout=True)
    w = np.linspace(-np.pi, np.pi, 1601)
    g = np.maximum(1-4*np.abs(w)/np.pi, 0)
    q = np.maximum(4*np.abs(w)/np.pi-3, 0)
    for a, y, title in zip(ax, (g, q), ("$G(\\omega)$", "$Q(\\omega)$")):
        a.plot(w/np.pi, y, color=BLUE)
        freq(a, title)
        a.set(ylim=(-.08, 1.2), yticks=[0, 1])
        a.set_xticks([-1, -.75, -.25, 0, .25, .75, 1],
                     labels=["-1", r"$-3/4$", r"$-1/4$", "0",
                             r"$1/4$", r"$3/4$", "1"])
    save(fig, EX / "triangle-given.pdf")
    n = np.arange(-18, 19)
    g = 8*sinc_samples(np.pi/8, n)**2
    q = (-1.)**n*g
    fig, ax = plt.subplots(1, 2, figsize=(9, 2.9), constrained_layout=True)
    for a, y, title in zip(ax, (g, q), (r"$8s_{\pi/8}^2[n]$",
                                       r"$8(-1)^ns_{\pi/8}^2[n]$")):
        sample(a, n, y, title)
        a.set_ylim(-.14, .15)
        a.plot(0, 1/8, "o", color=RED)
    save(fig, EX / "triangle-answer.pdf")


def wide():
    n = np.arange(-16, 17)
    fig, ax = plt.subplots(figsize=(7.5, 2.6), constrained_layout=True)
    sample(ax, n, sinc_samples(3*np.pi/4, n)**2, r"$s_{3\pi/4}^2[n]$", "$z[n]$")
    ax.plot(0, 9/16, "o", color=RED)
    ax.set_ylim(-.03, .65)
    save(fig, EX / "square-wide-given.pdf")
    fig, ax = plt.subplots(2, 1, figsize=(8.2, 5), constrained_layout=True)
    w = np.linspace(-3.6*np.pi, 3.6*np.pi, 4001)
    for k, color, label in ((-1, GRAY, "$C_0(\\omega+2\\pi)$"),
                             (0, BLUE, "$C_0(\\omega)$"),
                             (1, RED, "$C_0(\\omega-2\\pi)$")):
        ax[0].plot(w/np.pi, triangle(w-2*k*np.pi, 3*np.pi/4),
                    color=color, label=label)
    freq(ax[0], "Shift ordinary triangles by $2\\pi$", "$C_0$", (-3.6, 3.6))
    ax[0].legend(fontsize=8, loc="upper right")
    ax[0].set(yticks=[0, np.pi, 1.5*np.pi],
              yticklabels=["0", r"$\pi$", r"$3\pi/2$"], ylim=(-.2, 6.6))
    w = np.linspace(-np.pi, np.pi, 1601)
    ax[1].plot(w/np.pi, period_sum(w, 3*np.pi/4), color=BLUE)
    freq(ax[1], "Add overlaps, then divide by $2\\pi$", "$Z$")
    ax[1].set(ylim=(-.05, .9), yticks=[0, .5, .75],
              yticklabels=["0", r"$1/2$", r"$3/4$"],
              xticks=[-1, -.5, 0, .5, 1],
              xticklabels=["-1", r"$-1/2$", "0", r"$1/2$", "1"])
    save(fig, EX / "square-wide-folding.pdf")
    fig, ax = plt.subplots(1, 2, figsize=(9, 2.9), constrained_layout=True)
    sample(ax[0], n, sinc_samples(np.pi/4, n)**2, "Only the sample at zero changes")
    ax[0].plot(0, 9/16, "o", color=RED, label=r"$+\,\frac{1}{2}\delta[n]$")
    ax[0].vlines(0, 1/16, 9/16, color=RED, lw=1.8)
    ax[0].legend(fontsize=9)
    narrow_spec = triangle(w, np.pi/4)/(2*np.pi)
    ax[1].plot(w/np.pi, narrow_spec, "--", color=GRAY, label="narrow triangle")
    ax[1].plot(w/np.pi, np.full_like(w, .5), "--", color=RED, label="constant 1/2")
    ax[1].plot(w/np.pi, narrow_spec+.5, color=BLUE, label="sum")
    freq(ax[1], "Narrow triangle + constant", "$Z$")
    ax[1].set(ylim=(-.05, .9), yticks=[0, .25, .5, .75],
              yticklabels=["0", r"$1/4$", r"$1/2$", r"$3/4$"])
    ax[1].legend(fontsize=8)
    save(fig, EX / "square-wide-answer.pdf")


def recovery():
    w = np.linspace(-np.pi, np.pi, 1601)
    fig, ax = plt.subplots(figsize=(7.5, 2.7), constrained_layout=True)
    ax.plot(w/np.pi, np.sin(w)-np.sin(2*w), color=BLUE)
    freq(ax, "Known imaginary part", r"$\Im X$")
    save(fig, EX / "recovery-given.pdf")
    n = np.arange(-4, 5)
    xo = .5*(n == -1)-.5*(n == 1)-.5*(n == -2)+.5*(n == 2)
    partial = -(n == -2).astype(float)+(n == -1).astype(float)
    fig, ax = plt.subplots(1, 2, figsize=(9, 2.9), constrained_layout=True)
    sample(ax[0], n, xo, "Odd part from $j\\Im X$", "$x_o[n]$")
    sample(ax[1], n, partial, "Negative samples doubled; $x[0]=A$", "$x[n]$")
    for a in ax:
        a.set(xticks=n, ylim=(-1.4, 1.5))
    ax[1].plot(0, 1.1, "o", mfc="white", mec=RED)
    ax[1].text(.15, 1.1, "$A>0$", color=RED)
    save(fig, EX / "recovery-alignment.pdf")
    fig, ax = plt.subplots(1, 2, figsize=(9, 2.9), constrained_layout=True)
    sample(ax[0], n, partial+(n == 0), "$x[0]=1$: energy $3$")
    ax[0].set(xticks=n, ylim=(-1.3, 1.4))
    ax[1].plot(w/np.pi, 1+np.cos(w)-np.cos(2*w), color=BLUE)
    freq(ax[1], "Recovered even real part", r"$\Re X$")
    save(fig, EX / "recovery-answer.pdf")


if __name__ == "__main__":
    cosine_modulation()
    even_odd()
    narrow()
    triangle_inverse()
    wide()
    recovery()
