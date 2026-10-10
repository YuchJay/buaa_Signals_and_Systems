"""Hilbert transform, analytic signal, and instantaneous parameter figures."""

import numpy as np
import matplotlib.pyplot as plt
from generate import save, style, impulse, BLUE, RED, GRAY, GREEN

plt.rcParams.update({"font.size": 10, "axes.titlesize": 11})


def causal_parts():
    w = np.linspace(-5, 5, 1201)
    fig, aa = plt.subplots(1, 2, figsize=(9.5, 3), constrained_layout=True)
    aa[0].plot(w, 1/(1+w*w), color=BLUE)
    aa[1].plot(w, -w/(1+w*w), color=RED)
    for ax in aa:
        style(ax, (-5, 5)); ax.set_xlabel(r"$\Omega$")
    aa[0].set(title=r"$R(\Omega)=1/(1+\Omega^2)$", ylim=(-.1, 1.15))
    aa[1].set(title=r"$I(\Omega)=-\Omega/(1+\Omega^2)$", ylim=(-.65, .65))
    save(fig, "causal-spectrum-parts.pdf")


def response():
    fig, aa = plt.subplots(1, 3, figsize=(11, 2.9), constrained_layout=True)
    for ax in aa:
        style(ax, (-3, 3)); ax.set_xlabel(r"$\Omega$")
    for lo, hi, s in [(-3, 0, 1), (0, 3, -1)]:
        w = np.linspace(lo, hi, 301)
        aa[0].plot(w, w*0+s, color=BLUE)
        aa[1].plot(w, w*0+1, color=GREEN)
        aa[2].plot(w, w*0+s*np.pi/2, color=RED)
        aa[0].plot(0, s, "o", color=BLUE, mfc="white", ms=4)
        aa[1].plot(0, 1, "o", color=GREEN, mfc="white", ms=4)
        aa[2].plot(0, s*np.pi/2, "o", color=RED, mfc="white", ms=4)
    aa[0].plot(0, 0, "o", color=BLUE, ms=4)
    aa[1].plot(0, 0, "o", color=GREEN, ms=4)
    aa[0].set(title=r"$\mathrm{Im}\,G_{\rm H}$", ylim=(-1.5, 1.5))
    aa[1].set(title=r"$|G_{\rm H}|$", ylim=(-.2, 1.5))
    aa[2].set(title=r"$\arg G_{\rm H}$", ylim=(-2.2, 2.2))
    aa[2].set_yticks([-np.pi/2, 0, np.pi/2], [r"$-\pi/2$", "0", r"$\pi/2$"])
    save(fig, "hilbert-response.pdf")


def sinusoids():
    fig, aa = plt.subplots(2, 2, figsize=(10, 5.6), constrained_layout=True)
    t = np.linspace(-2*np.pi, 2*np.pi, 1201)
    for ax, inp, out, labels in [
        (aa[0, 0], np.cos(t), np.sin(t), ("$\\cos t$", "$\\sin t$")),
        (aa[0, 1], np.sin(t), -np.cos(t), ("$\\sin t$", "$-\\cos t$"))]:
        ax.plot(t, inp, color=GRAY, ls="--", label="input "+labels[0])
        ax.plot(t, out, color=BLUE, label="output "+labels[1])
        style(ax, (-2*np.pi, 2*np.pi), (-1.35, 1.4))
        ax.set_xlabel("$t$"); ax.legend(fontsize=9, loc="upper right")
        ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
                      [r"$-2\pi$", r"$-\pi$", "0", r"$\pi$", r"$2\pi$"])
    impulse(aa[1, 0], -1, np.pi, r"$\pi$", dy=.1)
    impulse(aa[1, 0], 1, -np.pi, r"$-\pi$", dy=-.5)
    for p in (-1, 1):
        impulse(aa[1, 1], p, -np.pi, r"$-\pi$", dy=-.5)
    for ax in aa[1]:
        style(ax, (-2, 2), (-4.1, 4.1))
        ax.set_xlabel(r"$\Omega$")
        ax.set_xticks([-1, 0, 1], [r"$-\Omega_0$", "0", r"$\Omega_0$"])
    aa[1, 0].set_title(r"Output $\sin t$: imaginary spectrum")
    aa[1, 1].set_title(r"Output $-\cos t$: real spectrum")
    save(fig, "hilbert-sinusoid.pdf")


