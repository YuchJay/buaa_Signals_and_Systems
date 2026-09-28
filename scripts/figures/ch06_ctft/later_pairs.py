"""Figures for CTFT scaling, duality, ideal filtering, and periodic spectra."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
BASIC = ROOT / "figures" / "06-ctft" / "basic"
EXAMPLES = ROOT / "figures" / "06-ctft" / "examples"
BLUE, RED, GRAY = "#25669b", "#b23a2b", "#666666"


def axes_grid(rows, cols, size):
    fig, axes = plt.subplots(rows, cols, figsize=size, constrained_layout=True)
    for ax in np.asarray(axes).flat:
        ax.axhline(0, color="#303030", lw=0.6, zorder=0)
        ax.axvline(0, color="#303030", lw=0.6, zorder=0)
        ax.grid(color="#dddddd", lw=0.45)
        ax.spines[["top", "right"]].set_visible(False)
    arr = np.asarray(axes)
    if arr.shape == ():
        return fig, arr.item()
    return fig, arr


def save(fig, directory, name):
    directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        directory / f"{name}.pdf",
        bbox_inches="tight",
        metadata={"CreationDate": None, "ModDate": None},
    )
    plt.close(fig)
    print(directory / f"{name}.pdf")


def impulse(ax, position, weight, text, dx=0.18, color=RED):
    ax.annotate(
        "",
        (position, weight),
        (position, 0),
        arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.45},
    )
    ax.text(position + dx, weight, text, va="center", color=color, fontsize=8)


def si(z):
    """Sine integral Si(z), vectorized for moderate real arguments."""
    z = np.asarray(z, dtype=float)
    out = np.empty(z.shape)
    for index, value in np.ndenumerate(z):
        upper = abs(value)
        if upper < 1e-8:
            out[index] = 0.0
            continue
        grid = np.linspace(0.0, upper, 6000)
        integrand = np.ones_like(grid)
        integrand[1:] = np.sin(grid[1:]) / grid[1:]
        area = np.trapezoid(integrand, grid)
        out[index] = np.copysign(area, value)
    return out


def verify():
    tau, height = 2.0, 1.0
    omega = np.array([0.4, 1.1, 2.5, 4.0])
    t = np.linspace(-tau / 2, tau / 2, 40001)
    signal = height * np.cos(np.pi * t / tau)
    numerical = np.trapezoid(signal[:, None] * np.exp(-1j * omega * t[:, None]), t, axis=0)
    closed = (2 * np.pi * height * tau * np.cos(omega * tau / 2)) / (np.pi**2 - (omega * tau) ** 2)
    if np.max(np.abs(numerical - closed)) > 2e-3:
        raise SystemExit("half-cosine mismatch")

    big_t, ramp_e = 1.0, 1.0
    ramp_w = np.array([0.7, 1.4, 2.2, 3.5])
    ramp_t = np.linspace(-big_t, big_t, 40001)
    ramp = (ramp_e / big_t) * ramp_t
    ramp_num = np.trapezoid(ramp[:, None] * np.exp(-1j * ramp_w * ramp_t[:, None]), ramp_t, axis=0)
    bracket = np.sin(ramp_w * big_t) / ramp_w**2 - big_t * np.cos(ramp_w * big_t) / ramp_w
    ramp_closed = -1j * (2 * ramp_e / big_t) * bracket
    if np.max(np.abs(ramp_num - ramp_closed)) > 2e-3:
        raise SystemExit("odd-ramp mismatch")

    gauss_w = np.linspace(-2, 2, 9)
    gauss_t = np.linspace(-12, 12, 60001)
    gauss = np.exp(-(gauss_t**2))
    gauss_num = np.trapezoid(gauss[:, None] * np.exp(-1j * gauss_w * gauss_t[:, None]), gauss_t, axis=0)
    gauss_closed = np.sqrt(np.pi) * np.exp(-(gauss_w / 2) ** 2)
    if np.max(np.abs(gauss_num - gauss_closed)) > 2e-3:
        raise SystemExit("gaussian mismatch")

    grid = np.linspace(0, 40, 20000)
    energy = np.trapezoid((np.exp(-grid) - np.exp(-2 * grid)) ** 2, grid)
    if abs(energy - 1 / 12) > 1e-4:
        raise SystemExit("energy integral mismatch")
    peak = 0.5 + float(si(np.pi) / np.pi)
    lobe = 2 * float(si(np.pi) / np.pi)
    print("step peak %.4f, overshoot %.4f, main lobe %.4f" % (peak, peak - 1, lobe))


def scaling():
    fig, ax = axes_grid(2, 2, (7.8, 4.6))
    ax[0, 0].plot([-1.6, -1, -1, 1, 1, 1.6], [0, 0, 1, 1, 0, 0], color=BLUE)
    ax[0, 0].set(xlabel=r"$t$", ylabel=r"$x(t)$", title=r"$x(t)$", xlim=(-2.2, 2.2), ylim=(-0.15, 1.35))
    ax[0, 1].plot([-1.2, -0.5, -0.5, 0.5, 0.5, 1.2], [0, 0, 1, 1, 0, 0], color=BLUE)
    ax[0, 1].set(xlabel=r"$t$", ylabel=r"$x(2t)$", title=r"$x(2t)$", xlim=(-2.2, 2.2), ylim=(-0.15, 1.35))
    w = np.linspace(-14, 14, 4001)
    sa = np.ones_like(w)
    nz = np.abs(w) > 1e-8
    sa[nz] = np.sin(w[nz]) / w[nz]
    ax[1, 0].plot(w, 2 * sa, color=BLUE)
    ax[1, 0].set(xlabel=r"$\omega$", ylabel=r"$X(\mathrm{j}\omega)$", title="Original spectrum", ylim=(-0.55, 2.25))
    sa2 = np.ones_like(w)
    sa2[nz] = np.sin(w[nz] / 2) / (w[nz] / 2)
    ax[1, 1].plot(w, sa2, color=BLUE)
    ax[1, 1].set(xlabel=r"$\omega$", ylabel=r"$X(\mathrm{j}\omega/2)/2$", title="Compressed in time", ylim=(-0.55, 2.25))
    save(fig, BASIC, "scaling-rectangles")


def duality():
    fig, ax = axes_grid(2, 2, (7.8, 4.6))
    ax[0, 0].plot([-1.8, -1, -1, 1, 1, 1.8], [0, 0, 1, 1, 0, 0], color=BLUE)
    ax[0, 0].set(xlabel=r"$t$", ylabel=r"$x(t)$", title="Rectangle, height 1", xlim=(-6, 6), ylim=(-0.2, 1.4))
    w = np.linspace(-12, 12, 4001)
    sinc = np.ones_like(w)
    nz = np.abs(w) > 1e-6
    sinc[nz] = 2 * np.sin(w[nz]) / w[nz]
    ax[0, 1].plot(w, sinc, color=BLUE)
    ax[0, 1].set(xlabel=r"$\omega$", ylabel=r"$X(\mathrm{j}\omega)$", title=r"$2\sin\omega/\omega$", xlim=(-12, 12))
    t = np.linspace(-12, 12, 4001)
    nzt = np.abs(t) > 1e-6
    xt = np.empty_like(t)
    xt[nzt] = 2 * np.sin(t[nzt]) / t[nzt]
    xt[~nzt] = 2
    ax[1, 0].plot(t, xt, color=BLUE)
    ax[1, 0].set(xlabel=r"$t$", ylabel=r"$X(t)$", title="Swapped into time", xlim=(-12, 12))
    ax[1, 1].plot([-6, -1, -1, 1, 1, 6], [0, 0, 2 * np.pi, 2 * np.pi, 0, 0], color=BLUE)
    ax[1, 1].set(
        xlabel=r"$\omega$",
        ylabel=r"$2\pi x(-\omega)$",
        title=r"Height $2\pi$",
        xlim=(-6, 6),
        ylim=(-0.4, 7.2),
        yticks=[0, 2 * np.pi],
        yticklabels=["0", r"$2\pi$"],
    )
    save(fig, BASIC, "duality-rectangle")


def two_sided_and_rational():
    fig, ax = axes_grid(2, 2, (7.8, 4.6))
    t = np.linspace(-4, 4, 1201)
    w = np.linspace(-6, 6, 1201)
    ax[0, 0].plot(t, np.exp(-np.abs(t)), color=BLUE)
    ax[0, 0].set(xlabel=r"$t$", ylabel=r"$e^{-|t|}$", title="Two-sided exponential")
    ax[0, 1].plot(w, 2 / (1 + w**2), color=BLUE)
    ax[0, 1].set(xlabel=r"$\omega$", ylabel=r"$X(\mathrm{j}\omega)$", title=r"$2/(1+\omega^2)$")
    ax[1, 0].plot(t, 1 / (1 + t**2), color=BLUE, label=r"$\Re$")
    ax[1, 0].plot(t, -t / (1 + t**2), color=RED, label=r"$\Im$")
    ax[1, 0].legend(frameon=False, fontsize=8)
    ax[1, 0].set(xlabel=r"$t$", title=r"$1/(1+\mathrm{j}t)$")
    spectrum = np.where(w < 0, 2 * np.pi * np.exp(w), 0.0)
    ax[1, 1].plot(w, spectrum, color=BLUE)
    ax[1, 1].set(xlabel=r"$\omega$", ylabel=r"$2\pi e^{\omega}u(-\omega)$", title="One-sided spectrum", ylim=(-0.4, 7))
    save(fig, BASIC, "dual-rational")

    fig, ax = axes_grid(1, 2, (7.4, 2.7))
    ax[0].plot(t, 1 / (1 + t**2), color=BLUE)
    ax[0].set(xlabel=r"$t$", ylabel=r"$1/(1+t^2)$", title="Even rational signal")
    ax[1].plot(w, np.pi * np.exp(-np.abs(w)), color=BLUE)
    ax[1].set(xlabel=r"$\omega$", ylabel=r"$\pi e^{-|\omega|}$", title="Real even spectrum")
    save(fig, BASIC, "lorentz-spectrum")


def hilbert():
    fig, ax = axes_grid(1, 3, (9.2, 2.8))
    t = np.linspace(-8, 8, 2001)
    mask = np.abs(t) > 0.08
    ax[0].plot(t[mask], 1 / (np.pi * t[mask]), color=BLUE)
    ax[0].set(xlabel=r"$t$", ylabel=r"$1/(\pi t)$", title="Hilbert kernel", xlim=(-8, 8), ylim=(-2.2, 2.2))
    ax[1].plot([-4, -0.05], [1, 1], color=BLUE)
    ax[1].plot([0.05, 4], [-1, -1], color=BLUE)
    ax[1].set(xlabel=r"$\omega$", ylabel=r"$\Im X$", title=r"$-\mathrm{sgn}(\omega)$", xlim=(-4, 4), ylim=(-1.4, 1.4))
    ax[2].plot([-4, -0.05], [np.pi / 2, np.pi / 2], color=BLUE)
    ax[2].plot([0.05, 4], [-np.pi / 2, -np.pi / 2], color=BLUE)
    ax[2].set(
        xlabel=r"$\omega$",
        ylabel=r"$\theta(\omega)$",
        title="Phase undefined at 0",
        xlim=(-4, 4),
        ylim=(-2, 2),
        yticks=[-np.pi / 2, 0, np.pi / 2],
        yticklabels=[r"$-\pi/2$", "0", r"$\pi/2$"],
    )
    save(fig, BASIC, "hilbert-spectrum")


def sinc_energy():
    fig, ax = axes_grid(1, 3, (9.2, 2.7))
    t = np.linspace(-18, 18, 4001)
    y = np.ones_like(t)
    nz = np.abs(t) > 1e-8
    y[nz] = np.sin(t[nz]) / t[nz]
    ax[0].plot(t, y, color=BLUE)
    ax[0].set(xlabel=r"$t$", ylabel=r"$\sin t/t$", title="Time signal", xlim=(-18, 18))
    ax[1].plot([-3, -1, -1, 1, 1, 3], [0, 0, np.pi, np.pi, 0, 0], color=BLUE)
    ax[1].set(
        xlabel=r"$\omega$",
        ylabel=r"$X(\mathrm{j}\omega)$",
        title=r"Height $\pi$",
        xlim=(-3, 3),
        ylim=(-0.3, 3.8),
        yticks=[0, np.pi],
        yticklabels=["0", r"$\pi$"],
    )
    w = np.linspace(-3, 3, 601)
    tri = np.maximum(np.pi * (1 - np.abs(w) / 2), 0)
    ax[2].plot(w, tri, color=BLUE)
    ax[2].plot(0, np.pi, "o", color=RED, ms=4)
    ax[2].set(xlabel=r"$\omega$", ylabel=r"$Y(\mathrm{j}\omega)$", title=r"Spectrum of $(\sin t/t)^2$", xlim=(-3, 3))
    save(fig, BASIC, "sinc-energy")


def causal_even():
    fig, ax = axes_grid(1, 2, (7.4, 2.7))
    t = np.linspace(-4, 4, 1001)
    ax[0].plot(t, 0.5 * np.exp(-np.abs(t)), color=BLUE)
    ax[0].set(xlabel=r"$t$", ylabel=r"$(x(t)+x(-t))/2$", title="Even part")
    ax[1].plot([-4, 0, 0], [0, 0, 1], color=BLUE)
    tp = t[t >= 0]
    ax[1].plot(tp, np.exp(-tp), color=BLUE)
    ax[1].set(xlabel=r"$t$", ylabel=r"$x(t)$", title=r"$e^{-t}u(t)$")
    save(fig, BASIC, "causal-from-real")


def ideal_lowpass():
    fig, ax = axes_grid(2, 2, (7.8, 4.6))
    t = np.linspace(-8, 8, 2001)
    nz = np.abs(t) > 1e-8
    h = np.empty_like(t)
    h[nz] = np.sin(t[nz]) / (np.pi * t[nz])
    h[~nz] = 1 / np.pi
    ax[0, 0].plot(t, h, color=BLUE)
    ax[0, 0].plot(0, 1 / np.pi, "o", color=RED, ms=3.5)
    ax[0, 0].set(xlabel=r"$\omega_c t$", ylabel=r"$h(t)$", title=r"Impulse response, $\omega_c=1$", ylim=(-0.15, 0.42))
    ax[0, 1].plot([-2.2, -1, -1, 1, 1, 2.2], [0, 0, 1, 1, 0, 0], color=BLUE)
    ax[0, 1].set(xlabel=r"$\omega/\omega_c$", ylabel=r"$|H|$", title="Magnitude", xlim=(-2.2, 2.2), ylim=(-0.1, 1.3))
    td = t - 1.5
    hd = np.ones_like(td)
    nzd = np.abs(td) > 1e-8
    hd[nzd] = np.sin(td[nzd]) / (np.pi * td[nzd])
    ax[1, 0].plot(t, hd, color=BLUE)
    ax[1, 0].axvline(1.5, color=GRAY, ls="--", lw=0.8)
    ax[1, 0].set(xlabel=r"$\omega_c t$", ylabel=r"$h(t-t_0)$", title=r"Delay $t_0=1.5/\omega_c$")
    phase_w = np.linspace(-1, 1, 200)
    ax[1, 1].plot(phase_w, -1.5 * phase_w, color=BLUE)
    ax[1, 1].set(xlabel=r"$\omega/\omega_c$", ylabel=r"$\theta(\omega)$", title=r"Phase inside the passband", xlim=(-1.35, 1.35))
    save(fig, BASIC, "ideal-lowpass")

    fig, ax = axes_grid(1, 2, (8.0, 3.1))
    lobe_t = np.linspace(-2.5 * np.pi, 2.5 * np.pi, 1801)
    nz = np.abs(lobe_t) > 1e-8
    kernel = np.empty_like(lobe_t)
    kernel[nz] = np.sin(lobe_t[nz]) / (np.pi * lobe_t[nz])
    kernel[~nz] = 1 / np.pi
    ax[0].plot(lobe_t, kernel, color=BLUE)
    main = np.abs(lobe_t) <= np.pi
    side = (np.abs(lobe_t) >= np.pi) & (np.abs(lobe_t) <= 2 * np.pi)
    ax[0].fill_between(lobe_t, 0, kernel, where=main, color=RED, alpha=0.28, interpolate=True)
    ax[0].fill_between(lobe_t, 0, kernel, where=side, color=BLUE, alpha=0.22, interpolate=True)
    ax[0].text(0, 0.20, r"$1.18$", ha="center", va="center", color=RED, fontsize=8)
    ax[0].text(1.5 * np.pi, -0.012, r"$0.14$", ha="center", va="top", color=BLUE, fontsize=8)
    ax[0].set(
        xlabel=r"$\omega_c t$",
        ylabel=r"$h(t)$",
        title="Main lobe and first sidelobes",
        xticks=[-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi],
        xticklabels=[r"$-2\pi$", r"$-\pi$", "0", r"$\pi$", r"$2\pi$"],
        xlim=(-8, 8),
    )
    step_t = np.linspace(-4 * np.pi, 4 * np.pi, 901)
    step_y = 0.5 + si(step_t) / np.pi
    ax[1].plot(step_t, step_y, color=BLUE)
    ax[1].axhline(1, color=GRAY, ls="--", lw=0.7)
    ax[1].axhline(0.5, color=GRAY, ls=":", lw=0.7)
    peak_t = np.pi
    peak_y = 0.5 + float(si(peak_t) / np.pi)
    ax[1].plot(peak_t, peak_y, "o", color=RED, ms=4)
    ax[1].text(peak_t + 0.45, peak_y + 0.015, r"$1.09$", color=RED, fontsize=8, va="bottom")
    ax[1].set(
        xlabel=r"$\omega_c t$",
        ylabel=r"$y(t)$",
        title="Step response",
        xticks=[-2 * np.pi, 0, np.pi, 2 * np.pi],
        xticklabels=[r"$-2\pi$", "0", r"$\pi$", r"$2\pi$"],
        yticks=[0, 0.5, 1],
        ylim=(-0.18, 1.25),
    )
    save(fig, BASIC, "ideal-lowpass-step")


def extra_pairs():
    fig, ax = axes_grid(1, 2, (7.4, 2.7))
    t = np.linspace(-3.2, 3.2, 801)
    w = np.linspace(-6, 6, 801)
    ax[0].plot(t, np.exp(-(t**2)), color=BLUE)
    ax[0].set(xlabel=r"$t/\tau$", ylabel=r"$x(t)/E$", title=r"$e^{-(t/\tau)^2}$")
    ax[1].plot(w, np.exp(-(w / 2) ** 2), color=BLUE)
    ax[1].set(xlabel=r"$\omega\tau$", ylabel=r"$X/(E\tau\sqrt{\pi})$", title="Gaussian spectrum")
    save(fig, BASIC, "gaussian-spectrum")

    fig, ax = axes_grid(1, 3, (9.3, 2.8))
    tau = 2.0
    tt = np.linspace(-2.2, 2.2, 801)
    pulse = np.where(np.abs(tt) < tau / 2, np.cos(np.pi * tt / tau), 0.0)
    ax[0].plot(tt, pulse, color=BLUE)
    ax[0].set(xlabel=r"$t$", ylabel=r"$x(t)/E$", title=r"Half-cosine, $\tau=2$", ylim=(-0.15, 1.2))
    ww = np.linspace(-8, 8, 4001)
    den = np.pi**2 - (ww * tau) ** 2
    closed = np.empty_like(ww)
    near = np.abs(den) < 1e-2
    closed[near] = tau / 2
    closed[~near] = 2 * np.pi * tau * np.cos(ww[~near] * tau / 2) / den[~near]
    ax[1].plot(ww, closed, color=BLUE)
    ax[1].plot([np.pi / tau, -np.pi / tau], [tau / 2, tau / 2], "o", color=RED, ms=4)
    ax[1].set(xlabel=r"$\omega$", ylabel=r"$X/E$", title="Signed spectrum")
    phase = np.where(closed > 0, 0.0, np.pi)
    phase[np.abs(closed) < 1e-2] = np.nan
    ax[2].plot(ww, phase, color=BLUE)
    ax[2].set(
        xlabel=r"$\omega$",
        ylabel=r"$\theta(\omega)$",
        title="Phase at zeros excluded",
        yticks=[0, np.pi],
        yticklabels=["0", r"$\pi$"],
        ylim=(-0.4, 3.6),
    )
    save(fig, BASIC, "half-cosine-spectrum")

    fig, ax = axes_grid(1, 3, (9.3, 2.8))
    big_t = 1.0
    rt = np.linspace(-1.8, 1.8, 801)
    ramp = np.where(np.abs(rt) < big_t, rt / big_t, 0.0)
    ax[0].plot(rt, ramp, color=BLUE)
    ax[0].set(xlabel=r"$t/T$", ylabel=r"$x(t)/E$", title="Odd finite ramp", ylim=(-1.3, 1.3))
    rw = np.linspace(-18, 18, 4001)
    imag = np.zeros_like(rw)
    nz = np.abs(rw) > 1e-3
    bracket = np.sin(rw[nz] * big_t) / rw[nz] ** 2 - big_t * np.cos(rw[nz] * big_t) / rw[nz]
    imag[nz] = np.imag(-1j * (2 / big_t) * bracket)
    ax[1].plot(rw, imag, color=RED)
    ax[1].set(xlabel=r"$\omega T$", ylabel=r"$\Im(X)/E$", title="Imaginary spectrum")
    ph = np.full_like(rw, np.nan)
    ph[imag < -0.02] = -np.pi / 2
    ph[imag > 0.02] = np.pi / 2
    ax[2].plot(rw, ph, color=BLUE, lw=1.0)
    ax[2].set(
        xlabel=r"$\omega T$",
        ylabel=r"$\theta(\omega)$",
        title="Phase undefined at zeros",
        yticks=[-np.pi / 2, np.pi / 2],
        yticklabels=[r"$-\pi/2$", r"$\pi/2$"],
        ylim=(-2, 2),
    )
    save(fig, BASIC, "odd-ramp-spectrum")


def periodic():
    fig, ax = axes_grid(1, 2, (7.8, 2.9))
    t = np.linspace(-8, 8, 4001)
    local = np.abs((t + 2) % 4 - 2)
    wave = np.where(local < 1, 1.0, 0.0)
    ax[0].plot(t, wave, color=BLUE)
    ax[0].set(xlabel=r"$t$", ylabel=r"$x(t)$", title=r"$T_0=4,\ T_1=1$", ylim=(-0.15, 1.35), xlim=(-8, 8))
    ax[1].set(xlim=(-6.4, 6.4), ylim=(-1.2, 3.6), xlabel=r"$\omega$", title=r"Impulse weights $2\pi A_k$")
    pairs = [(0, np.pi), (1, 2.0), (2, 0.0), (3, -2.0 / 3), (4, 0.0), (5, 0.4)]
    for k, weight in pairs:
        signs = (0,) if k == 0 else (1, -1)
        for sign in signs:
            pos = sign * k * np.pi / 2
            if abs(weight) < 1e-9:
                ax[1].plot([pos], [0], "o", color=GRAY, ms=3.5)
            else:
                label = r"$\pi$" if k == 0 else format(weight, ".3g")
                dx = 0.16 if pos >= 0 else -0.72
                impulse(ax[1], pos, weight, label, dx=dx)
    save(fig, BASIC, "periodic-rectangle-spectrum")

    fig, ax = axes_grid(1, 2, (7.6, 2.8))
    ax[0].set(xlim=(-3.5, 3.5), ylim=(-0.1, 1.45), xlabel=r"$t$", title=r"$\sum_k\delta(t-kT_0)$")
    ax[1].set(xlim=(-3.5, 3.5), ylim=(-0.1, 1.55), xlabel=r"$\omega/\omega_0$", title="Equal impulse weights")
    for k in range(-3, 4):
        impulse(ax[0], k, 1.0, r"$1$" if k == 0 else "", dx=0.12)
        impulse(ax[1], k, 1.15, r"$2\pi/T_0$" if k == 0 else "", dx=0.12)
    save(fig, BASIC, "impulse-train-spectrum")


def examples():
    fig, ax = axes_grid(1, 1, (6.4, 2.6))
    t = np.linspace(-1, 6, 1201)
    x = np.zeros_like(t)
    live = t >= 0
    x[live] = 2 * np.sqrt(3) * (np.exp(-t[live]) - np.exp(-2 * t[live]))
    ax.plot(t, x, color=BLUE)
    ax.set(xlabel=r"$t$", ylabel=r"$x(t)$", xlim=(-1, 6))
    save(fig, EXAMPLES, "parseval-normalized-answer")

    fig, ax = axes_grid(1, 1, (6.6, 2.6))
    t = np.linspace(-2.15, 2.15, 2001)
    folded = (t + 0.5) % 1 - 0.5
    tri = 1 - 2 * np.abs(folded)
    ax.plot(t, tri, color=BLUE)
    ax.set(xlabel=r"$t/T$", ylabel=r"$x(t)/E$", ylim=(-0.1, 1.25))
    save(fig, EXAMPLES, "triangle-fs-given")

    fig, ax = axes_grid(1, 1, (6.6, 2.7))
    ks = np.arange(-7, 8)
    coeff = np.zeros_like(ks, dtype=float)
    zero = ks == 0
    coeff[zero] = 0.5
    coeff[~zero] = 2 * np.sin(ks[~zero] * np.pi / 2) ** 2 / (np.pi**2 * ks[~zero] ** 2)
    ax.vlines(ks, 0, coeff, color=BLUE, lw=1.3)
    ax.plot(ks, coeff, "o", color=BLUE, ms=4)
    ax.set(xlabel=r"$k$", ylabel=r"$A_k/E$", xticks=ks)
    save(fig, EXAMPLES, "triangle-fs-answer")


if __name__ == "__main__":
    verify()
    scaling()
    duality()
    two_sided_and_rational()
    hilbert()
    sinc_energy()
    causal_even()
    ideal_lowpass()
    extra_pairs()
    periodic()
    examples()
