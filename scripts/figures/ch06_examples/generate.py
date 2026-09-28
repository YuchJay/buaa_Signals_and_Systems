"""Generate figures for the Chapter 6 worked examples."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parents[3] / "figures" / "06-ctft" / "examples"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#b23a2b"
GUIDE = "#555555"


def configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "mathtext.fontset": "stix",
            "axes.unicode_minus": False,
        }
    )


def draw_spectral_data() -> None:
    fig, axes = plt.subplots(2, 1, figsize=(6.8, 4.5), constrained_layout=True)

    omega = np.array([-4.0, -2.0, -2.0, 2.0, 2.0, 4.0])
    magnitude = np.array([0.0, 0.0, 1.0, 1.0, 0.0, 0.0])
    axes[0].plot(omega, magnitude, color=ACCENT, lw=1.6)
    axes[0].set_ylabel(r"$|X(\mathrm{j}\omega)|$")
    axes[0].set_ylim(-0.12, 1.25)
    axes[0].set_yticks([0, 1])

    omega_band = np.linspace(-2.0, 2.0, 400)
    axes[1].plot(omega_band, -2*omega_band, color=ACCENT, lw=1.6)
    axes[1].plot([-4, -2, 2, 4], [np.nan] * 4, alpha=0)
    axes[1].set_ylabel(r"$\theta(\omega)$ (unwrapped)")
    axes[1].set_yticks([-4, 0, 4])
    axes[1].set_xlabel(r"$\omega$")

    for ax in axes:
        ax.axhline(0, color="black", lw=0.7)
        ax.axvline(0, color="black", lw=0.7)
        ax.set_xlim(-4, 4)
        ax.set_xticks([-4, -2, 0, 2, 4])
        ax.grid(True, color="#dddddd", lw=0.6)
    axes[1].text(
        0.69,
        0.87,
        r"undefined for $|\omega|\geq 2$",
        transform=axes[1].transAxes,
        color=GUIDE,
        fontsize=8,
    )

    fig.savefig(OUT / "phase-recovery-given.pdf", bbox_inches="tight")
    plt.close(fig)


def draw_recovered_signal() -> None:
    t = np.linspace(-4.0, 8.0, 3000)
    shifted = t - 2.0
    x = 2.0 / np.pi * np.sinc(2.0 * shifted / np.pi)

    fig, ax = plt.subplots(figsize=(6.8, 3.2), constrained_layout=True)
    ax.plot(t, x, color=ACCENT, lw=1.6)
    ax.scatter([2.0], [2.0 / np.pi], color=ACCENT, s=20, zorder=3)
    ax.axhline(0, color="black", lw=0.7)
    ax.axvline(0, color="black", lw=0.7)
    ax.axvline(2, color=GUIDE, lw=0.8, ls="--")
    ax.text(2.12, 2.0 / np.pi, r"$x(2)=2/\pi$", va="center")
    ax.set_xlim(-4, 8)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$x(t)$")
    ax.grid(True, color="#dddddd", lw=0.6)
    fig.savefig(OUT / "phase-recovery-answer.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    configure()
    draw_spectral_data()
    draw_recovered_signal()
    draw_new_examples()
    for name in ("phase-recovery-given.pdf", "phase-recovery-answer.pdf"):
        print(f"Generated {OUT / name}")


def save_answer(name: str, t: np.ndarray, curves: list, ylabel: str) -> None:
    fig, ax = plt.subplots(figsize=(6.5, 2.5), constrained_layout=True)
    for values, label in curves:
        ax.plot(t, values, lw=1.5, label=label)
    ax.axhline(0, color="black", lw=0.6)
    ax.axvline(0, color="black", lw=0.6)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(ylabel)
    ax.grid(True, color="#dddddd", lw=0.5)
    ax.legend(frameon=False)
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)


def draw_new_examples() -> None:
    t = np.linspace(-1, 8, 1801)
    p = np.maximum(t, 0)
    u = (t >= 0).astype(float)
    save_answer(
        "exponential-convolution-answer.pdf", t,
        [((np.exp(-p) - np.exp(-3*p))/2*u, r"$a=1,\ b=3$"),
         (p*np.exp(-p)*u, r"$a=b=1$")], r"$y(t)$",
    )
    # The discontinuity at t=0 is drawn with its one-sided limits.
    ti = np.concatenate(([-1.0, 0.0], np.linspace(0, 8, 1601)))
    hi = np.concatenate(([0.0, 0.0],
                         (np.exp(-ti[2:])+np.exp(-3*ti[2:]))/2))
    save_answer("exponential-identification-answer.pdf", ti,
                [(hi, r"$h(t)$")], r"$h(t)$")
    save_answer("three-pole-answer.pdf", t,
                [(0.5*np.exp(-p)*(1-np.exp(-p))**2*u, r"$x(t)$")], r"$x(t)$")
    save_answer("differential-equation-answer.pdf", t,
                [((np.exp(-p)/4+p*np.exp(-p)/2-np.exp(-3*p)/4)*u,
                  r"$y(t)$")], r"$y(t)$")
    omega = np.linspace(-5, 5, 2001)
    spectrum = np.maximum(1-np.abs(omega-3), 0)+np.maximum(1-np.abs(omega+3), 0)
    fig, ax = plt.subplots(figsize=(6.5, 2.5), constrained_layout=True)
    ax.plot(omega, spectrum, color=ACCENT, lw=1.5)
    ax.axhline(0, color="black", lw=0.6)
    ax.axvline(0, color="black", lw=0.6)
    ax.set_xticks([-4, -3, -2, 0, 2, 3, 4])
    ax.set_yticks([0, 1])
    ax.set_xlabel(r"$\omega$")
    ax.set_ylabel(r"$X(\mathrm{j}\omega)$")
    ax.grid(True, color="#dddddd", lw=0.5)
    fig.savefig(OUT / "two-triangle-given.pdf", bbox_inches="tight")
    plt.close(fig)
    t = np.linspace(-12, 12, 4801)
    answer = np.sinc(t/(2*np.pi))**2*np.cos(3*t)/np.pi
    save_answer("two-triangle-answer.pdf", t,
                [(answer, r"$x(t)$")], r"$x(t)$")

    fig, ax = plt.subplots(figsize=(6.5, 2.5), constrained_layout=True)
    ax.plot([-5, -4, -3, -2, 2, 3, 4, 5], [0, 0, -1, 0, 0, 1, 0, 0], color=ACCENT, lw=1.6)
    ax.axhline(0, color="black", lw=0.6)
    ax.axvline(0, color="black", lw=0.6)
    ax.set_xticks([-4, -3, -2, 0, 2, 3, 4])
    ax.set_yticks([-1, 0, 1])
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$x(t)$")
    ax.grid(True, color="#dddddd", lw=0.5)
    fig.savefig(OUT / "triangle-difference-given.pdf", bbox_inches="tight")
    plt.close(fig)

    omega = np.linspace(-8, 8, 4001)
    sa = np.sinc(omega / (2 * np.pi))
    imag = -2 * sa**2 * np.sin(3 * omega)
    fig, ax = plt.subplots(figsize=(6.5, 2.5), constrained_layout=True)
    ax.plot(omega, imag, color=ACCENT, lw=1.3)
    ax.axhline(0, color="black", lw=0.6)
    ax.axvline(0, color="black", lw=0.6)
    ax.set_xlim(-8, 8)
    ax.set_xlabel(r"$\omega$")
    ax.set_ylabel(r"$\Im X(\mathrm{j}\omega)$")
    ax.grid(True, color="#dddddd", lw=0.5)
    fig.savefig(OUT / "triangle-difference-answer.pdf", bbox_inches="tight")
    plt.close(fig)

    tt = np.linspace(-8, 8, 1601)
    tri = np.maximum(3 - np.abs(tt) / 2, 0)
    save_answer("squared-sine-answer.pdf", tt, [(tri, r"$x(t)$")], r"$x(t)$")

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.6), constrained_layout=True)
    axes[0].plot([-1, 0, 0, 2, 2, 3], [0, 0, 1, 1, 0, 0], color=ACCENT, lw=1.6)
    axes[0].set_ylabel(r"$x(t)$")
    axes[1].plot([-1, 0, 1, 2, 3], [0, 0, 1, 0, 0], color=ACCENT, lw=1.6)
    axes[1].set_ylabel(r"$y(t)$")
    for axis in axes:
        axis.axhline(0, color="black", lw=0.6)
        axis.axvline(0, color="black", lw=0.6)
        axis.set_xlabel(r"$t$")
        axis.set_yticks([0, 1])
        axis.set_ylim(-0.15, 1.35)
        axis.grid(True, color="#dddddd", lw=0.5)
    fig.savefig(OUT / "lti-identification-given.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
