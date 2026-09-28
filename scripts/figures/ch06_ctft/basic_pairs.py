"""Draw CTFT pairs and magnitude/phase diagrams using dimensionless axes."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parents[3] / "figures" / "06-ctft" / "basic"
BLUE, RED, GRAY = "#25669b", "#b23a2b", "#666666"


def axes_grid(rows, cols, size):
    fig, axes = plt.subplots(rows, cols, figsize=size, constrained_layout=True)
    for ax in np.asarray(axes).flat:
        ax.axhline(0, color="#303030", lw=0.6, zorder=0)
        ax.axvline(0, color="#303030", lw=0.6, zorder=0)
        ax.grid(color="#dddddd", lw=0.45)
        ax.spines[["top", "right"]].set_visible(False)
    return fig, np.asarray(axes)


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight",
                metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)
    print(OUT / f"{name}.pdf")


def impulse(ax, position, weight, text, dx=0.14):
    ax.annotate("", (position, weight), (position, 0),
                arrowprops={"arrowstyle": "-|>", "color": RED, "lw": 1.5})
    ax.text(position + dx, weight, text, va="center", color=RED)


def exponential():
    fig, ax = axes_grid(2, 2, (8.1, 5.3))
    t = np.linspace(0, 5, 600)
    w = np.linspace(-5, 5, 1201)
    ax[0, 0].plot([-1, 0, 0], [0, 0, 1], color=BLUE)
    ax[0, 0].plot(t, np.exp(-t), color=BLUE)
    ax[0, 0].set(xlabel=r"$at$", ylabel=r"$x(t)$", title="Right-sided exponential")
    ax[0, 1].plot(w, 1/(1+w*w), color=BLUE, label=r"$a\,\Re X$")
    ax[0, 1].plot(w, -w/(1+w*w), color=RED, label=r"$a\,\Im X$")
    ax[0, 1].set(xlabel=r"$\omega/a$", title="Real and imaginary parts")
    ax[0, 1].legend(frameon=False, fontsize=8)
    ax[1, 0].plot(w, 1/np.sqrt(1+w*w), color=BLUE)
    for p, level, color in [(1, 1/np.sqrt(2), RED), (np.sqrt(3), 0.5, GRAY)]:
        ax[1, 0].hlines(level, -p, p, color=color, ls="--", lw=0.9)
        ax[1, 0].vlines([-p, p], 0, level, color=color, ls="--", lw=0.9)
    ax[1, 0].set(xlabel=r"$\omega/a$", ylabel=r"$a|X(\mathrm{j}\omega)|$",
                 title="Magnitude", ylim=(-0.04, 1.13),
                 xticks=[-np.sqrt(3), -1, 0, 1, np.sqrt(3)],
                 xticklabels=[r"$-\sqrt{3}$", r"$-1$", "0", r"$1$", r"$\sqrt{3}$"],
                 yticks=[0, 0.5, 1/np.sqrt(2), 1],
                 yticklabels=["0", r"$1/2$", r"$1/\sqrt{2}$", "1"])
    ax[1, 1].plot(w, -np.arctan(w), color=BLUE)
    ax[1, 1].axhline(np.pi/2, color=GRAY, ls="--", lw=0.7)
    ax[1, 1].axhline(-np.pi/2, color=GRAY, ls="--", lw=0.7)
    ax[1, 1].set(xlabel=r"$\omega/a$", ylabel=r"$\theta(\omega)$", title="Phase",
                 yticks=[-np.pi/2, 0, np.pi/2],
                 yticklabels=[r"$-\pi/2$", "0", r"$\pi/2$"], ylim=(-1.8, 1.8))
    save(fig, "exponential-spectrum")


def impulse_constant():
    fig, ax = axes_grid(2, 2, (7.6, 4.5))
    for a in ax.flat:
        a.set(xlim=(-3, 3), ylim=(-0.15, 1.45), xticks=[0], yticks=[])
    impulse(ax[0, 0], 0, 1, r"weight $1$")
    ax[0, 0].set(xlabel=r"$t$", title=r"$\delta(t)$")
    ax[0, 1].plot([-3, 3], [1, 1], color=BLUE)
    ax[0, 1].set(xlabel=r"$\omega$", title=r"$X(\mathrm{j}\omega)=1$",
                 yticks=[0, 1])
    ax[1, 0].plot([-3, 3], [1, 1], color=BLUE)
    ax[1, 0].set(xlabel=r"$t$", title=r"$x(t)=1$", yticks=[0, 1])
    impulse(ax[1, 1], 0, 1, r"weight $2\pi$")
    ax[1, 1].set(xlabel=r"$\omega$", title=r"$2\pi\delta(\omega)$")
    save(fig, "impulse-constant")


def rectangle():
    fig, ax = axes_grid(2, 2, (8.1, 5.0))
    w = np.linspace(-3.5, 3.5, 2801)  # w = omega*tau/(2*pi)
    transform = np.sinc(w)
    ax[0, 0].plot([-1, -.5, -.5, .5, .5, 1], [0, 0, 1, 1, 0, 0], color=BLUE)
    ax[0, 0].set(xlabel=r"$t/\tau$", ylabel=r"$x(t)/E$", title="Rectangle",
                 xticks=[-.5, 0, .5], ylim=(-.12, 1.25))
    ax[0, 1].plot(w, transform, color=BLUE)
    ax[0, 1].set(title="Signed spectrum", ylabel=r"$X(\mathrm{j}\omega)/(E\tau)$")
    ax[1, 0].plot(w, np.abs(transform), color=BLUE)
    ax[1, 0].set(title="Magnitude", ylabel=r"$|X(\mathrm{j}\omega)|/(E\tau)$")
    for a in (ax[0, 1], ax[1, 0], ax[1, 1]):
        a.set(xlabel=r"$\omega\tau/(2\pi)$", xticks=np.arange(-3, 4))
    # Draw separate intervals; no vertical segment through an undefined zero.
    for left, right in zip([-3.5, -3, -2, -1, 1, 2, 3],
                           [-3, -2, -1, 1, 2, 3, 3.5]):
        phase = 0 if np.sinc((left+right)/2) > 0 else np.pi
        ax[1, 1].plot([left, right], [phase, phase], color=BLUE)
        for p in (left, right):
            if abs(p) in (1, 2, 3):
                ax[1, 1].plot(p, phase, marker="o", mfc="white", mec=BLUE, ms=4)
    ax[1, 1].set(title="Phase (zeros excluded)", ylabel=r"$\theta(\omega)$",
                 ylim=(-0.4, 3.6), yticks=[0, np.pi], yticklabels=["0", r"$\pi$"])
    save(fig, "rectangle-spectrum")


def sinc():
    fig, ax = axes_grid(1, 2, (7.6, 2.7))
    t = np.linspace(-4, 4, 1601)  # t = omega_c*t/pi
    ax[0].plot(t, np.sinc(t), color=BLUE)
    ax[0].plot(0, 1, "o", color=RED, ms=4)
    ax[0].set(xlabel=r"$\omega_c t/\pi$", ylabel=r"$\pi x(t)/\omega_c$",
               title=r"$x(t)=\sin(\omega_c t)/(\pi t)$", xticks=[-4,-2,-1,0,1,2,4])
    ax[1].plot([-2,-1,-1,1,1,2], [0,0,1,1,0,0], color=BLUE)
    ax[1].plot([-1,1], [.5,.5], "o", color=RED, ms=4)
    ax[1].set(xlabel=r"$\omega/\omega_c$", ylabel=r"$X(\mathrm{j}\omega)$",
               title="Band-limited spectrum", xticks=[-1,0,1], ylim=(-.1,1.25))
    save(fig, "sinc-spectrum")


def harmonics():
    fig, ax = axes_grid(2, 3, (9.0, 4.6))
    t = np.linspace(-2, 2, 1001)  # t = omega0*t/pi
    for row, values, title in [(0, np.cos(np.pi*t), "Cosine"),
                               (1, np.sin(np.pi*t), "Sine")]:
        ax[row, 0].plot(t, values, color=BLUE)
        ax[row, 0].set(xlabel=r"$\omega_0t/\pi$", ylabel=r"$x(t)$", title=title)
        ax[row, 1].set(xlim=(-1.8,1.8), ylim=(-1.5,1.6), yticks=[],
                      xticks=[-1,0,1], xlabel=r"$\omega/\omega_0$")
        ax[row, 2].set(xlim=(-1.8,1.8), ylim=(-2,2),
                      xticks=[-1,0,1], xlabel=r"$\omega/\omega_0$",
                      yticks=[-np.pi/2,0,np.pi/2],
                      yticklabels=[r"$-\pi/2$","0",r"$\pi/2$"],
                      title="Line phase", ylabel=r"$\arg C$")
    ax[0, 1].set_title(r"$\Re X$: impulse weights")
    ax[1, 1].set_title(r"$\Im X$: impulse weights")
    for p in (-1,1):
        impulse(ax[0, 1], p, 1, r"$\pi$", dx=.12)
    impulse(ax[1, 1], -1, 1, r"$+\pi$", dx=.12)
    impulse(ax[1, 1], 1, -1, r"$-\pi$", dx=.12)
    ax[0, 2].plot([-1,1], [0,0], "o", color=BLUE)
    ax[1, 2].plot([-1,1], [np.pi/2,-np.pi/2], "o", color=BLUE)
    save(fig, "harmonic-spectra")


def step():
    fig, ax = axes_grid(1, 3, (9.0, 2.7))
    ax[0].plot([-3,0,0,3], [0,0,1,1], color=BLUE)
    ax[0].set(xlabel=r"$t$", ylabel=r"$u(t)$", ylim=(-.2,1.4), yticks=[0,1])
    ax[1].set(xlim=(-3,3), ylim=(-.2,1.4), yticks=[], xticks=[0],
              xlabel=r"$\omega$", title=r"$\Re U=\pi\delta(\omega)$")
    impulse(ax[1], 0, 1, r"weight $\pi$", dx=.2)
    for w in (np.linspace(-4,-.25,800), np.linspace(.25,4,800)):
        ax[2].plot(w, -1/w, color=BLUE)
    ax[2].set(xlabel=r"$\omega$", title=r"$\Im U=-\operatorname{pv}(1/\omega)$",
              ylim=(-4.5,4.5))
    save(fig, "step-spectrum")


def supplementary():
    fig, ax = axes_grid(2, 2, (7.8, 4.3))
    shapes = [
        ([-5,-3,-3,-1,-1,1,1,3,3,5], [0,0,1,1,2,2,1,1,0,0], r"$r_3+r_1$"),
        ([-5,-4,-4,-2,-2,2,2,4,4,5], [0,0,1,1,0,0,1,1,0,0], r"$r_4-r_2$"),
        ([-5,-3,-3,3,3,5], [1,1,0,0,1,1], r"$1-r_3$"),
        ([-5,-3,-3,-2,-2,2,2,3,3,5], [1,1,0,0,1,1,0,0,1,1], r"$1-r_3+r_2$"),
    ]
    for a, (t,x,title) in zip(ax.flat, shapes):
        a.plot(t,x,color=BLUE)
        a.set(title=title, xlabel=r"$t$", ylabel=r"$x(t)$", ylim=(-.15,2.4),
              xticks=[-4,-3,-2,-1,0,1,2,3,4], yticks=[0,1,2])
    save(fig, "rectangle-combinations")

    fig, ax = axes_grid(2, 2, (7.8, 4.3))
    t = np.linspace(-3,3,1601)
    w = np.linspace(-8,8,2001)
    ax[0,0].plot(t,np.maximum(1-np.abs(t)/2,0),color=BLUE)
    ax[0,1].plot(w,2*np.sinc(w/np.pi)**2,color=BLUE)
    ax[1,0].plot([-4,-3,-1,1,3,4],[0,0,1,1,0,0],color=BLUE)
    ax[1,1].plot(w,4*np.sinc(2*w/np.pi)*np.sinc(w/np.pi),color=BLUE)
    for row, title in enumerate(("Triangle", "Trapezoid")):
        ax[row,0].set(title=title,xlabel=r"$t$",ylabel=r"$x(t)$")
        ax[row,1].set(title="Signed spectrum",xlabel=r"$\omega$",ylabel=r"$X(\mathrm{j}\omega)$")
    save(fig, "triangle-trapezoid")

    fig, ax = axes_grid(1, 3, (9.0, 2.8))
    t=np.linspace(-5,7,3001)
    ax[0].plot(t,2/np.pi*np.sinc((t-1)/np.pi)*np.cos(3*t),color=BLUE)
    ax[0].set(title="Shifted sinc times carrier",xlabel=r"$t$",ylabel=r"$x(t)$")
    ax[1].plot([-5,-4,-4,-2,-2,2,2,4,4,5],[0,0,1,1,0,0,1,1,0,0],color=BLUE)
    ax[1].set(title="Magnitude",xlabel=r"$\omega$",ylabel=r"$|X|$",ylim=(-.1,1.25))
    for band, center in [((-4,-2),-3),((2,4),3)]:
        q=np.linspace(*band,100)
        ax[2].plot(q,-(q-center),color=BLUE)
    ax[2].set(title="Phase on each passband",xlabel=r"$\omega$",ylabel=r"$\theta$",
              xlim=(-5,5),ylim=(-1.3,1.3),xticks=[-4,-3,-2,0,2,3,4])
    save(fig, "shift-modulation-phase")


def sign_spectrum():
    fig, ax = axes_grid(1, 3, (9.2, 2.8))
    ax[0].plot([-3, 0, 0, 3], [-1, -1, 1, 1], color=BLUE)
    ax[0].set(xlabel=r"$t$", ylabel=r"$\operatorname{sgn}(t)$",
              title=r"$\operatorname{sgn}(t)$", ylim=(-1.4, 1.4), yticks=[-1, 0, 1])
    w_neg = np.linspace(-8, -0.45, 400)
    w_pos = np.linspace(0.45, 8, 400)
    ax[1].plot(w_neg, -2 / w_neg, color=BLUE)
    ax[1].plot(w_pos, -2 / w_pos, color=BLUE)
    ax[1].set(xlabel=r"$\omega$", ylabel=r"$\Im X$",
              title=r"$\Im X=-2/\omega$", ylim=(-5, 5))
    ax[2].plot([-8, -0.15], [np.pi / 2, np.pi / 2], color=BLUE)
    ax[2].plot([0.15, 8], [-np.pi / 2, -np.pi / 2], color=BLUE)
    ax[2].set(xlabel=r"$\omega$", ylabel=r"$\theta(\omega)$",
              title=r"undefined at $\omega=0$", xlim=(-8, 8), ylim=(-2, 2),
              yticks=[-np.pi / 2, 0, np.pi / 2],
              yticklabels=[r"$-\pi/2$", "0", r"$\pi/2$"])
    save(fig, "sign-spectrum")


def trapezoid_geometry():
    fig, ax = axes_grid(1, 3, (9.2, 2.8))
    ax[0].plot([-3, -2, -2, 2, 2, 3], [0, 0, 1, 1, 0, 0], color=BLUE)
    ax[0].set(title=r"$E_1=1,\ a=2$", xlabel=r"$t$", ylabel=r"$x_1(t)$",
              xticks=[-2, 0, 2], yticks=[0, 1], ylim=(-0.15, 1.35))
    ax[1].plot([-2, -1, -1, 1, 1, 2], [0, 0, 0.5, 0.5, 0, 0], color=BLUE)
    ax[1].set(title=r"$E_2=1/2,\ b=1$", xlabel=r"$t$", ylabel=r"$x_2(t)$",
              xticks=[-1, 0, 1], yticks=[0, 0.5], ylim=(-0.1, 0.8))
    ax[2].plot([-4, -3, -1, 1, 3, 4], [0, 0, 1, 1, 0, 0], color=BLUE)
    ax[2].set(title=r"height $2bE_1E_2=1$", xlabel=r"$t$", ylabel=r"$(x_1\ast x_2)(t)$",
              xticks=[-3, -1, 1, 3],
              xticklabels=[r"$-(a+b)$", r"$-(a-b)$", r"$a-b$", r"$a+b$"],
              yticks=[0, 1], ylim=(-0.15, 1.35))
    save(fig, "trapezoid-geometry")


def pulse_shapes():
    fig, ax = axes_grid(1, 3, (9.2, 2.8))
    ax[0].plot([-5, -4, -3, -2, 2, 3, 4, 5], [0, 0, 1, 0, 0, 1, 0, 0], color=BLUE)
    ax[0].set(title=r"$\Lambda(t-3)+\Lambda(t+3)$", xlabel=r"$t$", ylabel=r"$x(t)$",
              xticks=[-3, 0, 3], yticks=[0, 1], ylim=(-0.15, 1.35))
    ax[1].plot([-3, -2, -2, 0, 2, 2, 3], [0, 0, 1, 0, 1, 0, 0], color=BLUE)
    ax[1].set(title=r"$|t|/2,\ |t|<2$", xlabel=r"$t$", ylabel=r"$v(t)$",
              xticks=[-2, 0, 2], yticks=[0, 1], ylim=(-0.15, 1.35))
    ax[2].plot([-3, -1, 0, 4], [0, 0, 1, 1], color=BLUE)
    ax[2].set(title=r"rise on $(-1,0)$, then $1$", xlabel=r"$t$", ylabel=r"$x(t)$",
              xticks=[-1, 0], yticks=[0, 1], ylim=(-0.15, 1.35))
    save(fig, "pulse-shapes")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                         "mathtext.fontset": "stix", "axes.unicode_minus": False,
                         "axes.titlesize": 10})
    for draw in (exponential, impulse_constant, rectangle, sinc, harmonics, step,
                 supplementary, sign_spectrum, trapezoid_geometry, pulse_shapes):
        draw()


if __name__ == "__main__":
    main()
