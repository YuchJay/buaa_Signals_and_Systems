"""Generate DTFT figures for Chapter 7."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "07-dtft"
EXAMPLES = OUT / "examples"
BLUE, RED, GRAY = "#25669b", "#b23a2b", "#666666"


def save(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight",
                metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def style(ax, xlim=None, ylim=None):
    ax.axhline(0, color="#333333", lw=0.7, zorder=0)
    ax.axvline(0, color="#333333", lw=0.7, zorder=0)
    ax.grid(color="#dddddd", lw=0.45)
    ax.spines[["top", "right"]].set_visible(False)
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)


def stem(ax, n, y, color=BLUE, label=None):
    markerline, stemlines, baseline = ax.stem(n, y, linefmt=color,
                                               markerfmt="o", basefmt=" ")
    plt.setp(stemlines, linewidth=1.2)
    plt.setp(markerline, markersize=3.5)
    if label:
        ax.set_title(label)
    style(ax)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=7, integer=True))


def sinc_samples(gamma, n):
    return (gamma / np.pi) * np.sinc(gamma * n / np.pi)


def frequency_axis(ax, limits=(-2.5, 2.5)):
    """Frequency coordinate is omega/pi on every frequency panel."""
    style(ax, limits)
    ax.set_xlabel(r"$\omega/\pi$")
    ax.set_xticks(np.arange(np.ceil(limits[0]), np.floor(limits[1]) + 1))
    ax.axvspan(-1, 1, color="#eeeeee", zorder=-2)


def impulse(ax, x, weight, text=None, color=RED):
    ax.annotate("", xy=(x, weight), xytext=(x, 0),
                arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.5})
    if text:
        ax.text(x + 0.08, weight, text, color=color, va="center", fontsize=9)


def exponential():
    fig, ax = plt.subplots(2, 3, figsize=(10, 5.8), constrained_layout=True)
    n = np.arange(-5, 10)
    w = np.linspace(-2*np.pi, 2*np.pi, 2001)
    for row, a in enumerate((0.7, -0.7)):
        y = np.where(n >= 0, a ** n, 0.0)
        stem(ax[row, 0], n, y)
        ax[row, 0].set(xlabel="$n$", ylabel="$x[n]$", title=fr"$a={a}$")
        ax[row, 0].set_xticks([-4, 0, 4, 8])
        ax[row, 0].set_ylim(-1.15, 1.15)
        X = 1 / (1 - a * np.exp(-1j * w))
        ax[row, 1].plot(w / np.pi, np.abs(X), color=BLUE)
        frequency_axis(ax[row, 1], (-2, 2))
        ax[row, 1].set(ylabel=r"$|X|$", title="Magnitude", ylim=(-.05, 3.6))
        ax[row, 2].plot(w / np.pi, np.angle(X), color=BLUE)
        frequency_axis(ax[row, 2], (-2, 2))
        ax[row, 2].set(title="Phase", ylabel=r"$\theta(\omega)$",
                       ylim=(-1, 1), yticks=[-.75, 0, .75])
    save(fig, OUT / "exponential.pdf")


def impulse_constant():
    fig, ax = plt.subplots(2, 2, figsize=(8.4, 4.8), constrained_layout=True)
    n = np.arange(-5, 6)
    stem(ax[0, 0], n, (n == 0).astype(float))
    ax[0, 0].set(xlabel="$n$", ylabel="$x[n]$", title=r"$\delta[n]$")
    w = np.linspace(-3 * np.pi, 3 * np.pi, 500)
    ax[0, 1].plot(w / np.pi, np.ones_like(w), color=BLUE)
    style(ax[0, 1], (-3, 3), (-0.1, 1.25))
    ax[0, 1].set(xlabel=r"$\omega/\pi$", ylabel="$X$", title="Constant spectrum")
    stem(ax[1, 0], n, np.ones_like(n))
    style(ax[1, 0], (-5.5, 5.5), (-0.1, 1.25))
    ax[1, 0].set(xlabel="$n$", ylabel="$x[n]$", title="$1$")
    for k in range(-1, 2):
        impulse(ax[1, 1], 2 * k, 1, r"$2\pi$")
    frequency_axis(ax[1, 1], (-3, 3))
    ax[1, 1].set_ylim(-.1, 1.35)
    ax[1, 1].set(xlabel=r"$\omega/\pi$", ylabel="weight",
                 title=r"$2\pi\sum_k\delta(\omega-2k\pi)$")
    ax[1, 1].set_yticks([])
    save(fig, OUT / "impulse-constant.pdf")


def rectangle():
    fig, ax = plt.subplots(2, 2, figsize=(9, 5.4), constrained_layout=True)
    n = np.arange(-4, 5)
    stem(ax[0, 0], n, (np.abs(n) <= 2).astype(float))
    ax[0, 0].set(xlabel="$n$", ylabel="$x[n]$", title="Five-point rectangle")
    w = np.linspace(-np.pi, np.pi, 2001)
    X = 1 + 2*np.cos(w) + 2*np.cos(2*w)
    ax[0, 1].plot(w / np.pi, X, color=BLUE)
    style(ax[0, 1], (-1, 1))
    ax[0, 1].set(xlabel=r"$\omega/\pi$", ylabel="$X$", title="Signed spectrum")
    ax[1, 0].plot(w / np.pi, np.abs(X), color=BLUE)
    style(ax[1, 0], (-1, 1))
    ax[1, 0].set(xlabel=r"$\omega/\pi$", ylabel=r"$|X|$", title="Magnitude")
    roots = [-1, -.8, -.4, .4, .8, 1]
    for left, right in zip(roots[:-1], roots[1:]):
        value = 1 + 2*np.cos(np.pi*(left+right)/2) + 2*np.cos(np.pi*(left+right))
        phase = 0 if value > 0 else np.pi
        ax[1, 1].plot([left, right], [phase, phase], color=BLUE)
        for point in (left, right):
            if abs(point) < 1:
                ax[1, 1].plot(point, phase, "o", mfc="white", mec=BLUE, ms=4)
    style(ax[1, 1], (-1, 1), (-0.2, 3.5))
    ax[1, 1].set(xlabel=r"$\omega/\pi$", ylabel=r"$\arg X$",
                 title="Phase (zeros omitted)", yticks=[0, np.pi],
                 yticklabels=["0", r"$\pi$"])
    for panel in (ax[0, 1], ax[1, 0], ax[1, 1]):
        panel.set_xticks([-1, -.8, -.4, 0, .4, .8, 1],
                         labels=["-1", r"$-4/5$", r"$-2/5$", "0",
                                 r"$2/5$", r"$4/5$", "1"])
    save(fig, OUT / "rectangle.pdf")


def sinc():
    fig, ax = plt.subplots(2, 2, figsize=(8.5, 5.4), constrained_layout=True)
    n = np.arange(-16, 17)
    for row, width, parameter in ((0, .25, r"\pi/4"),
                                  (1, .75, r"3\pi/4")):
        stem(ax[row, 0], n, sinc_samples(width*np.pi, n))
        ax[row, 0].plot(0, width, "o", color=RED)
        ax[row, 0].set(xlabel="$n$", ylabel=fr"$s_{{{parameter}}}[n]$",
                       title=fr"$\omega_0={parameter}$")
        for k in range(-1, 2):
            left, right = 2*k-width, 2*k+width
            ax[row, 1].plot([left, left, right, right], [0, 1, 1, 0],
                           color=BLUE, lw=1.5)
            ax[row, 1].plot([left, right], [.5, .5], "o", color=RED, ms=3)
        frequency_axis(ax[row, 1])
        ax[row, 1].set(ylabel="$X$", title="Periodic rectangle",
                       ylim=(-.12, 1.3), yticks=[0, .5, 1])
        cutoff = "1/4" if row == 0 else "3/4"
        if row == 0:
            ax[row, 1].set_xticks([-2, -1, -width, width, 1, 2],
                                  labels=["-2", "-1", fr"$-{cutoff}$",
                                          fr"${cutoff}$", "1", "2"])
        else:
            ax[row, 1].set_xticks([-2, -width, 0, width, 2],
                                  labels=["-2", fr"$-{cutoff}$", "0",
                                          fr"${cutoff}$", "2"])
    save(fig, OUT / "sinc.pdf")


def step():
    fig, ax = plt.subplots(1, 3, figsize=(10, 3.3), constrained_layout=True)
    n = np.arange(-5, 9)
    stem(ax[0], n, (n >= 0).astype(float))
    ax[0].set(xlabel="$n$", ylabel="$u[n]$", title="Unit step", ylim=(-.1, 1.3))
    frequency_axis(ax[1])
    ax[1].plot([-2.5, 2.5], [.5, .5], color=BLUE)
    for k in (-1, 0, 1):
        impulse(ax[1], 2*k, 1.5, r"$\pi$")
    ax[1].set(ylabel=r"$\Re X$", title="Real part: constant + impulses",
              ylim=(-.1, 1.9), yticks=[0, .5], yticklabels=["0", r"$1/2$"])
    frequency_axis(ax[2])
    for left, right in [(-2.5, -2.012), (-1.988, -.012),
                        (.012, 1.988), (2.012, 2.5)]:
        v = np.linspace(left, right, 600)
        ax[2].plot(v, -.5/np.tan(np.pi*v/2), color=BLUE)
    ax[2].set(ylabel=r"$\Im X$", title="Imaginary part (principal value)",
              ylim=(-3, 3))
    save(fig, OUT / "step.pdf")


def harmonics():
    fig, ax = plt.subplots(2, 3, figsize=(9.5, 5.0), constrained_layout=True)
    n = np.arange(-8, 9)
    w0 = np.pi / 4
    for row, signal, title in [(0, np.cos(w0 * n), "Cosine"),
                                (1, np.sin(w0 * n), "Sine")]:
        stem(ax[row, 0], n, signal)
        ax[row, 0].set(xlabel=r"$n$", ylabel="$x[n]$", title=title)
        if row == 0:
            for p in (-.25, .25):
                impulse(ax[row, 1], p, 1, r"$\pi$")
            ax[row, 1].set(title=r"$\Re X$: impulse weights", ylim=(-.2, 1.4),
                           yticks=[])
            ax[row, 2].set(ylim=(-.5, .5),
                           title="Line phase",
                           yticks=[0, np.pi], yticklabels=["0", r"$\pi$"])
            ax[row, 2].plot([-.25, .25], [0, 0], "o", color=BLUE)
        else:
            impulse(ax[row, 1], -.25, 1, r"$+\pi$")
            impulse(ax[row, 1], .25, -1, r"$-\pi$")
            ax[row, 1].set(title=r"$\Im X$: impulse weights", ylim=(-1.4, 1.4),
                           yticks=[])
            ax[row, 2].set(ylim=(-2.2, 2.2),
                           title="Line phase",
                           yticks=[-np.pi/2, 0, np.pi/2],
                           yticklabels=[r"$-\pi/2$", "0", r"$\pi/2$"])
            ax[row, 2].plot([-.25, .25], [np.pi/2, -np.pi/2],
                            "o", color=BLUE)
        for panel in (ax[row, 1], ax[row, 2]):
            frequency_axis(panel, (-1, 1))
            panel.set_xticks([-1, -.25, 0, .25, 1],
                             labels=["-1", r"$-1/4$", "0", r"$1/4$", "1"])
    save(fig, OUT / "harmonics.pdf")


def alternating():
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.0), constrained_layout=True)
    n = np.arange(-8, 9)
    stem(ax[0], n, (-1.0) ** n)
    ax[0].set(xlabel="$n$", ylabel="$(-1)^n$", title="Alternating sequence")
    for p in (-3, -1, 1, 3):
        impulse(ax[1], p, 1, r"$2\pi$")
    frequency_axis(ax[1], (-3.5, 3.5))
    ax[1].set_ylim(-.1, 1.35)
    ax[1].set(xlabel=r"$\omega/\pi$", ylabel="weight",
              title=r"Odd multiples of $\pi$",
              yticks=[])
    save(fig, OUT / "alternating.pdf")


def sinc_parameters():
    fig, ax = plt.subplots(3, 2, figsize=(9.0, 6.5), constrained_layout=True)
    params = (-np.pi/4, 5*np.pi/4, 9*np.pi/4)
    labels = (r"-\pi/4", r"5\pi/4", r"9\pi/4")
    w = np.linspace(-np.pi, np.pi, 1500)
    n = np.arange(-12, 13)
    for row, gamma in enumerate(params):
        y = sinc_samples(gamma, n)
        stem(ax[row, 0], n, y)
        ax[row, 0].plot(0, gamma/np.pi, "o", color=RED, ms=5)
        ax[row, 0].set(xlabel="$n$", ylabel=fr"$s_{{{labels[row]}}}[n]$",
                       title=fr"$\gamma={labels[row]}$")
        S = np.zeros_like(w)
        for q in range(-3, 4):
            S += ((np.abs(w - 2*q*np.pi) < abs(gamma)).astype(float)
                  * np.sign(gamma))
        ax[row, 1].plot(w / np.pi, S, color=BLUE, drawstyle="steps-mid")
        style(ax[row, 1], (-1, 1), (-1.3, 3.5))
        ax[row, 1].set(xlabel=r"$\omega/\pi$", ylabel=r"$S_\gamma$",
                       title="Folded periodic spectrum")
        width = .75 if row == 1 else .25
        cutoff = "3/4" if row == 1 else "1/4"
        ax[row, 1].set_xticks([-1, -width, 0, width, 1],
                              labels=["-1", fr"$-{cutoff}$", "0",
                                      fr"${cutoff}$", "1"])
    save(fig, OUT / "sinc-parameters.pdf")


def example_stepped():
    fig, ax = plt.subplots(figsize=(8.5, 2.8), constrained_layout=True)
    w = np.linspace(-2.2*np.pi, 2.2*np.pi, 6000)
    folded = (w+np.pi/2) % np.pi - np.pi/2
    X = (np.abs(folded) < np.pi/8).astype(float) + (np.abs(folded) < 3*np.pi/8)
    ax.plot(w / np.pi, X, color=BLUE, drawstyle="steps-mid")
    style(ax, (-2.2, 2.2), (-.15, 2.35))
    ax.set(xlabel=r"$\omega/\pi$", ylabel="$X$", title="Given periodic stepped spectrum")
    ax.set_xticks([-2, -1, -3/8, -1/8, 1/8, 3/8, 1, 2],
                  labels=["-2", "-1", r"$-3/8$", r"$-1/8$",
                          r"$1/8$", r"$3/8$", "1", "2"])
    ax.set_yticks([0, 1, 2])
    save(fig, EXAMPLES / "stepped-given.pdf")

    fig, ax = plt.subplots(figsize=(8.5, 2.8), constrained_layout=True)
    ns = np.arange(-18, 19)
    val = (1 + (-1.0)**ns) * (sinc_samples(3*np.pi/8, ns) + sinc_samples(np.pi/8, ns))
    stem(ax, ns, val)
    ax.plot([0], [1], "o", color=RED, ms=5)
    ax.text(.5, 1.03, "$x[0]=1$", color=RED)
    ax.set(xlabel="$n$", ylabel="$x[n]$", title="Recovered sequence")
    save(fig, EXAMPLES / "stepped-answer.pdf")


def example_highpass():
    fig, ax = plt.subplots(figsize=(8.5, 2.8), constrained_layout=True)
    w = np.linspace(-2.2*np.pi, 2.2*np.pi, 6000)
    folded = (w+np.pi) % (2*np.pi) - np.pi
    X = (np.abs(folded) > 3*np.pi/4).astype(float)
    ax.plot(w / np.pi, X, color=BLUE, drawstyle="steps-mid")
    style(ax, (-2.2, 2.2), (-.15, 1.25))
    ax.set(xlabel=r"$\omega/\pi$", ylabel="$X$", title="Given periodic high-pass spectrum")
    ax.set_xticks([-2, -1, -.75, 0, .75, 1, 2],
                  labels=["-2", "-1", r"$-3/4$", "0", r"$3/4$", "1", "2"])
    ax.set_yticks([0, 1])
    save(fig, EXAMPLES / "highpass-given.pdf")

    fig, ax = plt.subplots(figsize=(8.5, 2.8), constrained_layout=True)
    ns = np.arange(-18, 19)
    val = (ns == 0).astype(float) - sinc_samples(3*np.pi/4, ns)
    stem(ax, ns, val)
    ax.plot([0], [.25], "o", color=RED, ms=5)
    ax.text(.5, .29, "$x[0]=1/4$", color=RED)
    ax.set(xlabel="$n$", ylabel="$x[n]$", title="Recovered high-pass sequence",
           ylim=(-.27, .36))
    save(fig, EXAMPLES / "highpass-answer.pdf")


if __name__ == "__main__":
    for func in (exponential, impulse_constant, rectangle, sinc, step,
                 harmonics, alternating, sinc_parameters,
                 example_stepped, example_highpass):
        func()
