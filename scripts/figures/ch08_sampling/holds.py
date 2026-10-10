"""Hold kernels, sampled LTI implementation, energy, and sampling examples."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from generate import save, style, impulse, BLUE, RED, GRAY, GREEN

plt.rcParams.update({"font.size": 10, "axes.titlesize": 11})


def stem(ax, x, y, color=BLUE):
    ax.vlines(x, 0, y, color=color, lw=1)
    ax.plot(x, y, "o", color=color, ms=3)


def pi_ticks(ax, multiples, symbol=r"\pi"):
    ax.set_xticks(np.array(multiples) * np.pi,
                  ["0" if k == 0 else
                   f"${'-' if k < 0 else ''}{'' if abs(k) == 1 else abs(k)}{symbol}$"
                   for k in multiples])


def hold_shapes():
    fig, aa = plt.subplots(2, 2, figsize=(10, 6), constrained_layout=True)
    t = np.linspace(-1.5, 2, 1401)
    aa[0, 0].plot(t, ((t >= 0) & (t < 1)).astype(float),
                  color=BLUE, label=r"$h_0,\ \tau=T$")
    aa[0, 0].plot(t, np.maximum(1-np.abs(t), 0), color=RED, label=r"$h_1$")
    style(aa[0, 0], (-1.5, 2), (-.15, 1.4))
    aa[0, 0].set(xlabel="$t/T$", title="Interpolation kernels")
    aa[0, 0].legend(loc="upper right", fontsize=9)
    n = np.arange(-3, 5)
    y = np.array([.3, .9, .5, 1.2, -.4, .2, .8, .4])
    tt = np.linspace(-3, 4, 2801)
    for ax, width, title in [(aa[0, 1], 1/3, r"Rectangular pulses: $\tau=T/3$"),
                             (aa[1, 0], 1, r"Zero-order hold: $\tau=T$")]:
        for ni, yi in zip(n, y):
            ax.plot([ni, ni, ni+width, ni+width], [0, yi, yi, 0],
                    color=BLUE, lw=1.25)
        ax.plot(n, y, "o", color=RED, ms=4, zorder=5)
        style(ax, (-3.2, 4.2), (-.65, 1.5))
        ax.set(xlabel="$t/T$", title=title)
    aa[1, 1].plot(tt, np.interp(tt, n, y), color=BLUE)
    aa[1, 1].plot(n, y, "o", color=RED, ms=4)
    style(aa[1, 1], (-3.2, 4.2), (-.65, 1.5))
    aa[1, 1].set(xlabel="$t/T$", title="First-order hold: straight segments")
    save(fig, "hold-shapes.pdf")


def hold_spectra():
    fig, aa = plt.subplots(3, 2, figsize=(10, 8), constrained_layout=True)
    v = np.linspace(-6*np.pi, 6*np.pi, 3601)
    s = np.sinc(v/(2*np.pi))
    aa[0, 0].plot(v, np.abs(s), color=BLUE)
    aa[1, 0].plot(v, s*s, color=RED)
    # Draw each phase branch separately: no lines through zeros or jumps.
    for lo, hi in zip(np.arange(-6, 6, 2), np.arange(-4, 8, 2)):
        z = np.linspace(lo*np.pi+.001, hi*np.pi-.001, 500)
        ph = np.angle(np.sinc(z/(2*np.pi))*np.exp(-1j*z/2))
        ph[np.r_[False, np.abs(np.diff(ph)) > np.pi]] = np.nan
        aa[0, 1].plot(z, ph, color=BLUE)
        aa[1, 1].plot(z, np.zeros_like(z), color=RED)
    for row in (0, 1):
        for ax in aa[row]:
            for k in (-4, -2, 2, 4):
                ax.axvline(k*np.pi, color=GRAY, ls="--", lw=.7)
            style(ax, (-5*np.pi, 5*np.pi))
            pi_ticks(ax, [-4, -2, 0, 2, 4])
            ax.set_xlabel(r"$\Omega T$")
        aa[row, 0].set_ylim(-.05, 1.15)
        aa[row, 1].set_ylim(-np.pi*1.15, np.pi*1.15)
        aa[row, 1].set_yticks([-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
    aa[0, 0].set(title="Rectangular kernel", ylabel=r"$|H_0|/T$")
    aa[0, 1].set(title="Rectangular kernel phase", ylabel=r"$\arg H_0$")
    aa[1, 0].set(title="Triangular kernel", ylabel=r"$H_1/T$")
    aa[1, 1].set(title="Triangular kernel phase", ylabel=r"$\arg H_1$")
    z = np.linspace(-np.pi+.001, np.pi-.001, 600)
    sz = np.sinc(z/(2*np.pi))
    aa[2, 0].plot(z, 1/sz, color=BLUE, label=r"$|C_0|$")
    aa[2, 0].plot(z, 1/sz**2, color=RED, label=r"$|C_1|$")
    for ax in aa[2]:
        style(ax, (-1.5*np.pi, 1.5*np.pi))
        pi_ticks(ax, [-1, 0, 1])
        ax.set_xlabel(r"$\Omega T$")
    aa[2, 0].plot([-1.5*np.pi, -np.pi], [0, 0], color=BLUE)
    aa[2, 0].plot([np.pi, 1.5*np.pi], [0, 0], color=BLUE)
    aa[2, 0].set(title="Compensation magnitude", ylabel="magnitude", ylim=(-.15, 2.8))
    aa[2, 0].legend(fontsize=9)
    aa[2, 1].plot(z, z/2, color=BLUE, label=r"$\arg C_0$")
    aa[2, 1].plot(z, z*0, color=RED, label=r"$\arg C_1$")
    aa[2, 1].set(title="Compensation phase (passband only)", ylabel="phase",
                  ylim=(-1.9, 1.9))
    aa[2, 1].set_yticks([-np.pi/2, 0, np.pi/2], [r"$-\pi/2$", "0", r"$\pi/2$"])
    aa[2, 1].legend(fontsize=9)
    save(fig, "hold-spectra.pdf")


def arrow(ax, x1, x2, y, text=None):
    ax.annotate("", (x2, y), (x1, y), arrowprops={"arrowstyle": "->", "lw": 1})
    if text:
        ax.text((x1+x2)/2, y+.09, text, ha="center", fontsize=10)


def box(ax, x, y, w, text):
    ax.add_patch(FancyBboxPatch((x, y-.15), w, .3,
                              boxstyle="round,pad=0.025", ec=BLUE, fc="#eef5fb"))
    ax.text(x+w/2, y, text, ha="center", va="center", fontsize=10)


def discrete_flow():
    fig, ax = plt.subplots(figsize=(11, 4.1), constrained_layout=True)
    ax.set(xlim=(-.3, 11.3), ylim=(-.15, 2.3))
    ax.axis("off")
    ax.text(0, 2.08, "Continuous-time LTI", color=GRAY)
    ax.text(0, 1.25, "Sampled processing", color=GRAY)
    ax.text(0, .45, "Reconstruction expanded", color=GRAY)
    for y in (1.8, 1):
        ax.text(0, y, "$x(t)$", va="center")
        ax.text(10.65, y, "$y(t)$", va="center")
    box(ax, 4, 1.8, 2.3, r"$h(t),\ H(\mathrm{j}\Omega)$")
    arrow(ax, .6, 3.95, 1.8); arrow(ax, 6.35, 10.5, 1.8)
    box(ax, 1.2, 1, 1.1, "Sample")
    box(ax, 4.5, 1, 1.5, r"$h_d[n]$")
    box(ax, 8.1, 1, 1.5, "Reconstruct")
    arrow(ax, .6, 1.1, 1); arrow(ax, 2.4, 4.4, 1, "$x[n]$")
    arrow(ax, 6.1, 8, 1, "$y[n]$"); arrow(ax, 9.7, 10.5, 1)
    ax.text(0, .05, "$y[n]$", va="center")
    box(ax, 1.2, .05, 1.65, "Impulse train")
    box(ax, 4.7, .05, 1.25, r"ZOH $h_0$")
    box(ax, 8.2, .05, 1.4, r"$C_0$")
    arrow(ax, .6, 1.1, .05); arrow(ax, 2.95, 4.6, .05, "$y_p(t)$")
    arrow(ax, 6.05, 8.1, .05, "$y_0(t)$"); arrow(ax, 9.7, 10.5, .05)
    ax.text(10.65, .05, "$y(t)$", va="center")
    save(fig, "discrete-system-flow.pdf")


def system_spectra():
    fig, aa = plt.subplots(2, 3, figsize=(11, 5.4), constrained_layout=True)
    om = np.linspace(-2, 2, 1001)
    x = np.maximum(1-np.abs(om), 0)
    h = np.maximum(1-(om/1.4)**2, 0)
    for ax, val, name in zip(aa[0], [x, h, x*h], ["X", "H", "Y"]):
        style(ax, (-2, 2), (-.05, 1.2))
        ax.plot(om, val, color=BLUE)
        ax.set(xlabel=r"$\Omega$", title=f"${name}(\\mathrm{{j}}\\Omega)$")
        ax.set_xticks([-np.pi/2, -1, 0, 1, np.pi/2],
                      [r"$-\pi/T$", "-1", "0", "1", r"$\pi/T$"])
    w = np.linspace(-3*np.pi, 3*np.pi, 3001)
    folded = (w+np.pi)%(2*np.pi)-np.pi
    xd = np.maximum(1-np.abs(folded/2), 0)/2
    hd = np.maximum(1-(folded/2/1.4)**2, 0)
    for ax, val, name in zip(aa[1], [xd, hd, xd*hd], ["X_d", "H_d", "Y_d"]):
        ax.axvspan(-np.pi, np.pi, color="#eeeeee")
        style(ax, (-3*np.pi, 3*np.pi), (-.05, 1.2))
        ax.plot(w, val, color=RED)
        ax.set(xlabel=r"$\omega$", title=f"${name}(\\mathrm{{e}}^{{\\mathrm{{j}}\\omega}})$")
        pi_ticks(ax, [-3, -2, -1, 0, 1, 2, 3])
    save(fig, "discrete-system-spectra.pdf")


def energy():
    fig = plt.figure(figsize=(10, 4.7), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.5, 1])
    t = np.linspace(-4, 4, 2001)
    for row, T in enumerate([.5, .25]):
        ax = fig.add_subplot(gs[row, 0])
        n = np.arange(int(-4/T), int(4/T)+1)
        ax.plot(t, np.sinc(t), color=GRAY, lw=1)
        stem(ax, n*T, np.sinc(n*T))
        style(ax, (-4.2, 4.2), (-.3, 1.15))
        ax.set(xlabel="$t$", title=f"$T={T}$")
    ax = fig.add_subplot(gs[:, 1]); ax.axis("off")
    table = ax.table(cellText=[["1/2", "1", "2", "1"],
                               ["1/4", "1", "4", "1"]],
                     colLabels=["$T$", "$E_c$", "$E_d$", "$TE_d$"],
                     cellLoc="center", loc="center")
    table.scale(1, 2)
    ax.set_title("Exact energies (all samples)")
    save(fig, "sample-energy.pdf")


def half_delay():
    n = np.arange(-7, 9)
    fig, ax = plt.subplots(figsize=(8, 2.7), constrained_layout=True)
    stem(ax, n, np.sinc(n-.5))
    style(ax, (-7.5, 8.5), (-.3, .8))
    ax.axvline(.5, ls="--", color=RED, lw=.8)
    ax.set(xlabel="$n$", ylabel="$h[n]$", title="Half-sample shifted sinc")
    ax.set_xticks(np.arange(-6, 9, 2))
    save(fig, "half-delay-time.pdf")
    fig, aa = plt.subplots(1, 2, figsize=(10, 3), constrained_layout=True)
    for k in range(-2, 3):
        lo, hi = (2*k-1)*np.pi, (2*k+1)*np.pi
        z = np.linspace(lo+.001, hi-.001, 400)
        aa[0].plot(z, z*0+1, color=BLUE)
        aa[1].plot(z, -(z-2*k*np.pi)/2, color=RED)
        for ax in aa:
            ax.plot([lo, hi], [1, 1] if ax is aa[0] else [np.pi/2, -np.pi/2],
                    "o", color=BLUE if ax is aa[0] else RED, mfc="white", ms=4)
    aa[0].plot(np.array([-3, -1, 1, 3])*np.pi, np.zeros(4), "o", color=BLUE, ms=4)
    for ax in aa:
        style(ax, (-3.3*np.pi, 3.3*np.pi))
        pi_ticks(ax, [-3, -2, -1, 0, 1, 2, 3]); ax.set_xlabel(r"$\omega$")
    aa[0].set(ylim=(-.12, 1.3), title="Magnitude with symmetric-limit endpoints",
              ylabel=r"$|H|$")
    aa[1].set(ylim=(-1.95, 1.95), title="Phase, one branch per period", ylabel=r"$\arg H$")
    aa[1].set_yticks([-np.pi/2, 0, np.pi/2], [r"$-\pi/2$", "0", r"$\pi/2$"])
    save(fig, "half-delay-spectrum.pdf")


def lines_lowpass():
    fig, aa = plt.subplots(1, 2, figsize=(10, 2.9), constrained_layout=True)
    t = np.linspace(-2*np.pi, 2*np.pi, 1001)
    aa[0].plot(t, 1+np.cos(t), color=BLUE)
    style(aa[0], (-2*np.pi, 2*np.pi), (-.15, 2.4))
    pi_ticks(aa[0], [-2, -1, 0, 1, 2])
    aa[0].set(xlabel="$t$", title="$x(t)=1+\\cos t$")
    ax = aa[1]; ax.set(xlim=(0, 10), ylim=(0, 1.5)); ax.axis("off")
    ax.text(0, .7, "$x(t)$", va="center")
    box(ax, 1.6, .7, 1.8, "Sample")
    box(ax, 5.7, .7, 2.2, "Lowpass")
    arrow(ax, .7, 1.5, .7); arrow(ax, 3.5, 5.6, .7, "$x_p(t)$")
    arrow(ax, 8, 9, .7); ax.text(9.2, .7, "$y(t)$", va="center")
    ax.text(2.5, .35, r"$T=\pi/3$", ha="center")
    ax.text(6.8, .32, r"$H=1,\ |\Omega|<2$", ha="center")
    save(fig, "lines-lowpass-question.pdf")
    fig, aa = plt.subplots(2, 2, figsize=(10, 6), constrained_layout=True)
    for k in range(-1, 2):
        for offset, weight in [(-1, 3), (0, 6), (1, 3)]:
            impulse(aa[0, 0], 6*k+offset, weight, str(weight), dx=.1, dy=.12)
        for offset, weight, text in [(-np.pi/3, np.pi, r"$\pi$"),
                                      (0, 2*np.pi, r"$2\pi$"),
                                      (np.pi/3, np.pi, r"$\pi$")]:
            impulse(aa[0, 1], 2*np.pi*k+offset, weight, text, dx=.12, dy=.12)
    style(aa[0, 0], (-8, 8), (-.2, 7.5))
    aa[0, 0].set(xlabel=r"$\Omega$", title=r"$X_p(\mathrm{j}\Omega)$: weights $3,6,3$")
    aa[0, 0].set_xticks([-7, -6, -5, -1, 0, 1, 5, 6, 7])
    style(aa[0, 1], (-2.7*np.pi, 2.7*np.pi), (-.2, 7.8))
    aa[0, 1].set(xlabel=r"$\omega$", title=r"$X(\mathrm{e}^{\mathrm{j}\omega})$: weights $\pi,2\pi,\pi$")
    pi_ticks(aa[0, 1], [-2, -1, 0, 1, 2])
    aa[0, 1].annotate(r"$\pi/3$", xy=(np.pi/3, 0), xytext=(2.1, 1.3),
                      arrowprops={"arrowstyle": "->", "lw": .7}, fontsize=9)
    aa[1, 0].axvspan(-2, 2, color="#eeeeee")
    for pos, weight in [(-1, 3), (0, 6), (1, 3)]:
        impulse(aa[1, 0], pos, weight, str(weight), dx=.1, dy=.12)
    style(aa[1, 0], (-8, 8), (-.2, 7.5))
    aa[1, 0].set(xlabel=r"$\Omega$", title=r"$Y(\mathrm{j}\Omega)$: retained central lines")
    aa[1, 0].set_xticks([-6, -2, -1, 0, 1, 2, 6])
    aa[1, 1].plot(t, 1+np.cos(t), color=GRAY, ls="--", label="$x(t)$")
    aa[1, 1].plot(t, 3/np.pi*(1+np.cos(t)), color=BLUE, label=r"$y(t)=(3/\pi)x(t)$")
    style(aa[1, 1], (-2*np.pi, 2*np.pi), (-.15, 2.5))
    aa[1, 1].set(xlabel="$t$", title="Output amplitude")
    pi_ticks(aa[1, 1], [-2, -1, 0, 1, 2]); aa[1, 1].legend(fontsize=9)
    save(fig, "lines-lowpass-answer.pdf")


if __name__ == "__main__":
    hold_shapes()
    hold_spectra()
    discrete_flow()
    system_spectra()
    energy()
    half_delay()
    lines_lowpass()
    print("wrote 9 sampling continuation figures")
