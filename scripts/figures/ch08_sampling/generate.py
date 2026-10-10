"""Sampling figures for Chapter 8, up to zero-order hold."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "08-sampling"
BLUE, RED, GRAY, GREEN = "#25669b", "#b23a2b", "#666666", "#2f7d4a"


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, bbox_inches="tight",
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


def hump(w, center, half, height):
    u = (w - center) / half
    return np.where(np.abs(u) <= 1, height * 0.5 * (1 + np.cos(np.pi * u)), 0.0)


def impulse(ax, x, weight, text=None, color=RED, dx=0.08, dy=0.04):
    ax.annotate(
        "", xy=(x, weight), xytext=(x, 0),
        arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.35},
    )
    if text:
        ax.text(x + dx, weight + dy, text, color=color, fontsize=8, va="bottom")


def three_relations():
    fig, ax = plt.subplots(3, 2, figsize=(10.2, 8.4), constrained_layout=True)
    t = np.linspace(-4.2, 4.2, 900)
    x = np.exp(-0.18 * t**2) * np.cos(1.4 * t)
    style(ax[0, 0], (-4.2, 4.2), (-1.25, 1.45))
    ax[0, 0].plot(t, x, color=BLUE, lw=1.5)
    n = np.arange(-4, 5)
    tn = n.astype(float)
    xn = np.exp(-0.18 * tn**2) * np.cos(1.4 * tn)
    ax[0, 0].vlines(tn, 0, xn, color=GREEN, lw=0.8, alpha=0.85)
    ax[0, 0].plot(tn, xn, "o", color=GREEN, ms=3.5)
    ax[0, 0].set(xlabel="$t$", ylabel="$x(t)$", title="Continuous-time signal")
    ax[0, 0].set_xticks([-4, -2, 0, 2, 4])
    ax[0, 0].annotate(
        "", xy=(1, -1.05), xytext=(0, -1.05),
        arrowprops={"arrowstyle": "<->", "color": GREEN, "lw": 1.0},
    )
    ax[0, 0].text(0.5, -0.92, r"$T=1$", color=GREEN, ha="center", fontsize=8)

    # T = 1, so Omega_s = 2 pi and replica height is 1/T = 1.
    w = np.linspace(-10, 10, 2001)
    style(ax[0, 1], (-10, 10), (-0.15, 1.35))
    ax[0, 1].plot(w, hump(w, 0, 1.5, 1), color=BLUE, lw=1.5)
    ax[0, 1].axvline(-1.5, color=GRAY, ls="--", lw=0.7)
    ax[0, 1].axvline(1.5, color=GRAY, ls="--", lw=0.7)
    ax[0, 1].text(-1.5, 1.12, r"$-\Omega_M$", ha="center", fontsize=8)
    ax[0, 1].text(1.5, 1.12, r"$\Omega_M$", ha="center", fontsize=8)
    ax[0, 1].set(xlabel=r"$\Omega$", ylabel=r"$X(\mathrm{j}\Omega)$",
                 title="Bandlimited spectrum")

    style(ax[1, 0], (-4.2, 4.2), (-1.15, 1.45))
    for ti, yi in zip(tn, xn):
        impulse(ax[1, 0], ti, yi if abs(yi) > 0.02 else 0.02, color=BLUE, text=None)
    ax[1, 0].plot(t, x, color=GRAY, lw=0.8, ls="--")
    ax[1, 0].set(xlabel="$t$", ylabel=r"$x_p(t)$", title="Impulse-train samples")
    ax[1, 0].set_xticks([-4, -2, 0, 2, 4])

    style(ax[1, 1], (-10, 10), (-0.08, 1.35))
    spec = sum(hump(w, k * 2 * np.pi, 1.5, 1.0) for k in range(-1, 2))
    ax[1, 1].plot(w, spec, color=BLUE, lw=1.5)
    ax[1, 1].text(0, 1.08, r"$1/T$", color=RED, ha="center", fontsize=8)
    ax[1, 1].text(2 * np.pi, -0.06, r"$\Omega_s$", ha="center", fontsize=8)
    ax[1, 1].text(-2 * np.pi, -0.06, r"$-\Omega_s$", ha="center", fontsize=8)
    ax[1, 1].set(xlabel=r"$\Omega$", ylabel=r"$X_p(\mathrm{j}\Omega)$",
                 title="Replicas, no overlap")

    style(ax[2, 0], (-4.5, 4.5), (-0.75, 1.25))
    markerline, stemlines, _ = ax[2, 0].stem(
        n, xn, linefmt=BLUE, markerfmt="o", basefmt=" ")
    plt.setp(stemlines, linewidth=1.2)
    plt.setp(markerline, markersize=3.6, color=BLUE)
    ax[2, 0].set(xlabel="$n$", ylabel="$x[n]$", title="Sample sequence")
    ax[2, 0].set_xticks(n)

    wd = np.linspace(-2.4 * np.pi, 2.4 * np.pi, 1801)
    # T = 1: omega = Omega, half-width Omega_M = 1.5 < pi.
    style(ax[2, 1], (-2.4 * np.pi, 2.4 * np.pi), (-0.08, 1.35))
    disc = sum(hump(wd, 2 * k * np.pi, 1.5, 1.0) for k in range(-2, 3))
    ax[2, 1].plot(wd, disc, color=BLUE, lw=1.5)
    ax[2, 1].axvspan(-np.pi, np.pi, color="#eeeeee", zorder=-2)
    ax[2, 1].set_xticks([-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi])
    ax[2, 1].set_xticklabels([r"$-2\pi$", r"$-\pi$", "$0$", r"$\pi$", r"$2\pi$"])
    ax[2, 1].text(0, 1.08, r"$1/T$", color=RED, ha="center", fontsize=8)
    ax[2, 1].axvline(1.5, color=GRAY, ls=":", lw=0.7)
    ax[2, 1].axvline(-1.5, color=GRAY, ls=":", lw=0.7)
    ax[2, 1].text(1.55, 0.22, r"$\Omega_M T$", color=GRAY, fontsize=7, ha="left")
    ax[2, 1].text(-1.55, 0.22, r"$-\Omega_M T$", color=GRAY, fontsize=7, ha="right")
    ax[2, 1].set(xlabel=r"$\omega$", ylabel=r"$X(\mathrm{e}^{\mathrm{j}\omega})$",
                 title="DTFT, one period shaded")
    save(fig, "three-relations.pdf")


def bandlimited_shapes():
    fig, ax = plt.subplots(1, 2, figsize=(8.8, 3.15), constrained_layout=True)
    w = np.linspace(-8, 8, 1801)
    style(ax[0], (-8, 8), (-0.08, 1.4))
    ax[0].plot(w, hump(w, 0, 2.4, 1), color=BLUE, lw=1.6)
    ax[0].axvline(-2.4, color=GRAY, ls="--", lw=0.7)
    ax[0].axvline(2.4, color=GRAY, ls="--", lw=0.7)
    ax[0].text(-2.4, 1.16, r"$-\Omega_M$", ha="center", fontsize=8)
    ax[0].text(2.4, 1.16, r"$\Omega_M$", ha="center", fontsize=8)
    ax[0].set(xlabel=r"$\Omega$", ylabel=r"$X(\mathrm{j}\Omega)$",
              title="Support fills the band")

    style(ax[1], (-8, 8), (-0.08, 1.4))
    center, half = 4.0, 1.15
    outer = center + half
    spec = hump(w, center, half, 1) + hump(w, -center, half, 1)
    ax[1].plot(w, spec, color=BLUE, lw=1.6)
    ax[1].axvline(outer, color=GRAY, ls="--", lw=0.7)
    ax[1].axvline(-outer, color=GRAY, ls="--", lw=0.7)
    ax[1].text(outer, 1.16, r"$\Omega_M$", ha="center", fontsize=8)
    ax[1].text(-outer, 1.16, r"$-\Omega_M$", ha="center", fontsize=8)
    ax[1].text(center, 1.08, r"$\Omega_c$", color=GREEN, ha="center", fontsize=8)
    ax[1].text(-center, 1.08, r"$-\Omega_c$", color=GREEN, ha="center", fontsize=8)
    ax[1].set(xlabel=r"$\Omega$", title="Two lobes, same outer edge")
    save(fig, "bandlimited-or.pdf")


def aliasing():
    fig, ax = plt.subplots(3, 1, figsize=(8.4, 7.6), constrained_layout=True)
    w = np.linspace(-7.5, 7.5, 2001)
    cases = [
        (3.6, 1.3, 0.55, None, r"$\Omega_s>2\Omega_M$: replicas separate"),
        (1.7, 1.3, 0.55, None, r"$\Omega_s<2\Omega_M$: full band overlaps"),
        (1.7, 0.35, 0.55, 1.15, r"nominal $\Omega_M$ too wide; actual support separates"),
    ]
    for a, (ws, half, height, nominal, title) in zip(ax, cases):
        style(a, (-7.5, 7.5), (-0.08, 1.25))
        parts = [hump(w, k * ws, half, height) for k in range(-3, 4)]
        total = np.sum(parts, axis=0)
        for part in parts:
            a.plot(w, part, color=GRAY, lw=0.9)
        a.plot(w, total, color=RED, lw=1.5)
        if nominal is not None:
            a.axvline(nominal, color=GREEN, ls="--", lw=0.9)
            a.axvline(-nominal, color=GREEN, ls="--", lw=0.9)
            a.text(nominal, 1.08, r"nominal $\Omega_M$", color=GREEN,
                   ha="left", fontsize=8)
        a.set(xlabel=r"$\Omega$", ylabel=r"$X_p$", title=title, ylim=(-0.08, 1.25))
        a.text(0.02, 0.86, "gray: replicas, red: sum", transform=a.transAxes,
               fontsize=8, color=GRAY)
    save(fig, "aliasing.pdf")


def reconstruction():
    fig, ax = plt.subplots(2, 1, figsize=(8.4, 5.6), constrained_layout=True)
    w = np.linspace(-9, 9, 2001)
    # Replica height 1/T = 0.5, gain T = 2, product restores height 1.
    ws, half = 4.2, 1.2
    style(ax[0], (-9, 9), (-0.15, 2.45))
    spec = sum(hump(w, k * ws, half, 0.5) for k in range(-2, 3))
    ax[0].plot(w, spec, color=BLUE, lw=1.4, label=r"$X_p$, height $1/T$")
    filt = np.where(np.abs(w) < 1.9, 2.0, 0.0)
    ax[0].plot(w, filt, color=GREEN, lw=1.5, label=r"$H$, gain $T$")
    ax[0].axvline(1.2, color=GRAY, ls="--", lw=0.6)
    ax[0].axvline(ws - 1.2, color=GRAY, ls="--", lw=0.6)
    ax[0].text(1.2, 1.38, r"$\Omega_M$", ha="center", fontsize=8)
    ax[0].text(1.9, 2.08, r"$\Omega_0$", color=GREEN, fontsize=8)
    ax[0].text(ws - 1.2, 1.55, r"$\Omega_s-\Omega_M$", ha="center", fontsize=8)
    ax[0].set(xlabel=r"$\Omega$", ylabel="spectrum", title="Lowpass recovery")
    ax[0].legend(frameon=False, fontsize=8, loc="upper right")

    style(ax[1], (-9, 9), (-0.1, 1.35))
    recovered = hump(w, 0, half, 1.0)
    ax[1].plot(w, recovered, color=RED, lw=1.6)
    ax[1].set(xlabel=r"$\Omega$", ylabel=r"$X(\mathrm{j}\Omega)$",
              title="Baseband copy restored")
    save(fig, "reconstruction.pdf")


def interpolation():
    fig, ax = plt.subplots(figsize=(8.6, 3.6), constrained_layout=True)
    n = np.arange(-4, 5)
    samples = np.array([0.05, -0.15, 0.45, 1.0, 0.55, -0.25, 0.2, -0.08, 0.03])
    t = np.linspace(-4.6, 4.6, 1401)
    style(ax, (-4.6, 4.6), (-0.55, 1.35))
    total = np.zeros_like(t)
    for ni, yi in zip(n, samples):
        term = yi * np.sinc(t - ni)
        total += term
        ax.plot(t, term, color="#b7c9d8", lw=0.8)
    ax.plot(t, total, color=BLUE, lw=1.7)
    ax.plot(n, samples, "o", color=RED, ms=4.5, zorder=4)
    ax.set(xlabel="$t/T$", ylabel="$x(t)$",
           title=r"Cardinal series, $\Omega_0=\pi/T$")
    save(fig, "interpolation.pdf")


def bandpass_recovery():
    fig, ax = plt.subplots(2, 1, figsize=(8.4, 5.6), constrained_layout=True)
    w = np.linspace(-10, 10, 2201)
    ws, half = 4.4, 1.15
    style(ax[0], (-10, 10), (-0.08, 1.45))
    # 1/T = 0.5, gain T/2 = 1, product is E/2 = 0.5 if E = 1.
    spec = sum(hump(w, k * ws, half, 0.5) for k in range(-2, 3))
    ax[0].plot(w, spec, color=BLUE, lw=1.3)
    gate = ((np.abs(w - ws) < 1.7) | (np.abs(w + ws) < 1.7)).astype(float) * 1.0
    ax[0].plot(w, gate, color=GREEN, lw=1.4)
    ax[0].text(ws, 1.08, r"gain $T/2$", color=GREEN, ha="center", fontsize=8)
    ax[0].text(0, 0.58, r"$1/T$", color=RED, ha="center", fontsize=8)
    ax[0].set(xlabel=r"$\Omega$", title=r"Keep the replicas at $\pm\Omega_s$",
              ylim=(-0.08, 1.35))

    style(ax[1], (-10, 10), (-0.08, 0.85))
    out = hump(w, ws, half, 0.5) + hump(w, -ws, half, 0.5)
    ax[1].plot(w, out, color=RED, lw=1.6)
    ax[1].text(ws, 0.58, r"$E/2$", color=RED, ha="center", fontsize=8)
    ax[1].set(xlabel=r"$\Omega$", ylabel="output",
              title=r"Spectrum of $x(t)\cos(\Omega_s t)$")
    save(fig, "bandpass-recovery.pdf")


def ideal_filters():
    fig, ax = plt.subplots(2, 2, figsize=(8.8, 5.8), constrained_layout=True)
    w = np.linspace(-8, 8, 1601)
    w0, ws = 1.6, 4.2

    def rect_band(center):
        return np.where(np.abs(w - center) < w0, 1.0, 0.0)

    panels = [
        (ax[0, 0], np.where(np.abs(w) < w0, 1.0, 0.0), "Lowpass"),
        (ax[0, 1], np.where(np.abs(w) < w0, 0.0, 1.0), "Highpass"),
        (ax[1, 0], rect_band(ws) + rect_band(-ws), "Bandpass"),
        (ax[1, 1], 1 - (rect_band(ws) + rect_band(-ws)), "Bandstop"),
    ]
    for a, y, title in panels:
        style(a, (-8, 8), (-0.15, 1.35))
        a.plot(w, y, color=BLUE, lw=1.5)
        a.set(xlabel=r"$\Omega$", ylabel="$H$", title=title, ylim=(-0.15, 1.55))
    ax[0, 0].text(w0, 1.08, r"$\Omega_0$", fontsize=8, ha="left")
    ax[0, 0].text(-w0, 1.08, r"$-\Omega_0$", fontsize=8, ha="right")
    ax[0, 1].text(w0, 1.08, r"$\Omega_0$", fontsize=8, ha="left")
    ax[0, 1].text(-w0, 1.08, r"$-\Omega_0$", fontsize=8, ha="right")
    ax[1, 0].text(ws - w0, 1.08, r"$\Omega_s-\Omega_0$", fontsize=7, ha="right")
    ax[1, 0].text(ws, 1.28, r"$\Omega_s$", fontsize=8, ha="center")
    ax[1, 0].text(ws + w0, 1.08, r"$\Omega_s+\Omega_0$", fontsize=7, ha="left")
    ax[1, 1].text(ws - w0, 1.08, r"$\Omega_s-\Omega_0$", fontsize=7, ha="right")
    ax[1, 1].text(ws + w0, 1.08, r"$\Omega_s+\Omega_0$", fontsize=7, ha="left")
    save(fig, "ideal-filters.pdf")


def nyquist_lines():
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.5), constrained_layout=True)
    for a, ylim in zip(ax, [(-2, 15), (-5, 5)]):
        style(a, (-3800 * np.pi, 3800 * np.pi), ylim)
        a.set_xticks([-3000 * np.pi, -1000 * np.pi, 0, 1000 * np.pi, 3000 * np.pi])
        a.set_xticklabels(
            [r"$-3000\pi$", r"$-1000\pi$", "$0$", r"$1000\pi$", r"$3000\pi$"]
        )
    # Real weights: DC 4pi, cosine pi, sine 0
    impulse(ax[0], 0, 4 * np.pi, r"$4\pi$", dx=220, dy=0.15)
    impulse(ax[0], 1000 * np.pi, np.pi, r"$\pi$", dx=220, dy=0.15)
    impulse(ax[0], -1000 * np.pi, np.pi, r"$\pi$", dx=220, dy=0.15)
    ax[0].set(ylabel="real weight", title="Real part")
    # Imag weights: sine at +3000pi is -pi, at -3000pi is +pi
    impulse(ax[1], 3000 * np.pi, -np.pi, r"$-\pi$", dx=280, dy=0.15)
    impulse(ax[1], -3000 * np.pi, np.pi, r"$\pi$", dx=280, dy=0.15)
    ax[1].set(ylabel="imaginary weight", title="Imaginary part")
    ax[1].axvline(3000 * np.pi, color=GRAY, ls="--", lw=0.6)
    ax[1].axvline(-3000 * np.pi, color=GRAY, ls="--", lw=0.6)
    save(fig, "nyquist-lines.pdf")


def sinc_square():
    t = np.linspace(-8, 8, 1601)
    wc = 1.5
    xt = (wc / np.pi) ** 2 * np.sinc(wc * t / np.pi) ** 2
    fig, ax = plt.subplots(figsize=(7.2, 3.2), constrained_layout=True)
    style(ax, (-8, 8), (-0.02, 0.28))
    ax.plot(t, xt, color=BLUE, lw=1.5)
    ax.set(xlabel="$t$", ylabel="$x(t)$",
           title=r"$(\sin\Omega_c t/(\pi t))^2$")
    save(fig, "sinc-square-time.pdf")

    w = np.linspace(-4.5, 4.5, 1201)
    rect = np.where(np.abs(w) < wc, 1.0, 0.0)
    tri = np.maximum(2 * wc - np.abs(w), 0) / (2 * np.pi)
    fig, ax = plt.subplots(1, 2, figsize=(9.0, 3.3), constrained_layout=True)
    style(ax[0], (-4.5, 4.5), (-0.08, 1.25))
    ax[0].plot(w, rect, color=BLUE, lw=1.5)
    ax[0].axvline(wc, color=GRAY, ls="--", lw=0.7)
    ax[0].axvline(-wc, color=GRAY, ls="--", lw=0.7)
    ax[0].text(wc, 1.08, r"$\Omega_c$", ha="center", fontsize=8)
    ax[0].set(xlabel=r"$\Omega$", ylabel="spectrum",
              title=r"Factor $\sin(\Omega_c t)/(\pi t)$")
    style(ax[1], (-4.5, 4.5), (-0.02, 0.62))
    ax[1].plot(w, tri, color=RED, lw=1.5)
    ax[1].axvline(2 * wc, color=GRAY, ls="--", lw=0.7)
    ax[1].axvline(-2 * wc, color=GRAY, ls="--", lw=0.7)
    ax[1].text(2 * wc, 0.08, r"$2\Omega_c$", ha="center", fontsize=8)
    peak = wc / np.pi
    ax[1].text(0.15, peak + 0.03, r"$\Omega_c/\pi$", ha="left",
               color=RED, fontsize=8)
    ax[1].set(xlabel=r"$\Omega$", ylabel=r"$X(\mathrm{j}\Omega)$",
              title="Square, triangular spectrum")
    save(fig, "sinc-square-spectrum.pdf")


if __name__ == "__main__":
    three_relations()
    bandlimited_shapes()
    aliasing()
    reconstruction()
    interpolation()
    bandpass_recovery()
    ideal_filters()
    nyquist_lines()
    sinc_square()
    print("wrote", len(list(OUT.glob('*.pdf'))), "pdfs")