def analytic_spectrum():
    fig, aa = plt.subplots(1, 2, figsize=(10, 3.1), constrained_layout=True)
    w = np.linspace(-7, 7, 1401)
    def tri(c):
        return np.maximum(1-np.abs(w-c), 0)
    aa[0].plot(w, (tri(-4)+tri(4))/2, color=BLUE)
    aa[1].plot(w, tri(4), color=RED)
    for ax in aa:
        style(ax, (-7, 7), (-.1, 1.3))
        ax.set(xlabel=r"$\Omega$")
        ax.set_xticks([-4, 0, 4], [r"$-\Omega_0$", "0", r"$\Omega_0$"])
        ax.set_yticks([0, .5, 1])
    aa[0].set_title(r"Real signal: $X(\mathrm{j}\Omega)$")
    aa[1].set_title(r"Analytic signal: $Z(\mathrm{j}\Omega)$")
    save(fig, "analytic-spectrum.pdf")


def envelope():
    t = np.linspace(0, 2*np.pi, 2401)
    a = 1+.5*np.cos(t)
    x, hx = a*np.cos(8*t), a*np.sin(8*t)
    fig, aa = plt.subplots(3, 1, figsize=(10, 6.5), constrained_layout=True)
    aa[0].plot(t, x, color=BLUE, lw=1, label="$x(t)$")
    aa[0].plot(t, a, color=RED, label="$A(t)$")
    aa[0].plot(t, -a, color=RED)
    aa[0].set(ylim=(-1.8, 1.8), title="Signal and envelope")
    aa[0].legend(loc="upper right", fontsize=9)
    ph = np.angle(np.exp(1j*8*t))
    ph[np.r_[False, np.abs(np.diff(ph)) > np.pi]] = np.nan
    aa[1].plot(t, ph, color=GRAY, lw=1, label="principal phase")
    aa[1].plot(t, 8*t, color=GREEN, label="unwrapped phase")
    aa[1].set(ylabel="phase (rad)", title="Principal and continuous phases")
    aa[1].legend(fontsize=9)
    aa[2].plot(t, np.full_like(t, 8), color=BLUE)
    aa[2].set(ylim=(0, 10), ylabel=r"$\Omega_{\rm inst}$", title="Instantaneous angular frequency")
    for ax in aa:
        style(ax, (0, 2*np.pi))
        ax.set_xticks([0, np.pi, 2*np.pi], ["0", r"$\pi$", r"$2\pi$"])
        ax.set_xlabel("$t$")
    save(fig, "instantaneous-envelope.pdf")
    fig, ax = plt.subplots(figsize=(9, 2.7), constrained_layout=True)
    ax.plot(t, x, color=BLUE)
    style(ax, (0, 2*np.pi), (-1.8, 1.8))
    ax.set(xlabel="$t$", ylabel="$x(t)$", title=r"$(1+\frac{1}{2}\cos t)\cos(8t)$")
    ax.set_xticks([0, np.pi, 2*np.pi], ["0", r"$\pi$", r"$2\pi$"])
    save(fig, "envelope-question.pdf")
    fig, aa = plt.subplots(1, 2, figsize=(10, 3.2), constrained_layout=True)
    aa[0].plot(t, hx, color=BLUE, label=r"$\widehat x(t)$")
    aa[0].plot(t, a, color=RED, label="$A(t)$")
    aa[0].plot(t, -a, color=RED)
    style(aa[0], (0, 2*np.pi), (-1.8, 1.8))
    aa[0].set(xlabel="$t$", title="Hilbert transform and envelope")
    aa[0].set_xticks([0, np.pi, 2*np.pi], ["0", r"$\pi$", r"$2\pi$"])
    aa[0].legend(fontsize=9)
    for p, weight, label in [(7, np.pi/2, r"$\pi/2$"),
                             (8, 2*np.pi, r"$2\pi$"),
                             (9, np.pi/2, r"$\pi/2$")]:
        impulse(aa[1], p, weight, label, dx=.12, dy=.1)
    style(aa[1], (-2, 11), (-.2, 7.7))
    aa[1].set(xlabel=r"$\Omega$", title="Analytic spectrum: impulse weights")
    aa[1].set_xticks([0, 7, 8, 9])
    save(fig, "envelope-answer.pdf")


if __name__ == "__main__":
    causal_parts()
    response()
    sinusoids()
    analytic_spectrum()
    envelope()
    print("wrote 7 Hilbert transform figures")
