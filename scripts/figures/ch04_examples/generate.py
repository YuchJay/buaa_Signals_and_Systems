"""Generate figures for the pre-convolution-formula LTI example in Chapter 4."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "figures" / "04-convolution" / "examples"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INK = "#202124"
LIGHT_GRAY = "#D8D8D8"
ACCENT = "#A33A32"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "mathtext.fontset": "stix",
        "xtick.color": INK,
        "ytick.color": INK,
        "savefig.transparent": True,
    }
)


def plot_sequence(ax, indices, values, title, *, ylim):
    markerline, stemlines, _ = ax.stem(indices, values, basefmt=" ")
    plt.setp(markerline, color=ACCENT, markersize=4.5)
    plt.setp(stemlines, color=ACCENT, linewidth=1.35)
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.grid(color=LIGHT_GRAY, linewidth=0.45, alpha=0.65)
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.set_xlim(min(indices) - 0.7, max(indices) + 0.7)
    ax.set_ylim(*ylim)
    ax.set_xticks(indices)
    ax.set_xlabel(r"$n$", loc="right")
    ax.set_title(title)


def save(fig, filename):
    fig.tight_layout(pad=0.8)
    fig.savefig(OUTPUT_DIR / filename, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def style_continuous(ax, title, *, xlim, ylim, xticks=None):
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.grid(color=LIGHT_GRAY, linewidth=0.45, alpha=0.65)
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if xticks is not None:
        ax.set_xticks(xticks)
    ax.set_xlabel(r"$t$", loc="right")
    ax.set_title(title)


def draw_steps(ax, edges, values, *, color=ACCENT):
    ax.stairs(values, edges, baseline=None, color=color, linewidth=1.5)


def draw_impulse(ax, location, amplitude, label):
    ax.annotate(
        "",
        xy=(location, amplitude),
        xytext=(location, 0),
        arrowprops={"arrowstyle": "->", "color": ACCENT, "linewidth": 1.5},
    )
    ax.text(location + 0.08, amplitude, label, color=ACCENT, va="center")


def given_figure():
    indices = np.arange(-1, 3)
    x = np.array([3, 2, 1, -1])
    h = np.array([1, 1, 2, -1])

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.5))
    plot_sequence(axes[0], indices, x, r"input $x[n]$", ylim=(-1.6, 3.7))
    plot_sequence(axes[1], indices, h, r"impulse response $h[n]$", ylim=(-1.6, 3.7))
    save(fig, "lti-superposition-given.pdf")


def answer_figure():
    indices = np.arange(-2, 5)
    y = np.array([3, 5, 9, 1, -1, -3, 1])

    fig, ax = plt.subplots(figsize=(6.2, 2.65))
    plot_sequence(ax, indices, y, r"output $y[n]$", ylim=(-4.0, 10.2))
    for n, value in zip(indices, y):
        offset = 0.45 if value >= 0 else -0.65
        x_position = n + 0.08 if n == 0 else n
        alignment = "left" if n == 0 else "center"
        ax.text(
            x_position,
            value + offset,
            rf"${value}$",
            ha=alignment,
            va="center",
            color=INK,
        )
    save(fig, "lti-superposition-answer.pdf")


def geometric_step_given_figure():
    indices = np.arange(-2, 9)
    x = np.where(indices >= 0, 0.5**indices, 0.0)
    h = np.where(indices >= 0, 1.0, 0.0)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.5))
    plot_sequence(axes[0], indices, x, r"$x[n]=(1/2)^n u[n]$", ylim=(-0.15, 1.25))
    plot_sequence(axes[1], indices, h, r"$h[n]=u[n]$", ylim=(-0.15, 1.25))
    axes[1].annotate(
        "continues",
        xy=(8.5, 1.0),
        xytext=(6.2, 1.13),
        arrowprops={"arrowstyle": "->", "color": INK},
        color=INK,
        fontsize=8,
    )
    save(fig, "geometric-step-given.pdf")


def geometric_step_answer_figure():
    indices = np.arange(-2, 9)
    y = np.where(indices >= 0, 2 * (1 - 0.5 ** (indices + 1)), 0.0)

    fig, ax = plt.subplots(figsize=(6.2, 2.65))
    plot_sequence(ax, indices, y, r"$y[n]=2(1-(1/2)^{n+1})u[n]$", ylim=(-0.2, 2.25))
    ax.axhline(2, color=INK, linewidth=0.8, linestyle="--")
    ax.text(7.5, 2.05, r"limit $2$", ha="right", va="bottom", color=INK)
    save(fig, "geometric-step-answer.pdf")


def causal_exponential_figures():
    t = np.linspace(-1, 5, 900)
    x = np.where(t >= 0, np.exp(-2 * t), 0)
    h = np.where(t >= 0, np.exp(-t), 0)
    y = np.where(t >= 0, np.exp(-t) - np.exp(-2 * t), 0)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.45), sharey=True)
    axes[0].plot(t, x, color=ACCENT, linewidth=1.5)
    axes[1].plot(t, h, color=ACCENT, linewidth=1.5)
    style_continuous(axes[0], r"$x(t)=e^{-2t}u(t)$", xlim=(-1, 5), ylim=(-0.1, 1.15))
    style_continuous(axes[1], r"$h(t)=e^{-t}u(t)$", xlim=(-1, 5), ylim=(-0.1, 1.15))
    save(fig, "causal-exponential-given.pdf")

    fig, ax = plt.subplots(figsize=(6.2, 2.55))
    ax.plot(t, y, color=ACCENT, linewidth=1.5)
    style_continuous(ax, r"$y(t)=(e^{-t}-e^{-2t})u(t)$", xlim=(-1, 5), ylim=(-0.05, 0.3))
    save(fig, "causal-exponential-answer.pdf")


def rectangle_ramp_figures():
    t = np.linspace(-0.6, 2.5, 1000)
    x = np.where((t >= 0) & (t <= 1), 1.0, 0.0)
    h = np.where((t >= 0) & (t <= 1), 1 - t, 0.0)
    y = np.piecewise(
        t,
        [(t >= 0) & (t <= 1), (t > 1) & (t <= 2)],
        [lambda z: z - z**2 / 2, lambda z: (2 - z) ** 2 / 2, 0],
    )

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.45), sharey=True)
    axes[0].plot(t, x, color=ACCENT, linewidth=1.5)
    axes[1].plot(t, h, color=ACCENT, linewidth=1.5)
    style_continuous(axes[0], r"$x(t)$", xlim=(-0.6, 1.6), ylim=(-0.1, 1.15), xticks=[0, 1])
    style_continuous(axes[1], r"$h(t)$", xlim=(-0.6, 1.6), ylim=(-0.1, 1.15), xticks=[0, 1])
    save(fig, "rectangle-ramp-given.pdf")

    fig, ax = plt.subplots(figsize=(6.2, 2.55))
    ax.plot(t, y, color=ACCENT, linewidth=1.5)
    style_continuous(ax, r"$y(t)=x(t)\ast h(t)$", xlim=(-0.4, 2.4), ylim=(-0.05, 0.58), xticks=[0, 1, 2])
    save(fig, "rectangle-ramp-answer.pdf")


def equal_rectangle_figures():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.45), sharey=True)
    for ax, title in zip(axes, (r"$x(t)$", r"$h(t)$")):
        draw_steps(ax, [-1, 1], [1])
        style_continuous(ax, title, xlim=(-2, 2), ylim=(-0.1, 1.2), xticks=[-1, 0, 1])
    save(fig, "equal-rectangle-given.pdf")

    t = np.linspace(-2.5, 2.5, 800)
    y = np.maximum(2 - np.abs(t), 0)
    fig, ax = plt.subplots(figsize=(6.2, 2.55))
    ax.plot(t, y, color=ACCENT, linewidth=1.5)
    style_continuous(ax, r"$y(t)=2-|t|$ for $|t|\leq2$", xlim=(-2.5, 2.5), ylim=(-0.1, 2.2), xticks=[-2, 0, 2])
    save(fig, "equal-rectangle-answer.pdf")


def unequal_rectangle_figures():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.45), sharey=True)
    draw_steps(axes[0], [-3, 3], [1])
    draw_steps(axes[1], [-1, 1], [1])
    style_continuous(axes[0], r"$x(t)$", xlim=(-4, 4), ylim=(-0.1, 1.2), xticks=[-3, 0, 3])
    style_continuous(axes[1], r"$h(t)$", xlim=(-4, 4), ylim=(-0.1, 1.2), xticks=[-1, 0, 1])
    save(fig, "unequal-rectangle-given.pdf")

    t = np.linspace(-4.5, 4.5, 1000)
    y = np.where(np.abs(t) <= 2, 2, np.maximum(4 - np.abs(t), 0))
    fig, ax = plt.subplots(figsize=(6.2, 2.55))
    ax.plot(t, y, color=ACCENT, linewidth=1.5)
    style_continuous(ax, r"$y(t)$ for $a=3,\ b=1$", xlim=(-4.5, 4.5), ylim=(-0.1, 2.25), xticks=[-4, -2, 0, 2, 4])
    save(fig, "unequal-rectangle-answer.pdf")


def signed_piecewise_figures():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.55), sharey=True)
    draw_steps(axes[0], [-1, 0, 1], [1, -2])
    draw_steps(axes[1], [-1, 0, 1], [1, 2])
    style_continuous(axes[0], r"$x(t)$", xlim=(-1.7, 1.7), ylim=(-2.35, 2.35), xticks=[-1, 0, 1])
    style_continuous(axes[1], r"$h(t)$", xlim=(-1.7, 1.7), ylim=(-2.35, 2.35), xticks=[-1, 0, 1])
    save(fig, "signed-piecewise-given.pdf")

    t = np.linspace(-2.4, 2.4, 1200)
    y = np.piecewise(
        t,
        [
            (t >= -2) & (t < -1),
            (t >= -1) & (t < 0),
            (t >= 0) & (t < 1),
            (t >= 1) & (t <= 2),
        ],
        [lambda z: z + 2, lambda z: -z, lambda z: -4 * z, lambda z: 4 * z - 8, 0],
    )
    fig, ax = plt.subplots(figsize=(6.2, 2.7))
    ax.plot(t, y, color=ACCENT, linewidth=1.5)
    style_continuous(ax, r"$y(t)=x(t)\ast h(t)$", xlim=(-2.4, 2.4), ylim=(-4.5, 1.3), xticks=[-2, -1, 0, 1, 2])
    save(fig, "signed-piecewise-answer.pdf")


def periodic_square_triangle_figures():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.55))
    draw_steps(axes[0], np.arange(-3, 6), [1, -1, 1, -1, 1, -1, 1, -1])
    style_continuous(axes[0], r"periodic $x(t)$", xlim=(-3.2, 5.2), ylim=(-1.3, 1.3), xticks=np.arange(-3, 6))
    axes[1].plot([0, 1, 2], [0, 1, 0], color=ACCENT, linewidth=1.5)
    style_continuous(axes[1], r"$h(t)$", xlim=(-0.5, 2.5), ylim=(-0.1, 1.2), xticks=[0, 1, 2])
    save(fig, "periodic-square-triangle-given.pdf")

    t = np.linspace(-2, 4, 1600, endpoint=False)
    phase = np.mod(t, 2)
    y = np.where(phase <= 1, 2 * phase * (phase - 1), -2 * (phase - 1) * (phase - 2))
    fig, ax = plt.subplots(figsize=(6.8, 2.65))
    ax.plot(t, y, color=ACCENT, linewidth=1.5)
    style_continuous(ax, r"periodic output $y(t)$", xlim=(-2, 4), ylim=(-0.62, 0.62), xticks=np.arange(-2, 5))
    save(fig, "periodic-square-triangle-answer.pdf")


def recover_signal_impulse_figures():
    fig, ax = plt.subplots(figsize=(6.2, 2.55))
    draw_steps(ax, [2, 3, 4], [1, 2])
    draw_impulse(ax, 1, 2.5, r"$2\delta(t-1)$")
    style_continuous(ax, r"given $g(t)=x(3-2t)$", xlim=(0, 5), ylim=(-0.15, 2.9), xticks=[1, 2, 3, 4])
    save(fig, "recover-signal-impulse-given.pdf")

    fig, ax = plt.subplots(figsize=(6.2, 2.55))
    draw_steps(ax, [-5, -3, -1], [2, 1])
    draw_impulse(ax, 1, 4.0, r"$4\delta(t-1)$")
    style_continuous(ax, r"recovered $x(t)$", xlim=(-6, 2), ylim=(-0.15, 4.5), xticks=[-5, -3, -1, 0, 1])
    save(fig, "recover-signal-impulse-answer.pdf")


def main():
    given_figure()
    answer_figure()
    geometric_step_given_figure()
    geometric_step_answer_figure()
    causal_exponential_figures()
    rectangle_ramp_figures()
    equal_rectangle_figures()
    unequal_rectangle_figures()
    signed_piecewise_figures()
    periodic_square_triangle_figures()
    recover_signal_impulse_figures()
    print(f"Generated 18 figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
