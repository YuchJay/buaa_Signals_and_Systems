"""DTFT properties and system examples; all frequency coordinates are omega/pi."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from generate import save, style, stem, frequency_axis, impulse, sinc_samples

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "07-dtft"
EX = OUT / "examples"
BLUE, RED = "#25669b", "#b23a2b"


def samples(ax, n, y, title, ylabel="$x[n]$"):
    stem(ax, n, y)
    ax.set(xlabel="$n$", ylabel=ylabel, title=title)


def freq(ax, title, ylabel="$X$", limits=(-1, 1)):
    frequency_axis(ax, limits)
    ax.set(title=title, ylabel=ylabel)


def sign():
    fig, ax = plt.subplots(2, 2, figsize=(9, 5.2), constrained_layout=True)
    n = np.arange(-7, 8)
    samples(ax[0, 0], n, np.sign(n), "Sign sequence")
    ax[0, 0].plot(0, 0, "o", color=RED)
    for lo, hi in ((-1, -.012), (.012, 1)):
        w = np.linspace(lo, hi, 700)
        val = -1 / np.tan(np.pi*w/2)
        ax[0, 1].plot(w, val, color=BLUE)
        ax[1, 0].plot(w, np.abs(val), color=BLUE)
    freq(ax[0, 1], "Imaginary part (principal value)", r"$\Im S$")
    freq(ax[1, 0], "Magnitude away from singularities", "$|S|$")
    ax[0, 1].set_ylim(-4, 4)
    ax[1, 0].set_ylim(-.1, 4)
    for lo, hi, val in ((-1, 0, np.pi/2), (0, 1, -np.pi/2)):
        ax[1, 1].plot([lo, hi], [val, val], color=BLUE)
        ax[1, 1].plot([lo, hi], [val, val], "o", mfc="white", mec=BLUE, ms=4)
    freq(ax[1, 1], "Phase (excluded points left open)", r"$\arg S$")
    ax[1, 1].set(ylim=(-2, 2), yticks=[-np.pi/2, 0, np.pi/2],
                 yticklabels=[r"$-\pi/2$", "0", r"$\pi/2$"])
    save(fig, OUT / "sign.pdf")


def linear_sum():
    fig, ax = plt.subplots(1, 2, figsize=(8.5, 2.8), constrained_layout=True)
    n = np.arange(-12, 13)
    y = sinc_samples(np.pi/4, n) + (n == 0)
    samples(ax[0], n, y, r"$s_{\pi/4}[n]+\delta[n]$")
    ax[0].plot(0, 1.25, "o", color=RED)
    w = np.linspace(-np.pi, np.pi, 1601)
    ax[1].plot(w/np.pi, 1+(np.abs(w)<np.pi/4), color=BLUE,
               drawstyle="steps-mid")
    freq(ax[1], "Rectangle + constant")
    ax[1].set(ylim=(-.1, 2.4), yticks=[0, 1, 2],
              xticks=[-1, -.25, 0, .25, 1],
              xticklabels=["-1", r"$-1/4$", "0", r"$1/4$", "1"])
    save(fig, OUT / "linear-sum.pdf")


def shifts():
    fig, ax = plt.subplots(2, 3, figsize=(10.5, 5.2), constrained_layout=True)
    n = np.arange(-4, 11)
    base = .6 ** np.maximum(n, 0) * (n >= 0)
    delayed = .6 ** np.maximum(n-2, 0) * (n >= 2)
    samples(ax[0, 0], n, base, "Original and delay by 2")
    ax[0, 0].plot(n, delayed, "s", color=RED, ms=3, label="delay")
    ax[0, 0].plot([], [], "o", color=BLUE, label="original")
    ax[0, 0].legend(fontsize=8)
    w = np.linspace(-np.pi, np.pi, 1601)
    X = 1 / (1-.6*np.exp(-1j*w))
    ax[0, 1].plot(w/np.pi, abs(X), color=BLUE, label="original")
    ax[0, 1].plot(w/np.pi, abs(X), "--", color=RED, label="delay")
    freq(ax[0, 1], "Same magnitude", "$|X|$")
    ax[0, 1].legend(fontsize=8)
    ax[0, 2].plot(w/np.pi, np.angle(X), color=BLUE, label="original")
    ax[0, 2].plot(w/np.pi, np.angle(X)-2*w, color=RED, label="delay")
    freq(ax[0, 2], "Phase: add $-2\\omega$", r"$\theta$")
    ax[0, 2].legend(fontsize=8)
    base_rect = (np.abs(w)<np.pi/4).astype(float)
    folded = (w-7*np.pi/8+np.pi) % (2*np.pi)-np.pi
    shifted = (abs(folded)<np.pi/4).astype(float)
    ax[1, 0].plot(w/np.pi, base_rect, color=BLUE, drawstyle="steps-mid")
    freq(ax[1, 0], "Original rectangle")
    extended = np.linspace(-np.pi, 2*np.pi, 2000)
    ax[1, 1].plot(extended/np.pi,
                  (abs(extended-7*np.pi/8)<np.pi/4).astype(float),
                  color=RED, drawstyle="steps-mid")
    freq(ax[1, 1], "Shift right by $7\\pi/8$", limits=(-1, 2))
    ax[1, 1].axvline(1, ls="--", color="#666666")
    ax[1, 2].plot(w/np.pi, shifted, color=RED, drawstyle="steps-mid")
    freq(ax[1, 2], "Fold into one period")
    for a in ax[1]:
        a.set_ylim(-.1, 1.35)
    ax[1, 0].set_xticks([-1, -.25, .25, 1],
                        labels=["-1", r"$-1/4$", r"$1/4$", "1"])
    ax[1, 1].set_xticks([-1, 0, .625, 1.125, 2],
                        labels=["-1", "0", r"$5/8$", r"$9/8$", "2"])
    ax[1, 2].set_xticks([-1, -.875, 0, .625, 1],
                        labels=["-1", r"$-7/8$", "0", r"$5/8$", "1"])
    save(fig, OUT / "shifts.pdf")


def expansion():
    fig, ax = plt.subplots(2, 2, figsize=(8.8, 5), constrained_layout=True)
    n = np.arange(-6, 7)
    w = np.linspace(-2*np.pi, 2*np.pi, 2001)
    for row, factor in enumerate((1, 2)):
        y = ((n % factor == 0) & (abs(n) <= 2*factor)).astype(float)
        samples(ax[row, 0], n, y,
                "Five-point rectangle" if row == 0 else "One zero between samples")
        ax[row, 0].set_xticks(np.arange(-6, 7, 2))
        X = 1+2*np.cos(factor*w)+2*np.cos(2*factor*w)
        ax[row, 1].plot(w/np.pi, X, color=BLUE)
        freq(ax[row, 1], "Period $2\\pi$" if row == 0 else "Period $\\pi$",
             limits=(-2, 2))
        ax[row, 1].set_ylim(-1.6, 5.6)
        if row == 1:
            ax[row, 1].plot(np.arange(-2, 3), np.full(5, 5), "o", color=RED, ms=4)
    save(fig, OUT / "expansion.pdf")


def weighted_exponential():
    fig, ax = plt.subplots(1, 3, figsize=(10, 2.8), constrained_layout=True)
    n = np.arange(-4, 14)
    y = (n+1)*.6**np.maximum(n, 0)*(n>=0)
    samples(ax[0], n, y, r"$(n+1)0.6^nu[n]$")
    w = np.linspace(-np.pi, np.pi, 1601)
    X = 1/(1-.6*np.exp(-1j*w))**2
    ax[1].plot(w/np.pi, abs(X), color=BLUE)
    freq(ax[1], "Magnitude", "$|X|$")
    ax[2].plot(w/np.pi, 2*np.angle(1/(1-.6*np.exp(-1j*w))), color=BLUE)
    freq(ax[2], "Phase", r"$\theta$")
    save(fig, OUT / "weighted-exponential.pdf")


def elementary_systems():
    fig, ax = plt.subplots(2, 3, figsize=(10, 5.1), constrained_layout=True)
    n = np.arange(-3, 6)
    w = np.linspace(-np.pi, np.pi, 1601)
    samples(ax[0, 0], n, (n==0).astype(float)-(n==1), "Difference impulse response", "$h[n]$")
    samples(ax[1, 0], n, (n==2).astype(float), "Delay by 2", "$h[n]$")
    ax[0, 1].plot(w/np.pi, 2*abs(np.sin(w/2)), color=BLUE)
    ax[1, 1].plot(w/np.pi, np.ones_like(w), color=BLUE)
    for row in (0, 1):
        freq(ax[row, 1], "Magnitude", "$|H|$")
        freq(ax[row, 2], "Phase", r"$\arg H$")
    for lo, hi in ((-np.pi, -.005), (.005, np.pi)):
        v = np.linspace(lo, hi, 700)
        ax[0, 2].plot(v/np.pi, np.angle(1-np.exp(-1j*v)), color=BLUE)
    ax[0, 2].plot([0, 0], [-np.pi/2, np.pi/2], "o", mfc="white", mec=BLUE, ms=4)
    ax[0, 2].set(yticks=[-np.pi/2, 0, np.pi/2],
                 yticklabels=[r"$-\pi/2$", "0", r"$\pi/2$"])
    ax[1, 2].plot(w/np.pi, -2*w, color=BLUE)
    ax[1, 2].set(yticks=[-2*np.pi, 0, 2*np.pi],
                 yticklabels=[r"$-2\pi$", "0", r"$2\pi$"])
    save(fig, OUT / "elementary-systems.pdf")


def sinusoidal_response():
    fig, ax = plt.subplots(1, 2, figsize=(9, 3), constrained_layout=True)
    for a in ax:
        freq(a, "Input" if a is ax[0] else "Output: complex weights", "weight")
        a.set(ylim=(-.1, 1.9), yticks=[])
        a.set_xticks([-1, -.25, 0, .25, 1],
                     labels=["-1", r"$-\omega_0/\pi$", "0",
                             r"$\omega_0/\pi$", "1"])
    for p in (-.25, .25):
        impulse(ax[0], p, 1, r"$\pi$")
        impulse(ax[1], p, 1)
    ax[1].text(-.25, 1.25, r"$\pi H(e^{-j\omega_0})$", ha="center", fontsize=10)
    ax[1].text(.25, 1.6, r"$\pi H(e^{j\omega_0})$", ha="center", fontsize=10)
    save(fig, OUT / "sinusoidal-response.pdf")


def principal():
    fig, ax = plt.subplots(1, 3, figsize=(10, 2.8), constrained_layout=True)
    w = np.linspace(-np.pi, np.pi, 1601)
    ax[0].plot([-1, 1], [.5, .5], color=BLUE)
    freq(ax[0], "First factor: real part", r"$\Re Q$")
    ax[0].set(ylim=(-.1, .8), yticks=[0, .5], yticklabels=["0", r"$1/2$"])
    for lo, hi in ((-1, -.012), (.012, 1)):
        v = np.linspace(lo, hi, 600)
        ax[1].plot(v, -.5/np.tan(np.pi*v/2), color=BLUE)
    freq(ax[1], "First factor: imaginary part", r"$\Im Q$")
    ax[1].set_ylim(-3, 3)
    ax[2].plot(w/np.pi, 1+2*np.cos(w)+2*np.cos(2*w), color=BLUE)
    freq(ax[2], "Second factor", "$V$")
    save(fig, EX / "principal-given.pdf")

    fig, ax = plt.subplots(3, 2, figsize=(8.8, 6.8), constrained_layout=True)
    k = np.arange(-3, 4)
    for a, n in zip(ax.ravel(), range(-3, 3)):
        stem(a, k, (abs(k)<=2).astype(float))
        a.plot(k, np.where(k<=n, .5, -.5), "o", color=RED, ms=4)
        a.axvline(n, color=RED, ls="--", lw=.7)
        a.set(xlabel="$k$", ylabel="aligned samples", title=fr"$n={n}$",
              ylim=(-.8, 1.3), xticks=k, yticks=[-.5, 0, .5, 1])
    save(fig, EX / "principal-alignment.pdf")

    fig, ax = plt.subplots(1, 2, figsize=(8.5, 2.8), constrained_layout=True)
    n = np.arange(-7, 8)
    c = np.clip(n+3, 0, 5)
    samples(ax[0], n, c-2.5, "Principal-value inverse", "$z[n]$")
    samples(ax[1], n, c, "Running sum", "$c[n]$")
    save(fig, EX / "principal-answer.pdf")


def exponential_examples():
    n = np.arange(-3, 12)
    nonneg = n>=0
    fig, ax = plt.subplots(1, 2, figsize=(8.5, 2.8), constrained_layout=True)
    samples(ax[0], n, (1/3)**np.maximum(n, 0)*nonneg, "Input", "$x[n]$")
    samples(ax[1], n, .5**np.maximum(n, 0)*nonneg, "Impulse response", "$h[n]$")
    save(fig, EX / "exponential-given.pdf")
    fig, ax = plt.subplots(1, 2, figsize=(8.5, 2.8), constrained_layout=True)
    ydiff = (.5**(np.maximum(n, 0)+1)-(1/3)**(np.maximum(n, 0)+1))/(.5-1/3)*nonneg
    yequal = (n+1)*.5**np.maximum(n, 0)*nonneg
    samples(ax[0], n, ydiff, r"$\alpha=1/2,\ \beta=1/3$", "$y[n]$")
    samples(ax[1], n, yequal, r"$\alpha=\beta=1/2$", "$y[n]$")
    save(fig, EX / "exponential-answer.pdf")

    fig, ax = plt.subplots(1, 2, figsize=(8.5, 2.8), constrained_layout=True)
    samples(ax[0], n, .5**np.maximum(n, 0)*nonneg, "Known input", "$x[n]$")
    samples(ax[1], n, (3*.5**np.maximum(n, 0)-2*(1/3)**np.maximum(n, 0))*nonneg,
            "Known output", "$y[n]$")
    save(fig, EX / "identify-given.pdf")
    fig, ax = plt.subplots(1, 2, figsize=(8.5, 2.8), constrained_layout=True)
    samples(ax[0], n, (1/3)**np.maximum(n, 0)*nonneg, "Recovered impulse response", "$h[n]$")
    w = np.linspace(-np.pi, np.pi, 1601)
    ax[1].plot(w/np.pi, abs(1/(1-(1/3)*np.exp(-1j*w))), color=BLUE)
    freq(ax[1], "Magnitude response", "$|H|$")
    ax[1].set_ylim(0, 1.7)
    save(fig, EX / "identify-answer.pdf")

    fig, a = plt.subplots(figsize=(7, 2.5), constrained_layout=True)
    samples(a, n, .5**np.maximum(n, 0)*nonneg, "Input to the difference equation", "$x[n]$")
    save(fig, EX / "equation-given.pdf")
    fig, ax = plt.subplots(1, 2, figsize=(8.5, 2.8), constrained_layout=True)
    h = (.6*.5**np.maximum(n, 0)+.4*(-1/3)**np.maximum(n, 0))*nonneg
    y = (.6*(n+1)*.5**np.maximum(n, 0)+.24*.5**np.maximum(n, 0)
         +.16*(-1/3)**np.maximum(n, 0))*nonneg
    samples(ax[0], n, h, "Impulse response", "$h[n]$")
    samples(ax[1], n, y, "Zero-state output", "$y[n]$")
    save(fig, EX / "equation-answer.pdf")


if __name__ == "__main__":
    for func in (sign, linear_sum, shifts, expansion, weighted_exponential,
                 elementary_systems, sinusoidal_response, principal,
                 exponential_examples):
        func()
